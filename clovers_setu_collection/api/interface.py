import asyncio
import httpx
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger("setu_api")


class SetuAPI(ABC):
    def __init__(self, **kwargs):
        self.client = httpx.AsyncClient(**kwargs)

    @abstractmethod
    async def api(self, n: int, r18: int, tag: str) -> list[str] | None: ...

    async def download(self, url: str, **kwargs):
        try:
            resp = await self.client.get(url, **kwargs)
        except httpx.TimeoutException:
            logger.warning(f"Timeout:{url}")
            return None
        if resp.status_code != 200:
            logger.warning(f"HTTP code {resp.status_code}:{url}")
            return None
        return resp.content

    async def call(self, n: int, r18: int, tag: str, **kwargs):
        urls = await self.api(n, r18, tag)
        if not urls:
            return
        task_list = [self.download(url, **kwargs) for url in urls]
        return [image for image in await asyncio.gather(*task_list) if image]
