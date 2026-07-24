from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM
    llm_provider: str = "omniroute"  # omniroute, auto, ollama, openai_compat, lm_studio, vllm, openrouter, custom
    llm_base_url: str = "http://localhost:7777/v1"  # OmniRoute / Ollama default
    llm_api_key: str = ""
    llm_model: str = "llama3.2"
    
    # TTS Engines
    tts_provider: str = "kokoro"  # kokoro, edge_tts, elevenlabs, gtts, openai_tts
    tts_voice: str = "af_heart"   # Kokoro voice
    edge_tts_voice: str = "en-US-JennyNeural"
    gtts_lang: str = "en"
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # Rachel (default)
    openai_tts_voice: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    openai_tts_model: str = "tts-1"
    
    # Media APIs (All Optional / Free Tiers)
    pexels_api_key: str = ""
    pixabay_api_key: str = ""
    unsplash_api_key: str = ""
    
    # Paths
    storage_dir: str = "../storage"
    ffmpeg_path: str = "ffmpeg"
    
    # Features
    gpu_enabled: bool = True
    whisper_model: str = "base"  # tiny, base, small, medium
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
