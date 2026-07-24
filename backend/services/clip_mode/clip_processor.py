from backend.services.subtitle.whisper_service import WhisperService
from backend.services.llm.base import LLMProvider
from backend.services.render.ffmpeg_renderer import FFmpegRenderer
import json
import os

class ClipProcessor:
    def __init__(self, whisper: WhisperService, llm: LLMProvider, ffmpeg: FFmpegRenderer):
        self.whisper = whisper
        self.llm = llm
        self.ffmpeg = ffmpeg

    async def transcribe(self, video_path: str) -> dict:
        return await self.whisper.transcribe_file(video_path)

    async def find_viral_moments(self, transcript: dict, count: int = 5) -> list[dict]:
        text = transcript.get("text", "")
        messages = [
            {"role": "system", "content": f"Find {count} viral moments in this transcript. Return ONLY JSON list: [{{'start': 0, 'end': 30, 'title': '...', 'hook': '...'}}]"},
            {"role": "user", "content": text}
        ]
        resp = await self.llm.generate(messages)
        try:
            if resp.startswith("```"):
                resp = resp.split("```")[1]
                if resp.startswith("json"):
                    resp = resp[4:]
            return json.loads(resp)
        except:
            return [{"start": 0, "end": 30, "title": "Highlight", "hook": "Awesome moment"}]

    async def cut_clips(self, video_path: str, moments: list[dict], output_dir: str) -> list[str]:
        clips = []
        for i, moment in enumerate(moments):
            out_path = os.path.join(output_dir, f"clip_{i}.mp4")
            start = moment.get("start", 0)
            end = moment.get("end", start + 30)
            duration = end - start
            cmd = [self.ffmpeg.ffmpeg, "-y", "-i", video_path, "-ss", str(start), "-t", str(duration), "-c:v", "copy", "-c:a", "copy", out_path]
            import subprocess
            subprocess.run(cmd)
            clips.append(out_path)
        return clips

    async def add_captions(self, clip_path: str, transcript_segment: dict, style: str) -> str:
        # A real implementation would use ffmpeg renderer to burn subtitles
        return clip_path

    async def export_shorts(self, clips: list[str], output_dir: str, aspect_ratio: str = "9:16", add_zoom: bool = True) -> list[str]:
        final_clips = []
        for i, clip in enumerate(clips):
            out_path = os.path.join(output_dir, f"short_{i}.mp4")
            # In a real app we'd add crop filter for vertical video and zoom effects
            cmd = [self.ffmpeg.ffmpeg, "-y", "-i", clip, "-vf", "crop=ih*9/16:ih", "-c:a", "copy", out_path]
            import subprocess
            subprocess.run(cmd)
            final_clips.append(out_path)
        return final_clips
