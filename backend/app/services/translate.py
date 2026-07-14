"""标题翻译服务 — 日文/英文 → 中文"""

from __future__ import annotations

import logging
import re
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class TranslateService:
    """翻译服务（Google Translate 免费接口）"""

    def __init__(self):
        self._cache: dict[str, str] = {}

    async def to_chinese(self, text: str) -> str:
        """将文本翻译为中文

        自动检测是否需要翻译（仅含日文/英文时翻译）
        """
        if not text or len(text) < 3:
            return text

        # 检查缓存
        cache_key = text.strip().lower()
        if cache_key in self._cache:
            return self._cache[cache_key]

        # 判断是否需要翻译
        if not self._needs_translate(text):
            # 已有中文，直接返回
            self._cache[cache_key] = text
            return text

        try:
            translated = await self._translate(text)
            if translated:
                self._cache[cache_key] = translated
                return translated
        except Exception as e:
            logger.warning("翻译失败: %s", e)

        return text

    @staticmethod
    def _needs_translate(text: str) -> bool:
        """判断是否需要翻译

        如果文本包含中文字符，视为已有中文，不需要翻译
        如果没有中文字符且文本长度超过5，需要翻译
        """
        has_chinese = bool(re.search(r"[\u4e00-\u9fff]", text))
        if has_chinese:
            return False
        # 纯番号格式不翻译（如 ABC-123）
        if re.match(r"^[A-Z]{2,6}[-_\s]?\d{2,6}", text.strip()):
            return False
        return len(text.strip()) > 5

    async def _translate(self, text: str) -> str | None:
        """调用 Google Translate 免费接口"""
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "zh-CN",
            "dt": "t",
            "q": text[:500],  # 限制长度
        }
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                # 解析响应
                sentences = []
                for part in data[0]:
                    if part[0]:
                        sentences.append(part[0])
                result = "".join(sentences)
                return result if result else None
        except Exception as e:
            logger.error("Google Translate 请求失败: %s", e)
            return None

    async def batch_translate(self, texts: list[str]) -> list[str]:
        """批量翻译"""
        import asyncio
        tasks = [self.to_chinese(t) for t in texts]
        return await asyncio.gather(*tasks)