"""元数据刮削服务"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)


class ScraperService:
    """AV 元数据刮削"""

    @staticmethod
    def parse_id(filename: str) -> str | None:
        """从文件名提取番号"""
        # 常见番号格式: ABC-123, ABC-12345, ABCDEF-123
        patterns = [
            r"([A-Z]{2,6}[-_]\d{2,6})",
            r"(\d{2,6}[-_][A-Z]{2,6})",
            r"([A-Z]{2,6}\d{2,6})",
        ]
        for pattern in patterns:
            match = re.search(pattern, filename.upper())
            if match:
                return match.group(1).replace("_", "-")
        return None

    @staticmethod
    def build_search_url(keyword: str) -> str:
        """生成搜索 URL"""
        import urllib.parse
        return f"https://www.javlibrary.com/cn/vl_searchbytitle.php?keyword={urllib.parse.quote(keyword)}"

    async def scrape(self, movie_id: str) -> dict:
        """刮削元数据（占位，后续对接具体数据源）"""
        return {
            "id": movie_id,
            "title": "",
            "actor": "",
            "cover": "",
            "tags": [],
            "release_date": "",
        }