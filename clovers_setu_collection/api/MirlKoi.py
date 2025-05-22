import json
from .interface import SetuAPI


class API(SetuAPI):
    name = "MirlKoi API"
    url_cache: dict[str, list[str]]
    tags: dict[str, tuple[str, ...]] = {
        "iw233": ("涩图", "随机图片", "随机壁纸"),
        "top": ("推荐",),
        "yin": ("白毛", "白发", "银发"),
        "cat": ("兽耳", "猫耳", "猫娘"),
        "xing": ("星空", "夜空", "星空壁纸", "夜空壁纸"),
        "mp": ("壁纸", "竖屏壁纸", "手机壁纸"),
        "pc": ("电脑壁纸", "横屏壁纸"),
    }
    NAME_ALIAS = {v: k for k, vs in tags.items() for v in vs}

    def __init__(self):
        super().__init__()
        self.url_cache = {}
        for tag in self.tags:
            self.url_cache[tag] = []

    async def api(self, n: int, r18: int, tag: str):
        tag = API.NAME_ALIAS.get(tag, "iw233")
        if len(self.url_cache[tag]) < n:
            resp = await self.client.get(
                f"https://dev.iw233.cn/api.php?sort={tag}&type=json&num=100",
                headers={"Referer": "http://www.weibo.com/"},
            )
            if resp.status_code != 200:
                return
            self.url_cache[tag].extend(json.loads("".join(x for x in resp.text if x.isprintable()))["pic"])
        url_list = self.url_cache[tag][:n]
        self.url_cache[tag] = self.url_cache[tag][n:]
        return url_list
