"""通知 API — 测试推送"""

from __future__ import annotations

from fastapi import APIRouter

from ..config import settings
from ..services.notifier import NotifierService

router = APIRouter()
notifier = NotifierService()


@router.post("/notify/test")
async def test_notify():
    """发送测试通知到已配置的渠道"""
    results = await notifier.send(
        title="Oasisic Muse 测试通知",
        message="如果收到此消息，说明通知配置正常 ✅",
    )
    return results


@router.get("/notify/status")
async def notify_status():
    """通知渠道状态"""
    channels = []
    if settings.tg_bot_token and settings.tg_chat_id:
        channels.append({"name": "Telegram", "configured": True})
    if settings.discord_webhook:
        channels.append({"name": "Discord", "configured": True})
    if not channels:
        channels.append({"name": "未配置", "configured": False})
    return {"channels": channels}