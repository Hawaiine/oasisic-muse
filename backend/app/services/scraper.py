"""AV 元数据刮削引擎 — 真实实现

数据源: jav321.com（可访问，无需代理）
字段: 标题、封面、演员、发行日期、类别、制作商、时长
封面: 下载到本地 + 生成缩略图

错误分类:
- source_unreachable: 数据源不可达
- not_found: 未找到该番号
- parse_error: 页面解析规则失效
- cloudflare_blocked: 被 Cloudflare 拦截
"""

from __future__ import annotations

import asyncio
import logging
import re
from pathlib import Path
from typing import Any

import httpx
from PIL import Image

from ..config import settings

logger = logging.getLogger(__name__)

# 数据目录
DATA_DIR = Path(settings.database_url.replace("sqlite:///", "")).parent
COVERS_DIR = DATA_DIR / "covers"
THUMBS_DIR = DATA_DIR / "thumbs"

# 错误类型
ERR_UNREACHABLE = "source_unreachable"
ERR_NOT_FOUND = "not_found"
ERR_PARSE = "parse_error"
ERR_CLOUDFLARE = "cloudflare_blocked"


class ScrapeError(Exception):
    """刮削异常"""
    def __init__(self, error_type: str, message: str, detail: Any = None):
        self.error_type = error_type
        self.message = message
        self.detail = detail
        super().__init__(f"[{error_type}] {message}")


