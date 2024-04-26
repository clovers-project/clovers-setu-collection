from clovers.core.plugin import Plugin, Event, Result
from clovers.utils.tools import to_int, download_url
from .setu_api import SetuAPI
from .api.Anosu import Anosu_api
from .api.MirlKoi import MirlKoi_api, MirlKoi_tags
from clovers.core.config import config as clovers_config
from .config import Config

config_key = __package__
config_data = Config.model_validate(clovers_config.get(config_key, {}))
clovers_config[config_key] = config_data.model_dump()

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
        return Result("text", msg + "\n连接失败，请稍等一年后重试。")
    image_list = [Result("image", image) for image in image_list]
    if len(image_list) == 1:
        return Result("list", [Result("text", msg), image_list[0]])

    async def result():
        yield Result("text", msg)
        for image in image_list:
            yield image

    return Result("segmented", result())


@plugin.handle({"设置api", "切换api", "指定api"}, ["group_id", "user_id"])
async def _(event: Event):
    if event.kwargs["group_id"]:
        return
    user_id = event.kwargs["user_id"]

    @plugin.temp_handle(f"api{user_id}", ["user_id"])
    async def _(event: Event):
        if event.kwargs["user_id"] != user_id:
            return

    return "请选择\n1.Jitsu/MirlKoi API\n2.Lolicon API"

    def save():
        with open(file, "w", encoding="utf8") as f:
            json.dump(customer_api, f, ensure_ascii=False, indent=4)

    if api == "1":
        customer_api[user_id] = "Jitsu/MirlKoi API"
        save()
        await set_api.finish("api已切换为Jitsu/MirlKoi API")
    elif api == "2":
        customer_api[user_id] = "Lolicon API"
        save()
        await set_api.finish("api已切换为Lolicon API")
    else:
        await set_api.finish("api设置失败")


__plugin__ = plugin
