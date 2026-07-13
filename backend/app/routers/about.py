"""关于页面 — 免责声明"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AboutResponse(BaseModel):
    title: str
    description: str
    disclaimer: str
    version: str


@router.get("/about", response_model=AboutResponse)
async def get_about():
    """获取项目信息与免责声明"""
    return AboutResponse(
        title="Oasisic Muse",
        description="AV 自动化刮削下载工具",
        disclaimer=(
            "本项目仅供内部交流学习使用，不得对外传播、转载或用于任何商业用途。"
            "所有资源来自网络，版权归原作者所有。"
            "使用者应对自己的行为负责，项目开发者不承担任何法律责任。"
        ),
        version="0.1.0",
    )