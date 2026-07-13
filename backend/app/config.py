"""Oasisic Muse 配置管理"""

from __future__ import annotations

import os
from pathlib import Path

DATA_DIR = Path(os.getenv("OASISIC_DATA", "/data"))
DB_PATH = DATA_DIR / "oasisic.db"


class Settings:
    """应用配置"""

    # 基础
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")

    # 数据库
    database_url: str = f"sqlite:///{DB_PATH}"

    # 下载器
    qb_host: str = os.getenv("QB_HOST", "")
    qb_port: int = int(os.getenv("QB_PORT", "8080"))
    qb_username: str = os.getenv("QB_USERNAME", "")
    qb_password: str = os.getenv("QB_PASSWORD", "")

    # 通知 - Telegram
    tg_bot_token: str = os.getenv("TG_BOT_TOKEN", "")
    tg_chat_id: str = os.getenv("TG_CHAT_ID", "")

    # 通知 - Discord
    discord_webhook: str = os.getenv("DISCORD_WEBHOOK_URL", "")

    # 媒体库
    emby_host: str = os.getenv("EMBY_HOST", "")
    emby_api_key: str = os.getenv("EMBY_API_KEY", "")

    # 代理
    proxy_url: str = os.getenv("PROXY_URL", "")

    # PT 站点
    pt_sites: str = os.getenv("PT_SITES", "")


settings = Settings()