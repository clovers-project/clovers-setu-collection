from pydantic import BaseModel
from pathlib import Path


class Config(BaseModel):
    save_image: bool = False
    """是否保存从api获取的图片"""
    data_path: str = str(Path("data/setu_collection"))
    """主路径"""
    open_r18_in_private: bool = True
    """私聊开启r18"""
    open_r18_in_public: bool = False
    """群聊开启r18（别开）"""
