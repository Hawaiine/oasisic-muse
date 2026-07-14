"""AV 元数据刮削 — 封面/演员/信息"""

from __future__ import annotations

import logging
import re
from typing import Any

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class AVMetadataService:
    """AV 元数据刮削

    通过番号从多个数据源刮削封面、演员、标题等信息
    """

    def __init__(self):
        self._cover_cache: dict[str, str] = {}

    async def lookup(self, movie_id: str) -> dict[str, Any] | None:
        """根据番号查询元数据

        Args:
            movie_id: 番号，如 ABC-123
        """
        movie_id = movie_id.upper().replace("_", "-").strip()
        if not movie_id:
            return None

        # 尝试多个数据源
        sources = [
            ("JavDB", self._lookup_javdb),
            ("JavLibrary", self._lookup_javlibrary),
        ]

        for name, source in sources:
            try:
                result = await source(movie_id)
                if result:
                    logger.info("[%s] %s 刮削成功", name, movie_id)
                    return result
            except Exception as e:
                logger.debug("[%s] %s 刮削失败: %s", name, movie_id, e)
                continue

        return None

    async def extract_from_title(self, title: str) -> list[dict[str, Any]]:
        """从标题中提取番号并刮削元数据"""
        ids = self._extract_ids(title)
        results = []
        for mid in ids[:3]:  # 最多查3个
            meta = await self.lookup(mid)
            if meta:
                results.append(meta)
        return results

    @staticmethod
    def _extract_ids(text: str) -> list[str]:
        """从文本中提取番号"""
        patterns = [
            r"([A-Z]{2,6}[-_\s]?\d{2,6})",
            r"(\d{2,6}[-_\s]?[A-Z]{2,6})",
        ]
        ids = []
        for pattern in patterns:
            matches = re.findall(pattern, text.upper())
            for m in matches:
                clean = m.replace(" ", "-").replace("_", "-")
                if clean not in ids:
                    ids.append(clean)
        return ids

    async def _lookup_javdb(self, movie_id: str) -> dict[str, Any] | None:
        """JavDB 查询"""
        url = f"https://javdb.com/search?q={movie_id}&f=all"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml",
        }

        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "html.parser")

                # 封面
                cover_img = soup.select_one(".movie-cover img, .cover img, img.cover")
                cover_url = ""
                if cover_img:
                    src = cover_img.get("src", "")
                    if src and not src.startswith("data:"):
                        cover_url = src

                # 标题
                title_el = soup.select_one(".title, .movie-title, h2 strong")
                title = title_el.get_text(strip=True) if title_el else ""

                # 演员
                actors = []
                actor_els = soup.select(".actors a, .cast a")
                for a in actor_els:
                    name = a.get_text(strip=True)
                    if name:
                        actors.append(name)

                if title or cover_url:
                    return {
                        "id": movie_id,
                        "title": title,
                        "cover": cover_url,
                        "actors": actors,
                        "source": "javdb",
                    }
        except Exception as e:
            logger.debug("JavDB 查询失败: %s", e)
        return None

    async def _lookup_javlibrary(self, movie_id: str) -> dict[str, Any] | None:
        """JavLibrary 查询"""
        url = f"https://www.javlibrary.com/cn/vl_searchbytitle.php?keyword={movie_id}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml",
        }

        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "html.parser")
                video = soup.select_one(".videothumblist .video, .searchresult .video")
                if not video:
                    return None

                cover_img = video.select_one("img")
                cover_url = cover_img.get("src", "") if cover_img else ""

                title_el = video.select_one(".title")
                title = title_el.get_text(strip=True) if title_el else ""

                if title or cover_url:
                    return {
                        "id": movie_id,
                        "title": title,
                        "cover": cover_url,
                        "actors": [],
                        "source": "javlibrary",
                    }
        except Exception as e:
            logger.debug("JavLibrary 查询失败: %s", e)
        return None