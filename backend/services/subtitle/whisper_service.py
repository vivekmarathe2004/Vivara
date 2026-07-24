from faster_whisper import WhisperModel
import os
import subprocess

class WhisperService:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None

    def _load_model(self):
        if self.model is None:
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")

    async def transcribe(self, audio_path: str) -> dict:
        self._load_model()
        segments_generator, info = self.model.transcribe(audio_path, word_timestamps=True)
        
        segments = []
        full_text = ""
        for segment in segments_generator:
            words = []
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
        temp_audio = video_path + ".wav"
        try:
            subprocess.run(["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", temp_audio], check=True, capture_output=True)
            res = await self.transcribe(temp_audio)
            return res
        finally:
            if os.path.exists(temp_audio):
                os.remove(temp_audio)

    def generate_srt(self, segments: list) -> str:
        def format_timestamp(seconds: float):
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            msecs = int((seconds - int(seconds)) * 1000)
            return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

        srt = ""
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            srt += f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n\n"
        return srt

    def generate_ass(self, segments: list, style_preset: str = "default") -> str:
        # Simplistic ASS template
        ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,60,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,3,1,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        def format_timestamp(seconds: float):
            hrs = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            secs = seconds % 60
            return f"{hrs}:{mins:02d}:{secs:05.2f}"
            
        for segment in segments:
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment['text'].strip().replace("\n", " ")
            ass += f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n"
        return ass
