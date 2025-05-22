from pydantic import BaseModel
from pathlib import Path
from typing import TypedDict, Any


class HttpxConfig(TypedDict):
    """httpx配置"""

    LoliconAPI: dict[str, Any]
    MirlKoiAPI: dict[str, Any]
    AnosuAPI: dict[str, Any]


class Config(BaseModel):
    save_image: bool = False
    """是否保存从api获取的图片"""
    path: str = Path("./data/setu_collection").as_posix()
    """主路径"""
    private_setu_limit: bool = False
    """私聊图片限制"""
    private_setu_api: str = "Lolicon API"
    """私聊使用的图片api"""
    public_setu_limit: bool = True
    """群聊图片限制（别关）"""
    public_setu_api: str = "Jitsu/MirlKoi API"
    """群聊使用的图片api"""
    httpx_config: HttpxConfig = {
        "LoliconAPI": {},
        "MirlKoiAPI": {},
        "AnosuAPI": {},
    }
