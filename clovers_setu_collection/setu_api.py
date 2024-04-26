import asyncio
import httpx
from collections.abc import Callable, Coroutine


class SetuAPI:
    def __init__(self, url_list: Callable[..., Coroutine]) -> None:
        self.url_list = url_list

    async def call(self, n: int | str, r18: int | str, tag: str, **kwargs):
        url_list = await self.url_list(n, r18, tag)

        async def task(client: httpx.AsyncClient, url: str, **kwargs):
            try:
                resp = await client.get(url, **kwargs)
            except httpx.TimeoutException:
                return None
            if resp.status_code != 200:
                return None
            return resp.content

        async with httpx.AsyncClient() as client:
            task_list = [asyncio.create_task(task(client, url, **kwargs)) for url in url_list]
        return [image for image in await asyncio.gather(*task_list) if image]
