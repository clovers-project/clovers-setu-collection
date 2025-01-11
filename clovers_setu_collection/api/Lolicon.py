import json
from .interface import SetuAPI


class API(SetuAPI):
    name = "Lolicon API"

    async def api(self, n: int, r18: int, tag: str):
        if tag:
            tag = f"&tag={tag}"
        resp = await self.client.get(f"https://api.lolicon.app/setu/v2?num={n}&r18={r18}{tag}&excludeAI=1")
        if resp.status_code != 200:
            return
        lolicon_list = json.loads("".join(x for x in resp.text if x.isprintable()))["data"]
        if not lolicon_list:
            return
        return [x["urls"]["original"] for x in lolicon_list]
