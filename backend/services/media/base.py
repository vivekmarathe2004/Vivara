from abc import ABC, abstractmethod

class MediaProvider(ABC):
    @abstractmethod
    async def search_videos(self, query: str, per_page: int = 10) -> list[dict]:
        pass

    @abstractmethod
    async def search_images(self, query: str, per_page: int = 10) -> list[dict]:
        pass

    @abstractmethod
    async def download(self, url: str, output_path: str) -> str:
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        pass
