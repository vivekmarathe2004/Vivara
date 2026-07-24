from backend.config import Settings
from backend.services.tts.base import TTSProvider
from backend.services.tts.kokoro_tts import KokoroTTSProvider
from backend.services.tts.edge_tts_provider import EdgeTTSProvider
from backend.services.tts.gtts_provider import GTTSProvider
from backend.services.tts.elevenlabs_provider import ElevenLabsTTSProvider
from backend.services.tts.openai_tts import OpenAITTSProvider

class TTSNotAvailableError(Exception):
    pass

def get_tts_provider(settings: Settings) -> TTSProvider:
    provider_name = (settings.tts_provider or "kokoro").lower()
    
    if provider_name == "gtts":
        return GTTSProvider(lang=settings.gtts_lang)
    elif provider_name == "elevenlabs":
        return ElevenLabsTTSProvider(
            api_key=settings.elevenlabs_api_key,
            voice_id=settings.elevenlabs_voice_id
        )
    elif provider_name in ["openai", "openai_tts"]:
        return OpenAITTSProvider(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            voice=settings.openai_tts_voice,
            model=settings.openai_tts_model
        )
    elif provider_name == "kokoro":
        return KokoroTTSProvider()
    else:
        return EdgeTTSProvider()
