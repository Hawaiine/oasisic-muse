"""NexusPHP 通用站点适配器 (Rousi, NicePT, PTTime)"""

from __future__ import annotations

import logging
import re
from typing import Any
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from .base import PTSiteAdapter, TorrentResult

logger = logging.getLogger(__name__)


class NexusPHPAdapter(PTSiteAdapter):
    """NexusPHP 站点适配器 (通用)"""

    def __init__(self, base_url: str, name: str, short: str, cookie: str = "", passkey: str = ""):
        super().__init__(cookie, passkey)
        self._base_url = base_url.rstrip("/")
        self._name = name
        self._short = short

    @property
    def name(self) -> str:
        return self._name

    @property
    def short_name(self) -> str:
        return self._short

    async def search(self, keyword: str) -> list[TorrentResult]:
        results: list[TorrentResult] = []
        search_url = f"{self._base_url}/torrents.php?search={keyword}"

        try:
            async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
                resp = await client.get(search_url, headers=self._build_headers())
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "html.parser")
                # NexusPHP 标准表格结构
                rows = soup.select("table.torrents > tr, tr.torrent_row")

                for row in rows[:30]:
                    try:
                        title_el = row.select_one("a[href*='details.php']")
                        if not title_el:
                            continue
                        title = title_el.get_text(strip=True)

                        # 下载链接
                        dl_link = row.select_one("a[href*='download.php']")
                        torrent_url = ""
                        if dl_link:
                            href = dl_link.get("href", "")
                            torrent_url = urljoin(self._base_url, href)

                        # 大小
                        size_el = row.select_one(
                            "td.rowfollow:nth-child(6), td:nth-child(5), td.size, .size"
                        )
                        size = size_el.get_text(strip=True) if size_el else ""

                        # 做种数
                        se_el = row.select_one(
                            "td.rowfollow:nth-child(7), td:nth-child(6), td.seeders, .seeders"
                        )
                        seeders = 0
                        if se_el:
                            m = re.search(r"\d+", se_el.get_text(strip=True))
                            if m:
                                seeders = int(m.group())

                        results.append(TorrentResult(
                            title=title,
                            site=self.short_name,
                            site_name=self.name,
                            torrent_url=torrent_url,
                            detail_url=urljoin(self._base_url, f"/{title_el.get('href', '')}"),
                            size=size,
                            seeders=seeders,
                            leechers=0,
                        ))
                    except Exception as e:
                        logger.debug("解析 %s 条目失败: %s", self._name, e)
                        continue
        except Exception as e:
            logger.error("%s 搜索失败: %s", self._name, e)

        return results


# 预设站点
def create_rousi(cookie: str = "") -> NexusPHPAdapter:
    return NexusPHPAdapter("https://rousi.pro", "Rousi", "RS", cookie)


def create_nicept(cookie: str = "") -> NexusPHPAdapter:
    return NexusPHPAdapter("https://www.nicept.net", "NicePT", "NPT", cookie)


def create_pttime(cookie: str = "") -> NexusPHPAdapter:
    return NexusPHPAdapter("https://www.pttime.org", "PTTime", "PTT", cookie)