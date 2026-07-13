"""下载服务 — qBittorrent 集成"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from ..config import settings

logger = logging.getLogger(__name__)


class DownloaderService:
    """qBittorrent 下载管理"""

    @property
    def _base_url(self) -> str:
        return f"http://{settings.qb_host}:{settings.qb_port}"

    async def login(self) -> bool:
        """登录 qBittorrent Web UI"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    f"{self._base_url}/api/v2/auth/login",
                    data={"username": settings.qb_username, "password": settings.qb_password},
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error("qBittorrent 登录失败: %s", e)
            return False

    async def add_torrent(self, torrent_url: str, save_path: str = "") -> dict[str, Any]:
        """添加种子下载"""
        if not await self.login():
            return {"success": False, "error": "登录失败"}

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                files = {"urls": (None, torrent_url)}
                if save_path:
                    files["savepath"] = (None, save_path)
                resp = await client.post(
                    f"{self._base_url}/api/v2/torrents/add",
                    data=files,
                )
                return {"success": resp.status_code == 200, "status_code": resp.status_code}
        except Exception as e:
            logger.error("添加下载失败: %s", e)
            return {"success": False, "error": str(e)}

    async def get_torrents(self) -> list[dict]:
        """获取种子列表"""
        if not await self.login():
            return []

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{self._base_url}/api/v2/torrents/info",
                )
                return resp.json() if resp.status_code == 200 else []
        except Exception as e:
            logger.error("获取种子列表失败: %s", e)
            return []