"""
FFmpeg Renderer
---------------
Assembles stock video clips, images, voiceover audio, and subtitles into a final MP4.
Supports NVENC (NVIDIA), AMF (AMD), and CPU fallback automatically.
"""
from __future__ import annotations

import asyncio
import os
import subprocess
import json
import shutil
from pathlib import Path


class FFmpegRenderer:
    def __init__(self, ffmpeg_path: str = "ffmpeg", gpu_enabled: bool = True):
        self.ffmpeg = ffmpeg_path
        self.gpu_enabled = gpu_enabled
        self._gpu_info: dict | None = None

    def detect_gpu(self) -> dict:
        """Check which GPU video encoders are available via FFmpeg."""
        if self._gpu_info is not None:
            return self._gpu_info

        result = {
            "cuda_available": False,
            "nvenc_supported": False,
            "amf_supported": False,
            "qsv_supported": False,
            "device": "CPU (libx264)",
        }

        try:
            res = subprocess.run(
                [self.ffmpeg, "-hide_banner", "-encoders"],
                capture_output=True, text=True, timeout=10
            )
            stdout = res.stdout.lower()
            if "h264_nvenc" in stdout:
                result.update(cuda_available=True, nvenc_supported=True, device="NVIDIA NVENC")
            elif "h264_amf" in stdout:
                result.update(amf_supported=True, device="AMD AMF")
            elif "h264_qsv" in stdout:
                result.update(qsv_supported=True, device="Intel QSV")
        except Exception:
            pass

        try:
            smi = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=5
            )
            if smi.returncode == 0 and smi.stdout.strip():
                result["device"] = smi.stdout.strip().splitlines()[0]
        except Exception:
            pass

        self._gpu_info = result
        return result

    def _video_codec(self) -> list[str]:
        """Return the best available video codec args for this machine."""
        if not self.gpu_enabled:
            return ["-c:v", "libx264", "-preset", "fast", "-crf", "23"]

        gpu = self.detect_gpu()
        if gpu["nvenc_supported"]:
            return ["-c:v", "h264_nvenc", "-preset", "p4", "-rc", "vbr", "-cq", "23"]
        if gpu["amf_supported"]:
            return ["-c:v", "h264_amf", "-quality", "balanced"]
        if gpu["qsv_supported"]:
            return ["-c:v", "h264_qsv", "-preset", "medium"]
        return ["-c:v", "libx264", "-preset", "fast", "-crf", "23"]

    async def render_video(
        self,
        project_id: str,
        scenes: list[dict],
        audio_path: str,
        subtitle_path: str,
        output_path: str,
        settings: dict,
        progress_callback,
    ) -> str:
        await asyncio.get_event_loop().run_in_executor(
            None,
            self._render_sync,
            project_id,
            scenes,
            audio_path,
            subtitle_path,
            output_path,
            settings,
            progress_callback,
        )
        return output_path

    def _render_sync(
        self,
        project_id: str,
        scenes: list[dict],
        audio_path: str,
        subtitle_path: str,
        output_path: str,
        settings: dict,
        progress_callback,
    ):
        """Synchronous render — runs in a thread executor."""
        aspect = settings.get("aspect_ratio", "16:9")
        width, height = (1920, 1080) if aspect == "16:9" else (1080, 1920)

        progress_callback(10, "Building scene list...")
        valid_scenes = [s for s in scenes if s.get("path") and Path(s["path"]).exists()]

        if not valid_scenes:
            blank_path = str(Path(output_path).parent / "blank.mp4")
            subprocess.run(
                [
                    self.ffmpeg, "-y",
                    "-f", "lavfi",
                    "-i", f"color=c=black:s={width}x{height}:r=30:d=10",
                    "-c:v", "libx264", "-t", "10", blank_path,
                ],
                capture_output=True, check=False
            )
            valid_scenes = [{"path": blank_path}]

        concat_file = str(Path(output_path).parent / f"{project_id}_concat.txt")
        with open(concat_file, "w", encoding="utf-8") as f:
            for s in valid_scenes:
                abs_path = str(Path(s["path"]).resolve()).replace("\\", "/")
                f.write(f"file '{abs_path}'\n")

        progress_callback(20, "Concatenating clips...")
        concat_out = str(Path(output_path).parent / f"{project_id}_concat.mp4")
        scale_filter = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,format=yuv420p"

        concat_cmd = [
            self.ffmpeg, "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-vf", scale_filter,
            "-c:v", "libx264", "-preset", "fast",
            "-an",
            concat_out,
        ]
        res = subprocess.run(concat_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Concat failed:\n{res.stderr[-2000:]}")

        progress_callback(60, "Mixing audio and subtitles...")
        video_filters = []
        inputs = ["-i", concat_out]

        has_audio = audio_path and Path(audio_path).exists()
        if has_audio:
            inputs += ["-i", audio_path]

        if subtitle_path and Path(subtitle_path).exists():
            safe_sub = str(Path(subtitle_path).resolve()).replace("\\", "/").replace(":", "\\:")
            video_filters.append(f"subtitles='{safe_sub}'")

        final_cmd = [self.ffmpeg, "-y"] + inputs

        if video_filters:
            final_cmd += ["-vf", ",".join(video_filters)]

        # Map explicitly: input 0 for video, input 1 for audio (if available)
        if has_audio:
            final_cmd += ["-map", "0:v:0", "-map", "1:a:0"]
        else:
            final_cmd += ["-map", "0:v:0"]

        final_cmd += self._video_codec()
        
        if has_audio:
            final_cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]

        final_cmd.append(output_path)

        progress_callback(75, "Running final FFmpeg pass...")
        res = subprocess.run(final_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Final render failed:\n{res.stderr[-2000:]}")

        for tmp in [concat_file, concat_out]:
            try:
                os.remove(tmp)
            except Exception:
                pass

        progress_callback(98, "Finalizing...")

    async def generate_thumbnail(self, video_path: str, output_path: str) -> str:
        """Extract a frame at 2 seconds as JPEG thumbnail."""
        cmd = [
            self.ffmpeg, "-y",
            "-ss", "2",
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            output_path,
        ]
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: subprocess.run(cmd, capture_output=True, check=False)
        )
        return output_path

    def _build_ffmpeg_cmd(self, **kwargs) -> list[str]:
        return [self.ffmpeg, "-y", "-hide_banner", "-loglevel", "error"]
