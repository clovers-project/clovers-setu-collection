import httpx
import json
from ..setu_api import SetuAPI


async def Lolicon(n: int, r18: int, tag: str):
    async with httpx.AsyncClient() as client:
        if tag:
            tag = f"&tag={tag}"
        resp = await client.get(f"https://api.lolicon.app/setu/v2?num={n}&r18={r18}{tag}&excludeAI=1")
    if resp.status_code != 200:
        return
    lolicon_list = json.loads("".join(x for x in resp.text if x.isprintable()))["data"]
    if not lolicon_list:
        return
    return [x["urls"]["original"] for x in lolicon_list]


Lolicon_api = SetuAPI(Lolicon, "Lolicon API")
