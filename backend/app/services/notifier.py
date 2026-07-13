"""通知服务 — Telegram + Discord"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from ..config import settings

logger = logging.getLogger(__name__)


class NotifierService:
    """多渠道通知推送"""

    async def send(self, title: str, message: str, level: str = "info") -> list[dict[str, Any]]:
        """发送通知到所有已配置的渠道"""
        results = []

        if settings.tg_bot_token and settings.tg_chat_id:
            result = await self._send_telegram(title, message, level)
            results.append({"channel": "telegram", **result})

        if settings.discord_webhook:
            result = await self._send_discord(title, message, level)
            results.append({"channel": "discord", **result})

        return results

    async def _send_telegram(self, title: str, message: str, level: str) -> dict:
        """发送 Telegram 通知"""
        emoji = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
        text = f"{emoji.get(level, 'ℹ️')} <b>{title}</b>\n\n{message}"

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                url = f"https://api.telegram.org/bot{settings.tg_bot_token}/sendMessage"
                resp = await client.post(url, json={
                    "chat_id": settings.tg_chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                })
                resp.raise_for_status()
                return {"success": True}
        except Exception as e:
            logger.error("Telegram 通知失败: %s", e)
            return {"success": False, "error": str(e)}

    async def _send_discord(self, title: str, message: str, level: str) -> dict:
        """发送 Discord 通知"""
        colors = {"info": 5814783, "success": 5763719, "warning": 16766720, "error": 15548997}

        embed = {
            "title": title,
            "description": message,
            "color": colors.get(level, 5814783),
            "timestamp": "2026-01-01T00:00:00Z",
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(settings.discord_webhook, json={"embeds": [embed]})
                resp.raise_for_status()
                return {"success": True}
        except Exception as e:
            logger.error("Discord 通知失败: %s", e)
            return {"success": False, "error": str(e)}