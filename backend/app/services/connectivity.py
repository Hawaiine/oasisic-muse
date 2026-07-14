"""连通性检测 — PT站/下载器/Jellyfin/通知"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import httpx

from ..config import settings
from ..services.downloader import DownloaderService
from ..services.media_library import MediaLibraryService
from ..services.notifier import NotifierService

logger = logging.getLogger(__name__)

PT_CONFIG_PATH = Path(settings.database_url.replace("sqlite:///", "")).parent / "pt_sites.json"


class ConnectivityCheck:
    """全局连通性检测"""

    PT_SITES = [
        {"short": "MT", "name": "M-Team", "url": "https://kp.m-team.cc"},
        {"short": "RS", "name": "Rousi", "url": "https://rousi.pro"},
        {"short": "NPT", "name": "NicePT", "url": "https://www.nicept.net"},
        {"short": "PTT", "name": "PTTime", "url": "https://www.pttime.org"},
    ]

    @staticmethod
    def _get_pt_cookies() -> dict[str, str]:
        """读取 PT 站点 Cookie"""
        if PT_CONFIG_PATH.exists():
            try:
                config = json.loads(PT_CONFIG_PATH.read_text())
                return {
                    short: data.get("cookie", "")
                    for short, data in config.items()
                    if data.get("cookie")
                }
            except Exception:
                return {}
        return {}

    async def check_all(self) -> dict:
        """检测所有服务连通性"""
        import asyncio

        results = {"services": [], "summary": {"total": 0, "online": 0, "offline": 0}}

        # 并发检测
        tasks = [
            self._check_pt_sites(),
            self._check_downloader(),
            self._check_media_library(),
            self._check_notify(),
            self._check_disk(),
        ]

        for task in asyncio.as_completed(tasks):
            try:
                result = await task
                if isinstance(result, list):
                    results["services"].extend(result)
                else:
                    results["services"].append(result)
            except Exception as e:
                logger.error("连通性检测失败: %s", e)

        # 汇总
        for s in results["services"]:
            results["summary"]["total"] += 1
            if s.get("status") == "online":
                results["summary"]["online"] += 1
            else:
                results["summary"]["offline"] += 1

        return results

    async def _check_pt_sites(self) -> list[dict]:
        """检测 PT 站点连通性"""
        results = []
        cookies = self._get_pt_cookies()

        for site in self.PT_SITES:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                if site["short"] in cookies:
                    headers["Cookie"] = cookies[site["short"]]

                async with httpx.AsyncClient(timeout=8, follow_redirects=True) as client:
                    resp = await client.get(site["url"], headers=headers)
                    online = resp.status_code == 200
                    results.append({
                        "type": "pt_site",
                        "name": site["name"],
                        "short": site["short"],
                        "url": site["url"],
                        "status": "online" if online else "offline",
                        "http_code": resp.status_code,
                        "auth_configured": site["short"] in cookies,
                    })
            except Exception as e:
                results.append({
                    "type": "pt_site",
                    "name": site["name"],
                    "short": site["short"],
                    "url": site["url"],
                    "status": "offline",
                    "error": str(e)[:50],
                    "auth_configured": site["short"] in cookies,
                })

        return results

    async def _check_downloader(self) -> dict:
        """检测下载器连通性"""
        if not settings.qb_host:
            return {"type": "downloader", "name": "qBittorrent", "status": "offline", "reason": "未配置"}

        try:
            dl = DownloaderService()
            result = await dl.check_connection()
            return {
                "type": "downloader",
                "name": "qBittorrent",
                "status": "online" if result.get("connected") else "offline",
                "version": result.get("version", ""),
                "error": result.get("error", ""),
            }
        except Exception as e:
            return {"type": "downloader", "name": "qBittorrent", "status": "offline", "error": str(e)[:50]}

    async def _check_media_library(self) -> dict:
        """检测媒体库连通性"""
        if not settings.emby_host:
            return {"type": "media_library", "name": "Jellyfin/EMBY", "status": "offline", "reason": "未配置"}

        try:
            lib = MediaLibraryService()
            result = await lib.check_connection()
            return {
                "type": "media_library",
                "name": "Jellyfin/EMBY",
                "status": "online" if result.get("connected") else "offline",
                "version": result.get("version", ""),
                "server_name": result.get("server_name", ""),
            }
        except Exception as e:
            return {"type": "media_library", "name": "Jellyfin/EMBY", "status": "offline", "error": str(e)[:50]}

    async def _check_notify(self) -> dict:
        """检测通知渠道配置"""
        channels = []
        if settings.tg_bot_token and settings.tg_chat_id:
            channels.append("Telegram")
        if settings.discord_webhook:
            channels.append("Discord")
        return {
            "type": "notify",
            "name": "通知",
            "status": "online" if channels else "offline",
            "channels": channels or ["未配置"],
        }

    @staticmethod
    async def _check_disk() -> dict:
        """检测磁盘空间"""
        import shutil
        try:
            usage = shutil.disk_usage("/data")
            free_gb = usage.free / (1024 ** 3)
            total_gb = usage.total / (1024 ** 3)
            return {
                "type": "disk",
                "name": "磁盘空间",
                "status": "online" if free_gb > 5 else "offline",
                "free_gb": round(free_gb, 1),
                "total_gb": round(total_gb, 1),
                "used_percent": round((usage.used / usage.total) * 100, 1),
            }
        except Exception as e:
            return {"type": "disk", "name": "磁盘空间", "status": "offline", "error": str(e)[:50]}