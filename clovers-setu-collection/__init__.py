import json
from pathlib import Path
from collections.abc import Callable
from clovers.core.plugin import Plugin, Event, Result
from clovers.utils.tools import to_int
from .setu_api import SetuAPI
from .api.Anosu import Anosu_api
from .api.MirlKoi import MirlKoi_api, MirlKoi_tags
from clovers.core.config import config as clovers_config
from .config import Config

config_key = __package__
config_data = Config.model_validate(clovers_config.get(config_key, {}))
clovers_config[config_key] = config_data.model_dump()
path = Path(config_data.path)
image_file = path / "image"
customer_api_file = path / "customer_api.json"
customer_api: dict[str, str]
if customer_api_file.exists():
    with open(customer_api_file, "r", encoding="utf8") as f:
        customer_api = json.load(f)
else:
    customer_api_file.parent.mkdir(parents=True, exist_ok=True)
    customer_api = {}


def save_customer_api():
    with open(customer_api_file, "w", encoding="utf8") as f:
        json.dump(customer_api, f, ensure_ascii=False, indent=4)


api_dict = {"1": "Jitsu/MirlKoi API", "2": "Lolicon API"}
plugin = Plugin()


@plugin.handle({"涩图，色图"}, ["to_me"])
async def _(event: Event):
    if not event.kwargs["to_me"]:
        return
    msg = (
        "发送【来一张xx涩图】可获得一张随机色图。"
        "群聊图片取自：\n"
        "Jitsu：https://image.anosu.top/\n"
        "MirlKoi API：https://iw233.cn/\n"
        "私聊图片取自：\n"
        "Lolicon API：https://api.lolicon.app/"
    )
    return Result("text", msg)


open_r18_in_private = config_data.open_r18_in_private
open_r18_in_public = config_data.open_r18_in_public
save_image = config_data.save_image
translate: Callable[[list[bytes]], list[Result]]
if save_image:
    translate = lambda image_list: [Result("image", image) for image in image_list]
else:

    def translate_with_save(image_list: list[bytes]):
        result: list[Result] = []
        for image in image_list:
            image_name = hex(hash(image))[2:] + ".png"
            with open(image_file / image_name, "wb") as f:
                f.write(image)
            result.append(Result("image", image))
        return result

    translate = translate_with_save


@plugin.handle(r"来(.*)[张份]([rR]18)?(.+)$", ["Bot_Nickname", "group_id", "user_id"])
async def _(event: Event):
    Bot_Nickname = event.kwargs["Bot_Nickname"]
    n, r18, tag = event.args
    if n:
        n = to_int(n)
        if n is None:
            return
    else:
        n = 1
    if tag[-2:] in {"色图", "涩图", "图片"}:
        tag = tag[:-2]
    msg = []
    if n > 5:
        n = 5
        msg.append("最多可以点5张图片哦")

    msg.append(f"{Bot_Nickname}为你准备了{n}张随机{tag}图片！")
    if r18:
        if event.kwargs["group_id"]:
            if open_r18_in_public:
                r18 = 1
            else:
                r18 = 0
                msg.append("(r18禁止)")
        else:
            if open_r18_in_private:
                r18 = 1
            else:
                r18 = 0
                msg.append("(r18禁止)")
    else:
        r18 = 0

    def choice_api(tag: str) -> SetuAPI:
        if not tag or tag in MirlKoi_tags:
            return MirlKoi_api
        return Anosu_api

    api = choice_api(tag)
    msg.append(f"使用api：{api.name}")
    msg = "\n".join(msg)
    image_list = await api.call(n, r18, tag, headers={"Referer": "http://www.weibo.com/"})
    if not image_list:
        return Result("text", msg + "\n连接失败，请稍后重试。")
    if save_image:
        for image in image_list:
            image_name = hex(hash(image))[2:] + ".png"
            with open(image_file / image_name, "wb") as f:
                f.write(image)

    image_list = translate(image_list)
    if len(image_list) == 1:
        return Result("list", [Result("text", msg), image_list[0]])

    async def result():
        yield Result("text", msg)
        for image in image_list:
            yield image

    return Result("segmented", result())


api_tip = "\n".join(f"{k}.{v}" for k, v in api_dict.items())


@plugin.handle({"设置api", "切换api", "指定api"}, ["group_id", "user_id"])
async def _(event: Event):
    if event.kwargs["group_id"]:
        return
    user_id = event.kwargs["user_id"]

    @plugin.temp_handle(f"api{user_id}", ["user_id"], timeout=15)
    async def _(event: Event, finish):
        if event.kwargs["user_id"] != user_id:
            return
        finish()
        api = event.raw_command
        if api not in api_dict:
            return "设置失败"
        customer_api[user_id] = event.raw_command
        save_customer_api()
        return f"已设置为：{api_dict[event.raw_command]}"

    return f"请选择\n{api_tip}"


__plugin__ = plugin
