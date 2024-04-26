import httpx
import json
from ..setu_api import SetuAPI


async def Anosu(n, r18, tag):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://image.anosu.top/pixiv/json?num={n}&r18={r18}&keyword={tag}")
    if resp.status_code != 200:
        return
    anosu_list = json.loads("".join(x for x in resp.text if x.isprintable()))
    if not anosu_list:
        return
    return [x["url"] for x in anosu_list]


anosu_api = SetuAPI(Anosu)
