"""设置管理 API — 全部 web 可配置"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from ..config import settings
from ..services.config_store import store

logger = logging.getLogger(__name__)

router = APIRouter()

PT_CONFIG_PATH = Path(settings.database_url.replace("sqlite:///", "")).parent / "pt_sites.json"


def _load_pt_config() -> dict:
    if PT_CONFIG_PATH.exists():
        try:
            return json.loads(PT_CONFIG_PATH.read_text())
        except Exception:
            return {}
    return {}


def _save_pt_config(config: dict):
    PT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    PT_CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False))


def _mask(value: str) -> str:
    """脱敏显示"""
    if not value:
        return "未配置"
    if len(value) < 8:
        return "已配置"
    return value[:4] + "****" + value[-4:]


@router.get("/settings")
async def get_settings():
    """获取全部配置（脱敏）"""
    pt = _load_pt_config()
    all_ = store.get_all()

    return {
        # PT 站点
        "pt_sites": [
            {
                "short": "MT", "name": "M-Team", "url": "https://kp.m-team.cc",
                "auth_type": "cookie",
                "cookie_configured": bool(pt.get("MT", {}).get("cookie", "")),
            },
            {
                "short": "RS", "name": "Rousi", "url": "https://rousi.pro",
                "auth_type": "cookie+passkey",
                "cookie_configured": bool(pt.get("RS", {}).get("cookie", "")),
            },
            {
                "short": "NPT", "name": "NicePT", "url": "https://www.nicept.net",
                "auth_type": "cookie+passkey",
                "cookie_configured": bool(pt.get("NPT", {}).get("cookie", "")),
            },
            {
                "short": "PTT", "name": "PTTime", "url": "https://www.pttime.org",
                "auth_type": "cookie+passkey",
                "cookie_configured": bool(pt.get("PTT", {}).get("cookie", "")),
            },
        ],
        # 下载器
        "qb_host": all_.get("qb_host", "未配置"),
        "qb_port": all_.get("qb_port", "8080"),
        "qb_user": _mask(all_.get("qb_username", "")),
        "qb_configured": bool(all_.get("qb_host")),
        # 通知
        "tg_configured": bool(all_.get("tg_bot_token") and all_.get("tg_chat_id")),
        "tg_bot": _mask(all_.get("tg_bot_token", "")),
        "discord_configured": bool(all_.get("discord_webhook")),
        "discord_url": _mask(all_.get("discord_webhook", "")),
        # 媒体库
        "emby_host": all_.get("emby_host", "未配置"),
        "emby_configured": bool(all_.get("emby_host")),
        # 代理
        "proxy_url": all_.get("proxy_url", "未配置"),
        "proxy_configured": bool(all_.get("proxy_url")),
    }


class PTSiteAuth(BaseModel):
    cookie: str = ""
    passkey: str = ""


class PTSitesConfig(BaseModel):
    sites: dict[str, PTSiteAuth]


@router.post("/settings/pt-sites")
async def save_pt_sites(config: PTSitesConfig):
    """保存 PT 站点认证"""
    current = _load_pt_config()
    for short, auth in config.sites.items():
        if short not in current:
            current[short] = {}
        if auth.cookie:
            current[short]["cookie"] = auth.cookie
        if auth.passkey:
            current[short]["passkey"] = auth.passkey
    _save_pt_config(current)
    return {"saved": True, "sites": list(config.sites.keys())}


@router.get("/settings/pt-sites")
async def get_pt_sites_config():
    """获取 PT 站点配置状态"""
    config = _load_pt_config()
    return {
        short: {
            "cookie_configured": bool(data.get("cookie", "")),
            "passkey_configured": bool(data.get("passkey", "")),
        }
        for short, data in config.items()
    }


class GlobalConfig(BaseModel):
    """全局配置"""
    qb_host: str = ""
    qb_port: str = "8080"
    qb_username: str = ""
    qb_password: str = ""
    tg_bot_token: str = ""
    tg_chat_id: str = ""
    discord_webhook: str = ""
    emby_host: str = ""
    emby_api_key: str = ""
    proxy_url: str = ""


@router.post("/settings/all")
async def save_all_settings(config: GlobalConfig):
    """一键保存所有配置"""
    store.set_many({
        "qb_host": config.qb_host,
        "qb_port": config.qb_port,
        "qb_username": config.qb_username,
        "qb_password": config.qb_password,
        "tg_bot_token": config.tg_bot_token,
        "tg_chat_id": config.tg_chat_id,
        "discord_webhook": config.discord_webhook,
        "emby_host": config.emby_host,
        "emby_api_key": config.emby_api_key,
        "proxy_url": config.proxy_url,
    })
    logger.info("全局配置已保存")
    return {"saved": True}