class AVScraper:
    """AV 元数据刮削引擎（真实实现）"""

    # 数据源配置
    SOURCES = {
        "jav321": {
            "search_url": "https://jav321.com/search/{movie_id}",
            "detail_url": "https://jav321.com/video/{movie_id}",
        },
    }

    def __init__(self, proxy_url: str = ""):
        self._proxy_url = proxy_url or settings.proxy_url
        # 确保目录存在
        COVERS_DIR.mkdir(parents=True, exist_ok=True)
        THUMBS_DIR.mkdir(parents=True, exist_ok=True)

    def _get_client(self) -> httpx.AsyncClient:
        kwargs: dict[str, Any] = {
            "timeout": 15,
            "follow_redirects": True,
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        }
        if self._proxy_url:
            kwargs["proxies"] = self._proxy_url
            logger.debug("刮削使用代理: %s", self._proxy_url)
        return httpx.AsyncClient(**kwargs)

    async def scrape(self, movie_id: str) -> dict[str, Any]:
        """刮削单个番号的完整元数据

        返回:
            id: 番号
            title: 标题
            cover_url: 封面 URL
            cover_path: 本地封面路径
            thumb_path: 本地缩略图路径
            actors: [演员名]
            release_date: 发行日期
            categories: [类别]
            duration: 时长
            maker: 制作商
            source: 数据源
            error: 错误信息（仅失败时）
            error_type: 错误类型（仅失败时）
        """
        movie_id = movie_id.upper().replace("_", "-").strip()
        if not movie_id:
            return {"error": "番号为空", "error_type": ERR_NOT_FOUND}

        logger.info("刮削开始: %s", movie_id)

        # 从 jav321 获取数据
        try:
            result = await self._scrape_jav321(movie_id)
            if result:
                # 下载封面
                if result.get("cover_url"):
                    await self._download_cover(result["cover_url"], movie_id, result)
                return result
        except ScrapeError as e:
            logger.warning("刮削 %s 失败: %s", movie_id, e.message)
            return {
                "id": movie_id,
                "error": e.message,
                "error_type": e.error_type,
                "detail": e.detail,
            }
        except Exception as e:
            logger.error("刮削 %s 异常: %s", movie_id, e)
            return {
                "id": movie_id,
                "error": str(e)[:100],
                "error_type": ERR_UNREACHABLE,
            }

        return {
            "id": movie_id,
            "error": "所有数据源均未找到",
            "error_type": ERR_NOT_FOUND,
        }

    async def _scrape_jav321(self, movie_id: str) -> dict[str, Any] | None:
        """从 jav321.com 刮削

        实测验证: 返回封面、演员、类别、时长等真实数据
        """
        # 小写化番号用于 URL
        vid = movie_id.lower().replace("-", "")
        url = f"https://jav321.com/video/{vid}"

        async with self._get_client() as client:
            resp = await client.get(url)

            if resp.status_code == 404:
                # 尝试搜索
                search_url = f"https://jav321.com/search/{movie_id}"
                resp = await client.get(search_url)
                if resp.status_code != 200:
                    raise ScrapeError(ERR_UNREACHABLE, f"数据源返回 HTTP {resp.status_code}")

            html = resp.text

            # 检测 Cloudflare 拦截
            if "Just a moment" in html or "cf_chl_opt" in html:
                raise ScrapeError(ERR_CLOUDFLARE, "被 Cloudflare 拦截，请更换代理或稍后重试")

            # 检测番号未找到
            if "not found" in html.lower() or "没有找到" in html:
                raise ScrapeError(ERR_NOT_FOUND, f"未找到番号 {movie_id}")

            # ▸ 解析封面
            cover_url = ""
            cover_match = re.search(
                r'<img[^>]*class="img-responsive[^"]*"[^>]*src="(https?://[^"]+)"',
                html,
            )
            if cover_match:
                cover_url = cover_match.group(1)
                # 小图替换为大图
                cover_url = cover_url.replace("ps.jpg", ".jpg")  # 小预览 → 大图
                cover_url = cover_url.replace("-1.jpg", ".jpg")  # 另一种格式

            # ▸ 解析演员
            actors = []
            actor_matches = re.findall(
                r'<h4[^>]*align="center"[^>]*>(.*?)</h4>',
                html,
            )
            for a in actor_matches:
                name = a.strip()
                if name and len(name) < 20:
                    actors.append(name)

            # ▸ 解析发行日期
            release_date = ""
            date_match = re.search(r"发行日期[：:]\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})", html)
            if date_match:
                release_date = date_match.group(1)

            # ▸ 解析类别
            categories = re.findall(
                r'<a[^>]*href="/genre/[^"]+"[^>]*>(.*?)</a>',
                html,
            )
            # 清洗 HTML 标签
            categories = [re.sub(r"<[^>]+>", "", c).strip() for c in categories if c.strip()]

            # ▸ 解析时长
            duration = ""
            dur_match = re.search(r"(\d+)\s*分钟", html)
            if dur_match:
                duration = f"{dur_match.group(1)} 分钟"

            # ▸ 解析制作商
            maker = ""
            maker_match = re.search(r"制作商[：:]\s*(.*?)(?:<|$)", html)
            if maker_match:
                maker = maker_match.group(1).strip()

            # ▸ 解析标题（从页面文本）
            title = ""
            # 尝试从页面 heading 提取
            title_match = re.search(
                r'<h3[^>]*>(.*?)</h3>',
                html,
            )
            if title_match:
                title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip()

            result = {
                "id": movie_id.upper(),
                "title": title or movie_id.upper(),
                "cover_url": cover_url,
                "actors": actors,
                "release_date": release_date,
                "categories": categories,
                "duration": duration,
                "maker": maker,
                "source": "jav321",
            }

            logger.info(
                "jav321 刮削成功: %s | 演员=%d | 类别=%d | 封面=%s",
                movie_id,
                len(actors),
                len(categories),
                "有" if cover_url else "无",
            )
            return result

    async def _download_cover(self, url: str, movie_id: str, result: dict) -> None:
        """下载封面到本地并生成缩略图"""
        if not url:
            return

        cover_path = COVERS_DIR / f"{movie_id.lower()}.jpg"
        thumb_path = THUMBS_DIR / f"{movie_id.lower()}.jpg"

        try:
            async with self._get_client() as client:
                resp = await client.get(url)
                resp.raise_for_status()
                cover_path.write_bytes(resp.content)
                result["cover_path"] = str(cover_path)

                # 生成缩略图 (240px 宽)
                try:
                    img = Image.open(cover_path)
                    img.thumbnail((240, 340), Image.LANCZOS)
                    img.save(thumb_path, "JPEG", quality=75)
                    result["thumb_path"] = str(thumb_path)
                    logger.info("封面已下载: %s (原图=%dKB, 缩略图=%dKB)",
                               movie_id, len(resp.content) // 1024,
                               thumb_path.stat().st_size // 1024)
                except Exception as e:
                    logger.warning("缩略图生成失败: %s", e)
                    result["thumb_path"] = str(cover_path)

        except Exception as e:
            logger.warning("封面下载失败: %s", e)
            result["cover_path"] = url  # 保留原始 URL

    async def scrape_batch(self, movie_ids: list[str]) -> list[dict[str, Any]]:
        """批量刮削"""
        results = []
        for mid in movie_ids:
            result = await self.scrape(mid)
            results.append(result)
            await asyncio.sleep(0.5)  # 避免请求过快
        return results