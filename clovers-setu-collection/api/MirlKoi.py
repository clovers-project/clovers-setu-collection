import httpx
import json
from ..setu_api import SetuAPI

MirlKoi_tags: set[str] = set()
tags_sort: dict[str, str] = {
    "涩图 随机图片 随机壁纸": "iw233",
    "推荐": "top",
    "白毛 白发 银发": "yin",
    "兽耳 猫耳 猫娘": "cat",
    "星空 夜空 星空壁纸 夜空壁纸": "xing",
    "壁纸 竖屏壁纸 手机壁纸": "mp",
    "电脑壁纸 横屏壁纸": "pc",
}
sort_dict: dict[str, str] = {}
url_cache: dict[str, list[str]] = {}
for k, v in tags_sort.items():
    url_cache[v] = []
    for tag in k.split():
        sort_dict[tag] = k
        MirlKoi_tags.add(tag)


async def MirlKoi(n: int, r18: int, tag: str):
    tag = sort_dict.get(tag, "iw233")
    if len(url_cache[tag]) < n:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://dev.iw233.cn/api.php?sort={tag}&type=json&num=100",
                headers={"Referer": "http://www.weibo.com/"},
            )
        if resp.status_code != 200:
            return
        url_cache[tag].extend(json.loads("".join(x for x in resp if x.isprintable()))["pic"])
    url_list = url_cache[tag][:n]
    url_cache[tag] = url_cache[tag][n:]
    return url_list


MirlKoi_api = SetuAPI(MirlKoi, "MirlKoi")
