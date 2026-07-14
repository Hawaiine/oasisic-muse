"""M-Team (MT) 站点适配器"""

from __future__ import annotations

import logging
import re
from typing import Any

import httpx
from bs4 import BeautifulSoup

from .base import PTSiteAdapter, TorrentResult

logger = logging.getLogger(__name__)


class MTeamAdapter(PTSiteAdapter):
    """M-Team 站点 (kp.m-team.cc)"""

    @property
    def name(self) -> str:
        return "M-Team"

    @property
    def short_name(self) -> str:
        return "MT"

    async def search(self, keyword: str) -> list[TorrentResult]:
        results: list[TorrentResult] = []
        url = f"https://kp.m-team.cc/torrents.php?search={keyword}&search_area=0"

        try:
            async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
                resp = await client.get(url, headers=self._build_headers())
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "html.parser")
                rows = soup.select("table.torrents > tr, .torrentrow, tr.torrent_row")

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
                            torrent_url = f"https://kp.m-team.cc/{href}" if not href.startswith("http") else href

                        # 做种数
                        se_el = row.select_one("td.rowfollow:nth-child(7), td.seeders, span.seeders")
                        seeders = int(re.search(r"\d+", se_el.get_text() if se_el else "0").group()) if se_el else 0

                        results.append(TorrentResult(
                            title=title,
                            site=self.short_name,
                            site_name=self.name,
                            torrent_url=torrent_url,
                            detail_url=f"https://kp.m-team.cc/{title_el.get('href', '')}",
                            size="",
                            seeders=seeders,
                            leechers=0,
                        ))
                    except Exception as e:
                        logger.debug("解析 M-Team 条目失败: %s", e)
                        continue
        except Exception as e:
            logger.error("M-Team 搜索失败: %s", e)

        return results