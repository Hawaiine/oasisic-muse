"""标题翻译服务 — 多后端自动切换 + 缓存"""

from __future__ import annotations

import asyncio
import logging
import re
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class TranslateService:
    """翻译服务 — 自动切换后端

    后端优先级:
    1. Google Translate (海外)
    2. Microsoft Translator (国内可访问)
    3. 返回原文
    """

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
            self._cache[cache_key] = text
            return text

        # 顺序尝试多个后端
        backends = [
            ("Google", self._translate_google),
            ("Microsoft", self._translate_microsoft),
        ]

        for name, backend in backends:
            try:
                translated = await backend(text)
                if translated:
                    self._cache[cache_key] = translated
                    logger.info("[%s] %s → %s", name, text[:30], translated[:30])
                    return translated
            except Exception as e:
                logger.debug("[%s] 翻译失败: %s", name, e)
                continue

        # 所有后端都失败，返回原文
        self._cache[cache_key] = text
        return text

    @staticmethod
    def _needs_translate(text: str) -> bool:
        """判断是否需要翻译"""
        # 已含中文 → 不需要
        if re.search(r"[\u4e00-\u9fff]", text):
            return False
        # 纯番号格式（ABC-123）→ 不需要
        if re.match(r"^[A-Z]{2,6}[-_\s]?\d{2,6}", text.strip()):
            return False
        # 太短 → 不需要
        return len(text.strip()) > 5

    async def _translate_google(self, text: str) -> str | None:
        """Google Translate 免费接口"""
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "zh-CN",
            "dt": "t",
            "q": text[:500],
        }
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                sentences = []
                for part in data[0]:
                    if part[0]:
                        sentences.append(part[0])
                return "".join(sentences) if sentences else None
        except Exception as e:
            logger.debug("Google Translate 不可用: %s", e)
            return None

    async def _translate_microsoft(self, text: str) -> str | None:
        """Microsoft Translator 国内可访问

        使用官方免费接口 (不需要 API Key)
        """
        url = "https://api.cognitive.microsofttranslator.com/translate"
        params = {
            "api-version": "3.0",
            "from": "auto",
            "to": "zh-Hans",
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json; charset=UTF-8",
        }
        body = [{"Text": text[:500]}]

        try:
            async with httpx.AsyncClient(timeout=8) as client:
                resp = await client.post(url, params=params, json=body, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                if data and len(data) > 0 and "translations" in data[0]:
                    return data[0]["translations"][0].get("text")
                return None
        except Exception as e:
            logger.debug("Microsoft Translator 不可用: %s", e)
            return None

    async def batch_translate(self, texts: list[str]) -> list[str]:
        """批量翻译"""
        tasks = [self.to_chinese(t) for t in texts]
        return await asyncio.gather(*tasks)