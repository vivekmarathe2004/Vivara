"""
Pipeline Stage Runner
---------------------
Orchestrates running each stage of the video generation pipeline.
Each stage is fully independent: run, re-run, edit, or skip without
affecting other stages.

Stage order: script → voice → subtitles → media → render
"""
from __future__ import annotations

import asyncio
import datetime
import json
import traceback
from pathlib import Path

from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import SessionLocal
from backend.models.job import PipelineStage
from backend.models.project import Project
from backend.services.llm.factory import get_llm_provider
from backend.services.tts.factory import get_tts_provider
from backend.services.subtitle.whisper_service import WhisperService
from backend.services.script.script_generator import ScriptGenerator
from backend.services.script.scene_planner import ScenePlanner
from backend.services.script.metadata_generator import MetadataGenerator
from backend.services.media.pexels_provider import PexelsProvider
from backend.services.media.pixabay_provider import PixabayProvider
from backend.services.media.unsplash_provider import UnsplashProvider
from backend.services.media.openverse_provider import OpenverseProvider
from backend.services.render.ffmpeg_renderer import FFmpegRenderer

# Storage root (one level above backend/)
STORAGE = Path(__file__).parent.parent.parent.parent / "storage"


def _get_db() -> Session:
    return SessionLocal()


def _update_stage(db: Session, stage: PipelineStage, **kwargs):
    """Apply keyword updates to a stage and commit."""
    for k, v in kwargs.items():
        setattr(stage, k, v)
    db.commit()
    db.refresh(stage)


