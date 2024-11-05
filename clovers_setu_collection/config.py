from pydantic import BaseModel
from pathlib import Path


class Config(BaseModel):
    save_image: bool = True
    """是否保存从api获取的图片"""
    path: str = str(Path("data/setu_collection"))
    """主路径"""
    private_setu_limit: bool = False
    """私聊图片限制"""
    private_setu_api: str = "Lolicon API"
    """私聊使用的图片api"""
    public_setu_limit: bool = True
    """群聊图片限制（别关）"""
    public_setu_api: str = "Jitsu/MirlKoi API"
    """群聊使用的图片api"""
