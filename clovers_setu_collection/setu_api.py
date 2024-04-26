import asyncio
import httpx
import logging
from collections.abc import Callable, Coroutine

logger = logging.getLogger("setu_api")


class SetuAPI:
    def __init__(self, url_list: Callable[..., Coroutine], name: str = "undefined") -> None:
        self.url_list = url_list
        self.name = name

    async def call(self, n: int, r18: int, tag: str, **kwargs):
        url_list = await self.url_list(n, r18, tag)
        if not url_list:
            return

        async def task(client: httpx.AsyncClient, url: str, **kwargs):
            try:
                resp = await client.get(url, **kwargs)
            except httpx.TimeoutException:
                logger.warning(f"Timeout:{url}")
                return None
            if resp.status_code != 200:
                logger.warning(f"HTTP code {resp.status_code}:{url}")
                return None
            return resp.content

        async with httpx.AsyncClient() as client:
            task_list = [asyncio.create_task(task(client, url, **kwargs)) for url in url_list]
            return [image for image in await asyncio.gather(*task_list) if image]
