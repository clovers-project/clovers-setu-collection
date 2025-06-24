import json
import time
from pathlib import Path
from clovers import Plugin, EventProtocol, Result, TempHandle
from typing import Protocol
from clovers.config import Config as CloversConfig
from .config import Config
from .api.interface import SetuAPI
from .api import *


config_data = CloversConfig.environ().setdefault(__package__, {})
__config__ = Config.model_validate(config_data)
config_data.update(__config__.model_dump())


path = Path(__config__.path)
image_file = path / "image"
customer_api_file = path / "CustomerAPI.json"


save_image = __config__.save_image
httpx_config = __config__.httpx_config

if save_image:
    image_file.mkdir(parents=True, exist_ok=True)

    def translate(image_list: list[bytes]):
        result: list[Result] = []
        for image in image_list:
            image_name = hex(hash(image))[2:] + ".png"
            (image_file / image_name).write_bytes(image)
            result.append(Result("image", image))
        return result

else:

    def translate(image_list: list[bytes]):
        return [Result("image", image) for image in image_list]


customer_api: dict[str, str]


if customer_api_file.exists():
    customer_api = json.loads(customer_api_file.read_text())
else:
    path.mkdir(parents=True, exist_ok=True)
    customer_api = {}


class Event(EventProtocol, Protocol):
    Bot_Nickname: str
    user_id: str
    group_id: str | None
    to_me: bool


type Rule = Plugin.Rule.Checker[Event]


plugin = Plugin()
plugin.set_protocol("properties", Event)

to_me: Rule = lambda event: event.to_me

lolicon = LoliconAPI(**httpx_config.get("LoliconAPI", {}))
anosu = AnosuAPI(**httpx_config.get("AnosuAPI", {}))
# mirlkoi = MirlKoiAPI(**httpx_config.get("MirlKoiAPI", {}))


@plugin.shutdown
async def _():
    global lolicon, anosu
    await lolicon.client.aclose()
    await anosu.client.aclose()


public_setu_api: SetuAPI
private_setu_api: SetuAPI


def match_api(name: str) -> SetuAPI:
    match name:
        case "Lolicon API":
            return lolicon
        case "Anosu API":
            return anosu
        case _:
            global public_setu_api
            return public_setu_api


public_setu_api = match_api(__config__.public_setu_api)
private_setu_api = match_api(__config__.private_setu_api)


public_setu_limit = int(__config__.public_setu_limit)
private_setu_limit = int(__config__.private_setu_limit)


zh_number = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def to_int(N) -> int | None:
    try:
        result = int(N)
    except ValueError:
        result = zh_number.get(N)
    return result


async def segmented_result(msg: str, image_list: list[Result]):
    yield Result("text", msg)
    for image in image_list:
        yield image


@plugin.handle(r"来(.*)[张份]([rR]18)?(.+)$", ["to_me", "Bot_Nickname", "group_id", "user_id"], rule=to_me)
async def _(event: Event):
    n, r18, tag = event.args
    if not n:
        n = 1
    else:
        n = to_int(n)
        if not n:
            return
    msg = []
    if n > 5:
        n = 5
        msg.append("最多可以点5张图片哦")
    if tag.endswith(("色图", "涩图", "图片")):
        tag = tag[:-2]
    msg.append(f"{event.Bot_Nickname}为你准备了{n}张随机{tag}图片！")
    group_id = event.group_id
    user_id = event.user_id

    if r18:
        r18 = public_setu_limit if group_id else private_setu_limit
        if r18 == 0:
            msg.append("(r18禁止)")
    else:
        r18 = 0
    if user_id in customer_api:
        api = match_api(customer_api[user_id])
    elif group_id:
        api = public_setu_api
    else:
        api = private_setu_api

    msg.append(f"使用api：{api.name}")
    start = time.time()
    image_list = await api.call(n, r18, tag)
    msg.append(f"获取耗时：{(time.time() - start) :.2f}s")
    msg = "\n".join(msg)
    if not image_list:
        return Result("text", msg + "\n获取图片失败...")
    image_list = translate(image_list)
    if len(image_list) == 1:
        return Result("list", [Result("text", msg), image_list[0]])
    return Result("segmented", segmented_result(msg, image_list))


api_names = ["Anosu API", "Lolicon API"]


async def set_api(event: Event, handle: TempHandle):
    handle.finish()
    index = to_int(event.message)
    if index is None:
        return Result("text", "设置失败")
    try:
        api = api_names[index - 1]
    except (TypeError, IndexError):
        return Result("text", "设置失败")
    customer_api[event.user_id] = api
    customer_api_file.write_text(json.dumps(customer_api, ensure_ascii=False, indent=4), encoding="utf8")
    return Result("text", f"已设置为：{api}")


@plugin.handle(["设置api", "切换api", "指定api"], ["to_me", "user_id"], rule=to_me)
async def _(event: Event):
    rule: Rule = lambda e: e.user_id == event.user_id
    plugin.temp_handle(["user_id"], 15, rule=rule)(set_api)
    api_tip = "\n".join([f"{i}. {name}" for i, name in enumerate(api_names, 1)])
    return Result("text", f"请选择\n{api_tip}")


@plugin.handle(["涩图", "色图"], ["to_me"], rule=to_me)
async def _(event: Event):
    msg = (
        "发送【来一张xx涩图】可获得一张随机色图。"
        "图片取自：\n"
        "Anosu API：https://image.anosu.top/\n"
        # "MirlKoi API：https://iw233.cn/\n"
        "Lolicon API：https://api.lolicon.app/"
    )
    return Result("text", msg)


__plugin__ = plugin
