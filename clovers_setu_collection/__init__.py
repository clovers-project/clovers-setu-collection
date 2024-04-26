from clovers.core.plugin import Plugin, Event, Result
from clovers.utils.tools import to_int, download_url
from .setu_api import SetuAPI
from .api.Anosu import anosu_api

plugin = Plugin()


@plugin.handle({"涩图，色图"}, ["to_me"])
async def _(event: Event):
    if not event.kwargs["to_me"]:
        return
    msg = (
        "发送【我要一张xx涩图】可获得一张随机色图。"
        "群聊图片取自：\n"
        "Jitsu：https://image.anosu.top/\n"
        "MirlKoi API：https://iw233.cn/\n"
        "私聊图片取自：\n"
        "Lolicon API：https://api.lolicon.app/"
    )
    return Result("text", msg)


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

    def choice_api(tag: str) -> SetuAPI:
        return anosu_api
        # if not tag or (tag := is_MirlKoi_tag(tag)):
        #     api = "MirlKoi API"
        #     setufunc = MirlKoi
        # else:
        #     api = "Jitsu"
        #     setufunc = Anosu
        # pass

    if event.kwargs["group_id"]:
        if r18:
            msg.append("(r18禁止)")
    else:
        if r18:
            r18 = 1
    api = choice_api(tag)
    image_list = await api.call(n, r18, tag, headers={"Referer": "http://www.weibo.com/"})
    if image_list is None:
        msg.append("连接失败，请稍等一年后重试。")
        return Result("text", "\n".join(msg))
    if len(image_list) == 1:
        return Result("list", [Result("text", "\n".join(msg)), image_list[0]])

    async def result():
        yield Result("text", "\n".join(msg))
        for image in image_list:
            yield image

    return Result("segmented", result())


__plugin__ = plugin
