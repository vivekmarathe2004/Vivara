from fastapi import APIRouter
from backend.config import settings
from typing import Dict, Any
import os

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/")
def get_settings():
    safe_settings = settings.model_dump()
    for key in ["llm_api_key", "pexels_api_key", "pixabay_api_key", "unsplash_api_key", "elevenlabs_api_key"]:
        if safe_settings.get(key):
            safe_settings[key] = "***"
    return safe_settings

@router.put("/")
@router.post("/")
def update_settings(new_settings: Dict[str, Any]):
    env_lines = []
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            env_lines = f.readlines()
            
    updated_keys = set()
    new_lines = []
    for line in env_lines:
        if "=" in line:
            key, _ = line.split("=", 1)
            key_strip = key.strip()
            if key_strip.lower() in new_settings:
                val = str(new_settings[key_strip.lower()]).replace("\n", "").replace("\r", "")
                if val != "***":
                    new_lines.append(f"{key_strip}={val}\n")
                    if hasattr(settings, key_strip.lower()):
                        setattr(settings, key_strip.lower(), val)
                else:
                    new_lines.append(line)
                updated_keys.add(key_strip.lower())
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    for k, v in new_settings.items():
        if k not in updated_keys and v != "***":
            clean_v = str(v).replace("\n", "").replace("\r", "")
            new_lines.append(f"{k.upper()}={clean_v}\n")
            if hasattr(settings, k.lower()):
                setattr(settings, k.lower(), clean_v)
            
    with open(".env", "w") as f:
        f.writelines(new_lines)
        
    return settings.model_dump()

@router.get("/providers")
def list_providers():
    return [
        {"id": "omniroute", "name": "OmniRoute AI Gateway (Recommended)"},
        {"id": "auto", "name": "Auto (Smart routing)"},
        {"id": "ollama", "name": "Ollama (Local)"},
        {"id": "openai_compat", "name": "OpenAI Compatible"},
        {"id": "lm_studio", "name": "LM Studio"},
        {"id": "vllm", "name": "vLLM"},
        {"id": "openrouter", "name": "OpenRouter"},
        {"id": "custom", "name": "Custom Endpoint"}
    ]

@router.get("/tts-engines")
def list_tts_engines():
    return [
        {"id": "kokoro", "name": "Kokoro-82M (100% Free, Offline — Recommended)"},
        {"id": "edge_tts", "name": "Edge-TTS (100% Free, Microsoft Neural Voices)"},
        {"id": "gtts", "name": "Google Translate TTS (100% Free, 100+ Languages, No Key)"},
        {"id": "elevenlabs", "name": "ElevenLabs (Free API Key: 10,000 Chars/Mo)"},
        {"id": "openai_tts", "name": "OpenAI Speech API (Alloy, Echo, Fable, Onyx, Nova, Shimmer)"},
    ]

@router.get("/media-providers")
def list_media_providers():
    return [
        {"id": "pexels", "name": "Pexels (Free API Key, 200 Req/Hr)", "free_key_url": "https://www.pexels.com/api/"},
        {"id": "pixabay", "name": "Pixabay (Free API Key)", "free_key_url": "https://pixabay.com/api/docs/"},
        {"id": "unsplash", "name": "Unsplash Photos (Free API Key, 50 Req/Hr)", "free_key_url": "https://unsplash.com/developers"},
        {"id": "openverse", "name": "Openverse / Wikimedia (100% Free, No Key Required!)", "free_key_url": None},
    ]

@router.get("/voices")
def list_voices():
    prov = (settings.tts_provider or "kokoro").lower()
    if prov == "kokoro":
        return [
            {"id": "af_heart", "name": "Heart (Female, Natural)"},
            {"id": "af_bella", "name": "Bella (Female, Energetic)"},
            {"id": "af_nicole", "name": "Nicole (Female, Soft)"},
            {"id": "am_michael", "name": "Michael (Male, Professional)"},
            {"id": "am_adam", "name": "Adam (Male, Deep)"},
        ]
    elif prov == "gtts":
        return [
            {"id": "en", "name": "English (Google Voice)"},
            {"id": "es", "name": "Spanish (Google Voice)"},
            {"id": "fr", "name": "French (Google Voice)"},
            {"id": "de", "name": "German (Google Voice)"},
            {"id": "hi", "name": "Hindi (Google Voice)"},
            {"id": "ja", "name": "Japanese (Google Voice)"},
            {"id": "pt", "name": "Portuguese (Google Voice)"},
            {"id": "zh-CN", "name": "Chinese Mandarin (Google Voice)"},
        ]
    elif prov == "elevenlabs":
        return [
            {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel (Female, Warm)"},
            {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi (Female, Strong)"},
            {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella (Female, Expressive)"},
            {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni (Male, Deep)"},
            {"id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh (Male, Casual)"},
        ]
    elif prov in ["openai", "openai_tts"]:
        return [
            {"id": "alloy", "name": "Alloy (Neutral, Versatile)"},
            {"id": "echo", "name": "Echo (Male, Warm)"},
            {"id": "fable", "name": "Fable (British, Expressive)"},
            {"id": "onyx", "name": "Onyx (Male, Deep)"},
            {"id": "nova", "name": "Nova (Female, Energetic)"},
            {"id": "shimmer", "name": "Shimmer (Female, Clear)"},
        ]
    else:
        return [
            {"id": "en-US-JennyNeural", "name": "Jenny (Female, US)"},
            {"id": "en-US-GuyNeural", "name": "Guy (Male, US)"},
            {"id": "en-GB-SoniaNeural", "name": "Sonia (Female, UK)"},
            {"id": "en-AU-NatashaNeural", "name": "Natasha (Female, AU)"},
        ]
