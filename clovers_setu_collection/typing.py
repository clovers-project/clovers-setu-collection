from typing import Protocol
from collections.abc import Sequence


class PropertiesProtocol(Protocol):
    Bot_Nickname: str
    user_id: str
    group_id: str | None
    to_me: bool
    nickname: str
    avatar: str
    group_avatar: str | None
    image_list: list[str]
    permission: int
    at: list[str]


class Event(PropertiesProtocol, Protocol):
    """事件协议
    经过 EventBuilder 处理构建的返回值需要满足 EventProtocol 协议

    Attributes:
        message (str): 触发插件的消息原文
        args (Sequence[str]): 命令参数
        properties (dict): 插件声明的属性
    Methods:
        call(key: str, *args): 执行适配器调用方法并获取返回值
    """

    message: str
    args: Sequence[str]
    properties: dict

    def call(self, key: str, *args): ...
