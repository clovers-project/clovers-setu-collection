from pydantic import BaseModel
from pathlib import Path


class Config(BaseModel):
    save_image: bool = True
    """是否保存从api获取的图片"""
    path: str = str(Path("data/setu_collection"))
    """主路径"""
    private_setu_limit: bool = False
    """私聊图片限制"""
    public_setu_limit: bool = True
    """群聊图片限制（别关）"""
