from faster_whisper import WhisperModel
import os
import subprocess
from pathlib import Path

class WhisperService:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None

    def _load_model(self):
        if self.model is None:
            # Fallback handling if faster-whisper is not compiled with CUDA
            try:
                self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
            except Exception:
                # If tiny/base fails, fallback to tiny
                self.model = WhisperModel("tiny", device="cpu", compute_type="int8")

    async def transcribe(self, audio_path: str) -> dict:
        self._load_model()
        if not audio_path or not Path(audio_path).exists():
            return {"text": "", "segments": []}

        segments_generator, info = self.model.transcribe(audio_path, word_timestamps=True)
        
        segments = []
        full_text = ""
        for segment in segments_generator:
            words = []
            if hasattr(segment, "words") and segment.words:
                for word in segment.words:
                    words.append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end
                    })
            seg_dict = {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "words": words
            }
            segments.append(seg_dict)
            full_text += segment.text + " "
            
        return {"text": full_text.strip(), "segments": segments}

    async def transcribe_file(self, video_path: str) -> dict:
        if not video_path or not Path(video_path).exists():
            return {"text": "", "segments": []}

        temp_audio = video_path + ".wav"
        try:
            cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", temp_audio]
            subprocess.run(cmd, check=True, capture_output=True)
            res = await self.transcribe(temp_audio)
            return res
        except Exception:
            return {"text": "", "segments": []}
        finally:
            if os.path.exists(temp_audio):
                try:
                    os.remove(temp_audio)
                except Exception:
                    pass

    def generate_srt(self, segments: list) -> str:
        def format_timestamp(seconds: float):
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            msecs = int((seconds - int(seconds)) * 1000)
            return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

        srt = ""
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment.get("start", 0))
            end = format_timestamp(segment.get("end", 0))
            srt += f"{i}\n{start} --> {end}\n{segment.get('text', '').strip()}\n\n"
        return srt

    def generate_ass(self, segments: list, style_preset: str = "default") -> str:
        # Styled ASS Subtitle Presets (Hormozi, Bold, Cinematic, Minimal)
        style_preset_clean = (style_preset or "default").lower()
        
        if style_preset_clean == "bold" or style_preset_clean == "hormozi":
            font_size = "72"
            primary_col = "&H0000FFFF"  # Yellow text
            outline_col = "&H00000000"
            margin_v = "120"
        elif style_preset_clean == "cinematic":
            font_size = "54"
            primary_col = "&H00FFFFFF"  # White text
            outline_col = "&H00000000"
            margin_v = "60"
        else:
            font_size = "64"
            primary_col = "&H00FFFFFF"
            outline_col = "&H00000000"
            margin_v = "90"

        ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,{font_size},{primary_col},&H000000FF,{outline_col},&H00000000,1,0,0,0,100,100,0,0,1,3,1,2,10,10,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        def format_timestamp(seconds: float):
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = seconds % 60
            return f"{hrs}:{mins:02d}:{secs:05.2f}"
            
        for segment in segments:
            start = format_timestamp(segment.get("start", 0))
            end = format_timestamp(segment.get("end", 0))
            text = segment.get("text", "").strip().replace("\n", " ")
            if text:
                ass += f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"
        return ass
