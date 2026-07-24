import edge_tts
from backend.services.tts.base import TTSProvider

class EdgeTTSProvider(TTSProvider):
    async def synthesize(self, text: str, output_path: str, voice: str) -> dict:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return {"audio_path": output_path, "duration": 0.0, "word_timings": []}

    async def list_voices(self) -> list[dict]:
        voices = await edge_tts.list_voices()
        return [{"id": v["ShortName"], "name": v["FriendlyName"]} for v in voices]

    async def is_available(self) -> bool:
        return True