class PipelineStageRunner:
    """Runs individual pipeline stages for a given project."""

    async def run_stage(self, project_id: str, stage_name: str) -> None:
        """Run or re-run a single named stage for *project_id*."""
        dispatch = {
            "script": self._run_script,
            "voice": self._run_voice,
            "subtitles": self._run_subtitles,
            "media": self._run_media,
            "render": self._run_render,
        }
        handler = dispatch.get(stage_name)
        if handler is None:
            raise ValueError(f"Unknown stage: {stage_name!r}")

        db = _get_db()
        try:
            stage = (
                db.query(PipelineStage)
                .filter(
                    PipelineStage.project_id == project_id,
                    PipelineStage.stage == stage_name,
                )
                .first()
            )
            if stage is None:
                return

            _update_stage(
                db,
                stage,
                status="running",
                progress=0,
                error_msg=None,
                log="",
                started_at=datetime.datetime.utcnow(),
                completed_at=None,
            )

            # Update parent project status to running
            project = db.query(Project).filter(Project.id == project_id).first()
            if project:
                project.status = "running"
                db.commit()
        finally:
            db.close()

        # Run the actual stage logic
        try:
            await handler(project_id)
        except Exception as exc:
            db = _get_db()
            try:
                stage = (
                    db.query(PipelineStage)
                    .filter(
                        PipelineStage.project_id == project_id,
                        PipelineStage.stage == stage_name,
                    )
                    .first()
                )
                if stage:
                    _update_stage(
                        db,
                        stage,
                        status="error",
                        error_msg=str(exc),
                        log=traceback.format_exc(),
                        completed_at=datetime.datetime.utcnow(),
                    )
                project = db.query(Project).filter(Project.id == project_id).first()
                if project:
                    project.status = "error"
                    db.commit()
            finally:
                db.close()

    async def run_all(self, project_id: str) -> None:
        """Run all non-skipped, non-done stages in pipeline order."""
        for stage_name in ["script", "voice", "subtitles", "media", "render"]:
            db = _get_db()
            try:
                stage = (
                    db.query(PipelineStage)
                    .filter(
                        PipelineStage.project_id == project_id,
                        PipelineStage.stage == stage_name,
                    )
                    .first()
                )
                if stage is None or stage.status in ("done", "skipped"):
                    continue
            finally:
                db.close()

            await self.run_stage(project_id, stage_name)

            # Stop if this stage errored
            db = _get_db()
            try:
                stage = (
                    db.query(PipelineStage)
                    .filter(
                        PipelineStage.project_id == project_id,
                        PipelineStage.stage == stage_name,
                    )
                    .first()
                )
                if stage and stage.status == "error":
                    break
            finally:
                db.close()

    # ──────────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _get_project(self, db: Session, project_id: str) -> Project:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project is None:
            raise ValueError(f"Project {project_id!r} not found")
        return project

    def _get_stage(self, db: Session, project_id: str, stage_name: str) -> PipelineStage:
        stage = (
            db.query(PipelineStage)
            .filter(
                PipelineStage.project_id == project_id,
                PipelineStage.stage == stage_name,
            )
            .first()
        )
        if stage is None:
            raise ValueError(f"Stage {stage_name!r} not found for project {project_id!r}")
        return stage

    def _set_progress(self, project_id: str, stage_name: str, progress: int, log: str = ""):
        db = _get_db()
        try:
            stage = self._get_stage(db, project_id, stage_name)
            _update_stage(db, stage, progress=progress, log=log)
        finally:
            db.close()

    def _mark_done(self, project_id: str, stage_name: str, result_path: str = "", log: str = ""):
        db = _get_db()
        try:
            stage = self._get_stage(db, project_id, stage_name)
            _update_stage(
                db,
                stage,
                status="done",
                progress=100,
                result_path=result_path,
                log=log,
                completed_at=datetime.datetime.utcnow(),
            )
            if stage_name == "render":
                project = self._get_project(db, project_id)
                project.output_path = result_path
                project.status = "done"
                db.commit()
        finally:
            db.close()

    def _project_dir(self, project_id: str) -> Path:
        d = STORAGE / "projects" / project_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    # ──────────────────────────────────────────────────────────────────────────
    # Stage implementations
    # ──────────────────────────────────────────────────────────────────────────

    async def _run_script(self, project_id: str) -> None:
        """Stage 1: Generate script using LLM."""
        db = _get_db()
        try:
            project = self._get_project(db, project_id)
            proj_settings = json.loads(project.settings_json or "{}")
            topic = project.topic
            video_type = project.video_type
        finally:
            db.close()

        self._set_progress(project_id, "script", 10, "Connecting to LLM provider...")

        llm = get_llm_provider(settings)
        generator = ScriptGenerator(llm)

        self._set_progress(project_id, "script", 25, "Generating script...")
        result = await generator.generate(video_type, topic, proj_settings)

        self._set_progress(project_id, "script", 80, "Parsing scenes...")
        scene_planner = ScenePlanner()
        scenes = scene_planner.parse_scenes(result.get("script", ""))
        result["scenes"] = scenes

        self._set_progress(project_id, "script", 95, "Saving script...")

        proj_dir = self._project_dir(project_id)
        script_path = proj_dir / "script.json"
        script_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

        db = _get_db()
        try:
            project = self._get_project(db, project_id)
            project.script = result.get("script", "")
            db.commit()
        finally:
            db.close()

        self._mark_done(project_id, "script", str(script_path), "Script generated successfully.")

    async def _run_voice(self, project_id: str) -> None:
        """Stage 2: Generate voiceover using TTS."""
        db = _get_db()
        try:
            project = self._get_project(db, project_id)
            script_text = project.script or ""
            proj_settings = json.loads(project.settings_json or "{}")
        finally:
            db.close()

        if not script_text:
            raise ValueError("No script found. Run the Script stage first.")

        self._set_progress(project_id, "voice", 10, "Loading TTS engine...")

        tts = get_tts_provider(settings)
        voice = proj_settings.get("voice", settings.tts_voice)

        proj_dir = self._project_dir(project_id)
        audio_path = str(proj_dir / "voiceover.wav")

        self._set_progress(project_id, "voice", 30, "Synthesizing speech...")
        tts_result = await tts.synthesize(script_text, audio_path, voice)

        self._set_progress(project_id, "voice", 90, "Saving audio...")
        timings_path = proj_dir / "word_timings.json"
        timings_path.write_text(
            json.dumps(tts_result.get("word_timings", []), indent=2), encoding="utf-8"
        )

        self._mark_done(
            project_id, "voice", tts_result.get("audio_path", audio_path),
            f"TTS complete. Duration: {tts_result.get('duration', 0):.1f}s"
        )

    async def _run_subtitles(self, project_id: str) -> None:
        """Stage 3: Generate subtitles from the voiceover audio."""
        db = _get_db()
        try:
            voice_stage = self._get_stage(db, project_id, "voice")
            audio_path = voice_stage.result_path or ""
        finally:
            db.close()

        if not audio_path or not Path(audio_path).exists():
            raise ValueError("No voiceover audio found. Run the Voice stage first.")

        self._set_progress(project_id, "subtitles", 10, "Loading Whisper model...")
        whisper = WhisperService(settings.whisper_model)

        self._set_progress(project_id, "subtitles", 30, "Transcribing audio...")
        transcript = await whisper.transcribe(audio_path)

        self._set_progress(project_id, "subtitles", 70, "Generating subtitle files...")
        proj_dir = self._project_dir(project_id)

        srt_content = whisper.generate_srt(transcript["segments"])
        srt_path = proj_dir / "subtitles.srt"
        srt_path.write_text(srt_content, encoding="utf-8")

        ass_content = whisper.generate_ass(transcript["segments"])
        ass_path = proj_dir / "subtitles.ass"
        ass_path.write_text(ass_content, encoding="utf-8")

        self._mark_done(
            project_id, "subtitles", str(ass_path),
            f"Subtitles generated. {len(transcript['segments'])} segments."
        )

    async def _run_media(self, project_id: str) -> None:
        """Stage 4: Fetch stock media for each scene."""
        proj_dir = self._project_dir(project_id)
        script_json_path = proj_dir / "script.json"

        if not script_json_path.exists():
            raise ValueError("No script.json found. Run the Script stage first.")

        with open(script_json_path, encoding="utf-8") as f:
            script_data = json.load(f)

        scenes = script_data.get("scenes", [])
        if not scenes:
            self._mark_done(project_id, "media", "", "No scenes to fetch media for.")
            return

        self._set_progress(project_id, "media", 5, "Initialising media providers...")

        providers = []
        if settings.pexels_api_key:
            providers.append(PexelsProvider(settings.pexels_api_key))
        if settings.pixabay_api_key:
            providers.append(PixabayProvider(settings.pixabay_api_key))
        if settings.unsplash_api_key:
            providers.append(UnsplashProvider(settings.unsplash_api_key))
        
        # Always append Openverse (100% free open license media, zero key required!)
        providers.append(OpenverseProvider())

        media_dir = proj_dir / "media"
        media_dir.mkdir(exist_ok=True)
        media_manifest = []

        for idx, scene in enumerate(scenes):
            query = scene.get("search_query", scene.get("description", "nature"))
            progress = 10 + int((idx / len(scenes)) * 80)
            self._set_progress(
                project_id, "media", progress,
                f"Searching media for scene {idx + 1}/{len(scenes)}: {query!r}"
            )

            downloaded = False
            for provider in providers:
                try:
                    results = await provider.search_videos(query, per_page=3)
                    if not results:
                        results = await provider.search_images(query, per_page=3)

                    if results:
                        clip = results[0]
                        dl_url = clip.get("download_url") or clip.get("preview_url", "")
                        if dl_url:
                            ext = ".jpg" if clip.get("type") == "image" else ".mp4"
                            out_path = str(media_dir / f"scene_{idx:03d}{ext}")
                            await provider.download(dl_url, out_path)
                            media_manifest.append({
                                "scene_index": idx,
                                "query": query,
                                "path": out_path,
                                "source": clip.get("source", ""),
                            })
                            downloaded = True
                            break
                except Exception:
                    continue

            if not downloaded:
                media_manifest.append({
                    "scene_index": idx,
                    "query": query,
                    "path": "",
                    "source": "none",
                })

        manifest_path = proj_dir / "media_manifest.json"
        manifest_path.write_text(json.dumps(media_manifest, indent=2), encoding="utf-8")

        found = sum(1 for m in media_manifest if m["path"])
        self._mark_done(
            project_id, "media", str(manifest_path),
            f"Downloaded {found}/{len(scenes)} media items."
        )

    async def _run_render(self, project_id: str) -> None:
        """Stage 5: Render final video with FFmpeg."""
        proj_dir = self._project_dir(project_id)

        db = _get_db()
        try:
            project = self._get_project(db, project_id)
            proj_settings = json.loads(project.settings_json or "{}")
            voice_stage = self._get_stage(db, project_id, "voice")
            subtitle_stage = self._get_stage(db, project_id, "subtitles")
        finally:
            db.close()

        audio_path = voice_stage.result_path or ""
        subtitle_path = subtitle_stage.result_path or ""

        manifest_path = proj_dir / "media_manifest.json"
        if manifest_path.exists():
            with open(manifest_path, encoding="utf-8") as f:
                media_manifest = json.load(f)
        else:
            media_manifest = []

        self._set_progress(project_id, "render", 5, "Preparing FFmpeg renderer...")

        renderer = FFmpegRenderer(settings.ffmpeg_path, settings.gpu_enabled)
        output_dir = STORAGE / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / f"{project_id}.mp4")

        def progress_cb(pct: int, msg: str = ""):
            self._set_progress(project_id, "render", pct, msg or f"Rendering... {pct}%")

        self._set_progress(project_id, "render", 10, "Starting FFmpeg render...")

        final_path = await renderer.render_video(
            project_id=project_id,
            scenes=media_manifest,
            audio_path=audio_path,
            subtitle_path=subtitle_path,
            output_path=output_path,
            settings=proj_settings,
            progress_callback=progress_cb,
        )

        try:
            thumb_path = str(proj_dir / "thumbnail.jpg")
            await renderer.generate_thumbnail(final_path, thumb_path)
            db = _get_db()
            try:
                project = self._get_project(db, project_id)
                project.thumbnail_path = thumb_path
                db.commit()
            finally:
                db.close()
        except Exception:
            pass

        self._mark_done(
            project_id, "render", final_path,
            f"Video rendered successfully: {final_path}"
        )
