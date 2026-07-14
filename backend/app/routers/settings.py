"""设置管理 API"""

from __future__ import annotations

from fastapi import APIRouter

from ..config import settings

router = APIRouter()


@router.get("/settings")
async def get_settings():
    """获取当前配置（脱敏）"""
    return {
        "qb_host": settings.qb_host or "未配置",
        "qb_port": settings.qb_port,
        "tg_bot_token": "已配置" if settings.tg_bot_token else "未配置",
        "tg_chat_id": "已配置" if settings.tg_chat_id else "未配置",
        "discord_webhook": "已配置" if settings.discord_webhook else "未配置",
        "emby_host": settings.emby_host or "未配置",
        "proxy_url": settings.proxy_url or "未配置",
        "pt_sites": settings.pt_sites or "未配置",
        "sites": [
            {"short": "MT", "name": "M-Team", "url": "https://kp.m-team.cc", "configured": bool(settings.pt_sites)},
            {"short": "RS", "name": "Rousi", "url": "https://rousi.pro", "configured": bool(settings.pt_sites)},
            {"short": "NPT", "name": "NicePT", "url": "https://www.nicept.net", "configured": bool(settings.pt_sites)},
            {"short": "PTT", "name": "PTTime", "url": "https://www.pttime.org", "configured": bool(settings.pt_sites)},
        ],
    }