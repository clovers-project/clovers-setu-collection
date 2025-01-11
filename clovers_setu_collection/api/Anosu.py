import json
from .interface import SetuAPI


class API(SetuAPI):
    name = "Anosu API"

    async def api(self, n: int, r18: int, tag: str):
        param = []
        if n > 1:
            param.append(f"num={n}")
        if r18 == 1:
            param.append(f"r18={r18}")
        if tag:
            param.append(f"keyword={tag}")
        resp = await self.client.get(f"https://image.anosu.top/pixiv/json?{'&'.join(param)}")
        if resp.status_code != 200:
            return
        anosu_list = json.loads("".join(x for x in resp.text if x.isprintable()))
        if not anosu_list:
            return
        return [x["url"] for x in anosu_list]
