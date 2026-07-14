"""媒体库服务 — Jellyfin + EMBY"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from ..config import settings

logger = logging.getLogger(__name__)


class MediaLibraryService:
    """媒体库对接（Jellyfin 为主，EMBY 兼容）"""

    def __init__(self):
        self.host = settings.emby_host
        self.api_key = settings.emby_api_key

    @property
    def _is_configured(self) -> bool:
        return bool(self.host and self.api_key)

    async def _request(self, path: str, method: str = "GET") -> dict | list | None:
        if not self._is_configured:
            return None
        url = f"{self.host.rstrip('/')}{path}"
        headers = {
            "X-Emby-Token": self.api_key,
            "Accept": "application/json",
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.request(method, url, headers=headers)
                resp.raise_for_status()
                return resp.json() if resp.text else None
        except Exception as e:
            logger.error("媒体库请求失败 %s: %s", url, e)
            return None

    async def check_connection(self) -> dict:
        """检测连通性"""
        info = await self._request("/System/Info")
        if info and isinstance(info, dict):
            return {
                "connected": True,
                "version": info.get("Version", ""),
                "server_name": info.get("ServerName", ""),
            }
        return {"connected": False, "error": "无法连接"}

    async def refresh_library(self, item_id: str | None = None) -> bool:
        """刷新媒体库

        Args:
            item_id: 指定条目 ID，None 则表示全部刷新
        """
        path = "/Library/Refresh"
        if item_id:
            path = f"/Items/{item_id}/Refresh"

        result = await self._request(path, method="POST")
        return result is not None

    async def search_media(self, name: str) -> list[dict]:
        """搜索媒体库中的资源"""
        result = await self._request(f"/Items?searchTerm={name}&IncludeItemTypes=Movie&Recursive=true")
        if isinstance(result, dict):
            return result.get("Items", [])
        return []

    async def get_recent(self, limit: int = 10) -> list[dict]:
        """获取最近添加的媒体"""
        result = await self._request(
            f"/Items?Limit={limit}&SortBy=DateCreated&SortOrder=Descending&Recursive=true"
        )
        if isinstance(result, dict):
            return result.get("Items", [])
        return []