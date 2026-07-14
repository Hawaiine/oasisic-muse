"""PT 站点适配器基类"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TorrentResult:
    """标准化种子结果"""
    title: str
    site: str
    site_name: str
    torrent_url: str
    detail_url: str
    size: str
    seeders: int
    leechers: int
    category: str = ""
    free: bool = False


class PTSiteAdapter(ABC):
    """PT 站点适配器基类"""

    def __init__(self, cookie: str = "", passkey: str = ""):
        self.cookie = cookie
        self.passkey = passkey

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def short_name(self) -> str: ...

    @abstractmethod
    async def search(self, keyword: str) -> list[TorrentResult]: ...

    def _parse_size(self, size_str: str) -> str:
        """统一大小格式"""
        return size_str.strip()

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        if self.cookie:
            headers["Cookie"] = self.cookie
        return headers