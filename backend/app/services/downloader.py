"""下载服务 — qBittorrent 集成"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from ..config import settings

logger = logging.getLogger(__name__)


class DownloaderService:
    """qBittorrent 下载管理"""

    def __init__(self):
        self._base_url = f"http://{settings.qb_host}:{settings.qb_port}"
        self._client = httpx.AsyncClient(timeout=15)

    async def login(self) -> bool:
        """登录 qBittorrent Web UI"""
        try:
            resp = await self._client.post(
                f"{self._base_url}/api/v2/auth/login",
                data={"username": settings.qb_username, "password": settings.qb_password},
            )
            return resp.status_code == 200
        except Exception as e:
            logger.error("qBittorrent 登录失败: %s", e)
            return False

    async def add_torrent(self, torrent_url: str, save_path: str = "", category: str = "") -> dict[str, Any]:
        """添加种子下载"""
        if not await self.login():
            return {"success": False, "error": "登录失败"}

        try:
            data: dict[str, str] = {"urls": torrent_url}
            if save_path:
                data["savepath"] = save_path
            if category:
                data["category"] = category
            resp = await self._client.post(
                f"{self._base_url}/api/v2/torrents/add",
                data=data,
            )
            return {"success": resp.status_code == 200, "status_code": resp.status_code}
        except Exception as e:
            logger.error("添加下载失败: %s", e)
            return {"success": False, "error": str(e)}

    async def get_torrents(self, filter: str = "all") -> list[dict]:
        """获取种子列表"""
        if not await self.login():
            return []
        try:
            resp = await self._client.get(
                f"{self._base_url}/api/v2/torrents/info",
                params={"filter": filter},
            )
            return resp.json() if resp.status_code == 200 else []
        except Exception as e:
            logger.error("获取种子列表失败: %s", e)
            return []

    async def get_torrent(self, hash: str) -> dict | None:
        """获取单个种子详情"""
        torrents = await self.get_torrents()
        for t in torrents:
            if t.get("hash") == hash:
                return t
        return None

    async def delete_torrent(self, hash: str, delete_files: bool = False) -> bool:
        """删除种子"""
        if not await self.login():
            return False
        try:
            resp = await self._client.post(
                f"{self._base_url}/api/v2/torrents/delete",
                data={"hashes": hash, "deleteFiles": "true" if delete_files else "false"},
            )
            return resp.status_code == 200
        except Exception as e:
            logger.error("删除种子失败: %s", e)
            return False

    async def check_connection(self) -> dict:
        """检测连通性"""
        try:
            resp = await self._client.get(
                f"{self._base_url}/api/v2/app/version",
                timeout=5,
            )
            if resp.status_code == 200:
                return {"connected": True, "version": resp.text.strip()}
            return {"connected": False, "error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"connected": False, "error": str(e)}