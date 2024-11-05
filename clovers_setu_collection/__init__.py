import json
import time
from pathlib import Path
from clovers.core.plugin import Plugin, Event, Result
from clovers.utils.tools import to_int
from .setu_api import SetuAPI
from .api.Anosu import Anosu_api
from .api.MirlKoi import MirlKoi_api, MirlKoi_tags
from .api.Lolicon import Lolicon_api
from clovers.core.config import config as clovers_config
from .config import Config

config_key = __package__
config_data = Config.model_validate(clovers_config.get(config_key, {}))
clovers_config[config_key] = config_data.model_dump()

path = Path(config_data.path)
image_file = path / "image"
image_file.mkdir(parents=True, exist_ok=True)

customer_api_file = path / "CustomerAPI.json"
customer_api: dict[str, str]
if customer_api_file.exists():
    with open(customer_api_file, "r", encoding="utf8") as f:
        customer_api = json.load(f)
else:
    customer_api_file.parent.mkdir(parents=True, exist_ok=True)
    customer_api = {}


plugin = Plugin()


def to_me(event: Event):
    return event.kwargs["to_me"]


@plugin.handle(["涩图", "色图"], ["to_me"], rule=to_me)
async def _(event: Event):
    msg = (
        "发送【来一张xx涩图】可获得一张随机色图。"
        "图片取自：\n"
        "Jitsu：https://image.anosu.top/\n"
        "MirlKoi API：https://iw233.cn/\n"
        "Lolicon API：https://api.lolicon.app/"
    )
    return Result("text", msg)


public_setu_limit = config_data.public_setu_limit
public_setu_api = config_data.public_setu_api
private_setu_limit = config_data.private_setu_limit
private_setu_api = config_data.private_setu_api
save_image = config_data.save_image

if save_image:

    def translate_without_save(image_list: list[bytes]):
        return [Result("image", image) for image in image_list]

    translate = translate_without_save

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


def get_api(group_id: str, user_id: str, tag: str) -> SetuAPI:
    def choise_api(api_name: str, tag: str) -> SetuAPI:
        if api_name == "Lolicon API":
            return Lolicon_api
        else:
            if not tag or tag in MirlKoi_tags:
                return MirlKoi_api
            return Anosu_api

    if user_id in customer_api:
        api_name = customer_api[user_id]
    elif group_id:
        api_name = public_setu_api
    else:
        api_name = private_setu_api

    return choise_api(api_name, tag)


@plugin.handle(r"来(.*)[张份]([rR]18)?(.+)$", ["to_me", "Bot_Nickname", "group_id", "user_id"], rule=to_me)
async def _(event: Event):
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

    Bot_Nickname = event.kwargs["Bot_Nickname"]

    msg.append(f"{Bot_Nickname}为你准备了{n}张随机{tag}图片！")

    group_id = event.kwargs["group_id"]
    user_id = event.kwargs["user_id"]

    if r18:
        if group_id:
            if public_setu_limit:
                r18 = 0
                msg.append("(r18禁止)")
            else:
                r18 = 1
        else:
            if private_setu_limit:
                msg.append("(r18禁止)")
                r18 = 0
            else:
                r18 = 1
    else:
        r18 = 0

    api = get_api(group_id, user_id, tag)

    msg.append(f"使用api：{api.name}")
    start = time.time()
    image_list = await api.call(n, r18, tag, headers={"Referer": "http://www.weibo.com/"})
    msg.append(f"获取耗时：{round((time.time() - start)*1000,2)}ms")
    msg = "\n".join(msg)
    if not image_list:
        return Result("text", msg + "\n获取图片失败...")

    image_list = translate(image_list)

    if len(image_list) == 1:
        return Result("list", [Result("text", msg), image_list[0]])

    async def result():
        yield Result("text", msg)
        for image in image_list:
            yield image

    return Result("segmented", result())


api_names = ["Jitsu/MirlKoi API", "Lolicon API"]


@plugin.handle(["设置api", "切换api", "指定api"], ["to_me", "group_id", "user_id"], rule=to_me)
async def _(event: Event):
    user_id = event.kwargs["user_id"]

    @plugin.temp_handle(f"api{user_id}", ["user_id"], timeout=15, rule=lambda event: event.kwargs["user_id"] == user_id)
    async def _(event: Event, finish):
        finish()
        try:
            api = api_names[to_int(event.raw_command) - 1]
        except (TypeError, IndexError):
            return Result("text", "设置失败")
        customer_api[user_id] = api
        with open(customer_api_file, "w", encoding="utf8") as f:
            json.dump(customer_api, f, ensure_ascii=False, indent=4)
        return Result("text", f"已设置为：{api}")

    api_tip = "\n".join([f"{i}. {name}" for i, name in enumerate(api_names, 1)])
    return Result("text", f"请选择\n{api_tip}")


__plugin__ = plugin
