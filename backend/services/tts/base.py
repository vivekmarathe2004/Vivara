from abc import ABC, abstractmethod

class TTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, output_path: str, voice: str) -> dict:
        pass

    @abstractmethod
    async def list_voices(self) -> list[dict]:
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        pass
