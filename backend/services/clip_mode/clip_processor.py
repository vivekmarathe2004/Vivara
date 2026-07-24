from backend.services.subtitle.whisper_service import WhisperService
from backend.services.llm.base import LLMProvider
from backend.services.render.ffmpeg_renderer import FFmpegRenderer
import json
import os
import subprocess
from pathlib import Path

class ClipProcessor:
    def __init__(self, whisper: WhisperService, llm: LLMProvider, ffmpeg: FFmpegRenderer):
        self.whisper = whisper
        self.llm = llm
        self.ffmpeg = ffmpeg

    async def transcribe(self, video_path: str) -> dict:
        return await self.whisper.transcribe_file(video_path)

    async def find_viral_moments(self, transcript: dict, count: int = 5) -> list[dict]:
        text = transcript.get("text", "")
        if not text:
            return [{"start": 0, "end": 30, "title": "Viral Hook Segment", "hook": "Essential video snippet"}]

        messages = [
            {
                "role": "system", 
                "content": f"Analyze this transcript and return top {count} viral moments. Return ONLY a JSON list matching this structure: [{{\"start\": 12, \"end\": 45, \"title\": \"Hook Title\", \"hook\": \"Opening sentence\"}}]"
            },
            {"role": "user", "content": text[:4000]}
        ]
        resp = await self.llm.generate(messages)
        try:
            clean = resp.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            data = json.loads(clean.strip())
            if isinstance(data, list):
                return data
        except Exception:
            pass
        return [{"start": 0, "end": 30, "title": "Viral Highlight", "hook": "Key moments breakdown"}]

    async def cut_clips(self, video_path: str, moments: list[dict], output_dir: str) -> list[str]:
        clips = []
        os.makedirs(output_dir, exist_ok=True)
        
        for i, moment in enumerate(moments):
            out_path = os.path.join(output_dir, f"clip_{i:02d}.mp4")
            start = moment.get("start", 0)
            end = moment.get("end", start + 30)
            duration = max(5, end - start)
            
            # Fast accurate cut with re-encoding for clean keyframes
            cmd = [
                self.ffmpeg.ffmpeg, "-y",
                "-ss", str(start),
                "-i", video_path,
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac", "-b:a", "192k",
                out_path
            ]
            subprocess.run(cmd, capture_output=True, check=False)
            if os.path.exists(out_path):
                clips.append(out_path)
        return clips

    async def add_captions(self, clip_path: str, transcript_segment: dict, style: str) -> str:
        if not os.path.exists(clip_path):
            return clip_path
        
        # Build subtitle ASS file for clip
        out_ass = clip_path.replace(".mp4", ".ass")
        segments = transcript_segment.get("segments", [{"start": 0, "end": 10, "text": "Repurposed Short"}])
        ass_content = self.whisper.generate_ass(segments, style_preset=style)
        with open(out_ass, "w", encoding="utf-8") as f:
            f.write(ass_content)

        out_captioned = clip_path.replace(".mp4", "_captioned.mp4")
        safe_ass = str(Path(out_ass).resolve()).replace("\\", "/").replace(":", "\\:")
        
        cmd = [
            self.ffmpeg.ffmpeg, "-y",
            "-i", clip_path,
            "-vf", f"subtitles='{safe_ass}'",
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "copy",
            out_captioned
        ]
        subprocess.run(cmd, capture_output=True, check=False)
        return out_captioned if os.path.exists(out_captioned) else clip_path

    async def export_shorts(
        self, 
        clips: list[str], 
        output_dir: str, 
        aspect_ratio: str = "9:16", 
        add_zoom: bool = True
    ) -> list[str]:
        final_clips = []
        os.makedirs(output_dir, exist_ok=True)
        width, height = (1080, 1920) if aspect_ratio == "9:16" else (1920, 1080)

        for i, clip in enumerate(clips):
            if not os.path.exists(clip):
                continue
            out_path = os.path.join(output_dir, f"short_{i:02d}.mp4")
            
            crop_filter = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},format=yuv420p"
            if add_zoom:
                crop_filter = f"scale={width+100}:{height+100}:force_original_aspect_ratio=increase,crop={width}:{height},format=yuv420p"

            cmd = [
                self.ffmpeg.ffmpeg, "-y",
                "-i", clip,
                "-vf", crop_filter,
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac", "-b:a", "192k",
                out_path
            ]
            subprocess.run(cmd, capture_output=True, check=False)
            if os.path.exists(out_path):
                final_clips.append(out_path)
        return final_clips
