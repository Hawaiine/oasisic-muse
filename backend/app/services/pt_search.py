"""PT 站点搜索服务 — 聚合搜索"""

from __future__ import annotations

import logging
from typing import Any

from .pt_sites.base import TorrentResult
from .pt_sites.mteam import MTeamAdapter
from .pt_sites.nexusphp import create_nicept, create_pttime, create_rousi

logger = logging.getLogger(__name__)


class PTSearchService:
    """PT 站点聚合搜索"""

    def __init__(self, cookies: dict[str, str] | None = None):
        """
        cookies: {站点短名: cookie} 如 {"MT": "...", "RS": "..."}
        """
        cookies = cookies or {}
        self.sites = [
            MTeamAdapter(cookie=cookies.get("MT", "")),
            create_rousi(cookie=cookies.get("RS", "")),
            create_nicept(cookie=cookies.get("NPT", "")),
            create_pttime(cookie=cookies.get("PTT", "")),
        ]

    async def search_all(self, keyword: str) -> list[TorrentResult]:
        """在所有站点搜索关键词"""
        import asyncio

        results: list[TorrentResult] = []
        tasks = [site.search(keyword) for site in self.sites]

        for task in asyncio.as_completed(tasks):
            try:
                site_results = await task
                results.extend(site_results)
            except Exception as e:
                logger.error("搜索失败: %s", e)

        # 按做种数降序排列
        results.sort(key=lambda r: r.seeders, reverse=True)
        return results

    async def search_subscribe(self, keyword: str, actor: str = "") -> list[TorrentResult]:
        """按订阅关键词搜索，合并演员关键词"""
        results = await self.search_all(keyword)
        if actor:
            # 过滤匹配演员的结果
            actor_lower = actor.lower()
            filtered = [r for r in results if actor_lower in r.title.lower()]
            if filtered:
                return filtered
        return results