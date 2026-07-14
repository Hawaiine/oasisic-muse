"""设置管理 API"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

PT_CONFIG_PATH = Path(settings.database_url.replace("sqlite:///", "")).parent / "pt_sites.json"


def _load_pt_config() -> dict:
    """读取 PT 站点配置"""
    if PT_CONFIG_PATH.exists():
        try:
            return json.loads(PT_CONFIG_PATH.read_text())
        except Exception as e:
            logger.error("读取 PT 配置失败: %s", e)
    return {}


def _save_pt_config(config: dict):
    """保存 PT 站点配置"""
    PT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    PT_CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False))


@router.get("/settings")
async def get_settings():
    """获取当前配置（脱敏）"""
    pt_config = _load_pt_config()

    return {
        "qb_host": settings.qb_host or "未配置",
        "qb_port": settings.qb_port,
        "tg_bot_token": "已配置" if settings.tg_bot_token else "未配置",
        "tg_chat_id": "已配置" if settings.tg_chat_id else "未配置",
        "discord_webhook": "已配置" if settings.discord_webhook else "未配置",
        "emby_host": settings.emby_host or "未配置",
        "proxy_url": settings.proxy_url or "未配置",
        "pt_sites": [
            {
                "short": "MT",
                "name": "M-Team",
                "url": "https://kp.m-team.cc",
                "auth_type": "cookie",
                "cookie_configured": bool(pt_config.get("MT", {}).get("cookie", "")),
            },
            {
                "short": "RS",
                "name": "Rousi",
                "url": "https://rousi.pro",
                "auth_type": "cookie+passkey",
                "cookie_configured": bool(pt_config.get("RS", {}).get("cookie", "")),
            },
            {
                "short": "NPT",
                "name": "NicePT",
                "url": "https://www.nicept.net",
                "auth_type": "cookie+passkey",
                "cookie_configured": bool(pt_config.get("NPT", {}).get("cookie", "")),
            },
            {
                "short": "PTT",
                "name": "PTTime",
                "url": "https://www.pttime.org",
                "auth_type": "cookie+passkey",
                "cookie_configured": bool(pt_config.get("PTT", {}).get("cookie", "")),
            },
        ],
    }


class PTSiteAuth(BaseModel):
    cookie: str = ""
    passkey: str = ""


class PTSitesConfig(BaseModel):
    sites: dict[str, PTSiteAuth]  # key = site short name


@router.post("/settings/pt-sites")
async def save_pt_sites(config: PTSitesConfig):
    """保存 PT 站点认证信息"""
    current = _load_pt_config()
    for short, auth in config.sites.items():
        if short not in current:
            current[short] = {}
        if auth.cookie:
            current[short]["cookie"] = auth.cookie
        if auth.passkey:
            current[short]["passkey"] = auth.passkey

    _save_pt_config(current)
    logger.info("已保存 %d 个 PT 站点配置", len(config.sites))
    return {"saved": True, "sites": list(config.sites.keys())}


@router.get("/settings/pt-sites")
async def get_pt_sites_config():
    """获取 PT 站点认证信息（仅返回是否已配置，不返回实际值）"""
    config = _load_pt_config()
    return {
        short: {
            "cookie_configured": bool(data.get("cookie", "")),
            "passkey_configured": bool(data.get("passkey", "")),
        }
        for short, data in config.items()
    }