import httpx
import json
from ..setu_api import SetuAPI


async def Anosu(n: int, r18: int, tag: str):
    async with httpx.AsyncClient() as client:
        param = []
        if n > 1:
            param.append(f"num={n}")
        if r18 == 1:
            param.append(f"r18={r18}")
        if tag:
            param.append(f"keyword={tag}")
        resp = await client.get(f"https://image.anosu.top/pixiv/json?{'&'.join(param)}")
    if resp.status_code != 200:
        return
    anosu_list = json.loads("".join(x for x in resp.text if x.isprintable()))
    if not anosu_list:
        return
    return [x["url"] for x in anosu_list]


Anosu_api = SetuAPI(Anosu, "Anosu")
