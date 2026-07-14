"""Oasisic Muse 配置管理

配置优先级: 持久化配置（Web设置） > 环境变量 > 默认值
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

DATA_DIR = Path(os.getenv("OASISIC_DATA", "/data"))
DB_PATH = DATA_DIR / "oasisic.db"

# 延迟导入，避免循环依赖
_config_store: Any = None


def _get_store():
    global _config_store
    if _config_store is None:
        from .services.config_store import SettingsStore
        _config_store = SettingsStore(str(DATA_DIR))
    return _config_store


class Settings:
    """应用配置 — 按优先级读取"""

    @property
    def debug(self) -> bool:
        return os.getenv("DEBUG", "false").lower() == "true"

    @property
    def host(self) -> str:
        return os.getenv("HOST", "0.0.0.0")

    @property
    def port(self) -> int:
        return int(os.getenv("PORT", "8000"))

    @property
    def database_url(self) -> str:
        return f"sqlite:///{DB_PATH}"

    # qBittorrent
    @property
    def qb_host(self) -> str:
        return _get_store().get("qb_host") or os.getenv("QB_HOST", "")

    @property
    def qb_port(self) -> int:
        return int(_get_store().get("qb_port") or os.getenv("QB_PORT", "8080"))

    @property
    def qb_username(self) -> str:
        return _get_store().get("qb_username") or os.getenv("QB_USERNAME", "")

    @property
    def qb_password(self) -> str:
        return _get_store().get("qb_password") or os.getenv("QB_PASSWORD", "")

    # Telegram
    @property
    def tg_bot_token(self) -> str:
        return _get_store().get("tg_bot_token") or os.getenv("TG_BOT_TOKEN", "")

    @property
    def tg_chat_id(self) -> str:
        return _get_store().get("tg_chat_id") or os.getenv("TG_CHAT_ID", "")

    # Discord
    @property
    def discord_webhook(self) -> str:
        return _get_store().get("discord_webhook") or os.getenv("DISCORD_WEBHOOK_URL", "")

    # Jellyfin/EMBY
    @property
    def emby_host(self) -> str:
        return _get_store().get("emby_host") or os.getenv("EMBY_HOST", "")

    @property
    def emby_api_key(self) -> str:
        return _get_store().get("emby_api_key") or os.getenv("EMBY_API_KEY", "")

    # 代理
    @property
    def proxy_url(self) -> str:
        return _get_store().get("proxy_url") or os.getenv("PROXY_URL", "")

    # PT 站点（仅环境变量占位，实际走 pt_sites.json）
    @property
    def pt_sites(self) -> str:
        return os.getenv("PT_SITES", "")


settings = Settings()