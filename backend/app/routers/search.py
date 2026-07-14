"""搜索 API — 对接 PT 站点"""

from __future__ import annotations

import asyncio

from fastapi import APIRouter

from ..services.av_metadata import AVMetadataService
from ..services.pt_search import PTSearchService
from ..services.translate import TranslateService

router = APIRouter()
translator = TranslateService()
av_meta = AVMetadataService()


@router.get("/search")
async def search_pt(keyword: str = "", actor: str = "", category: str = "av", translate: bool = True, covers: bool = True):
    """搜索 PT 站点

    Args:
        keyword: 搜索关键词/番号/演员名
        actor: 演员名（可选）
        category: 分类，av=仅AV，all=全部
        translate: 是否翻译标题
        covers: 是否查询封面
    """
    service = PTSearchService()
    if actor:
        results = await service.search_subscribe(keyword, actor)
    else:
        results = await service.search_all(keyword)

    # 智能过滤：番号格式或指定AV模式
    if category == "av":
        results = [r for r in results if _is_av_related(r.title, keyword, actor)]

    items = [r.__dict__ for r in results]

    # 翻译标题
    if translate and items:
        await _translate_items(items)

    # 查询封面
    if covers and items:
        await _attach_covers(items)

    return {
        "items": items,
        "total": len(items),
        "category": category,
    }


async def _translate_items(items: list[dict]):
    """批量翻译标题"""
    titles = [item["title"] for item in items]
    translated = await translator.batch_translate(titles)
    for item, t_title in zip(items, translated):
        item["title_cn"] = t_title if t_title and t_title != item["title"] else ""


async def _attach_covers(items: list[dict]):
    """批量查询封面"""
    async def _get_cover(item: dict):
        ids = av_meta._extract_ids(item["title"])
        if ids:
            meta = await av_meta.lookup(ids[0])
            if meta and meta.get("cover"):
                item["cover"] = meta["cover"]
                item["actors"] = meta.get("actors", [])
                item["movie_id"] = ids[0]

    tasks = [_get_cover(item) for item in items[:10]]  # 最多查10个封面
    await asyncio.gather(*tasks)


def _is_av_related(title: str, keyword: str, actor: str = "") -> bool:
    """判断是否AV相关内容

    - 标题含番号格式 → AV
    - 关键词本身是番号 → 全部匹配
    - 关键词是名字 → 按文本匹配
    """
    import re
    # 标题含番号
    if re.search(r"[A-Z]{2,6}[-_\s]?\d{2,6}", title.upper()):
        return True
    # 关键词本身是番号 → 放宽匹配
    if re.match(r"^[A-Z]{2,6}[-_\s]?\d{2,6}", keyword.upper()):
        return True
    # 包含演员名
    if actor and actor.lower() in title.lower():
        return True
    return False


@router.get("/search/lookup")
async def lookup_movie(movie_id: str):
    """查询单个作品的元数据（封面、演员、发行日期、类别等）

    使用真实数据源 jav321.com 刮削
    """
    from ..services.scraper import AVScraper
    scraper = AVScraper()
    result = await scraper.scrape(movie_id)
    return result


@router.post("/search/scrape")
async def scrape_movie(movie_id: str):
    """手动触发刮削（下载封面+生成缩略图）"""
    from ..services.scraper import AVScraper
    scraper = AVScraper()
    result = await scraper.scrape(movie_id)
    return result


@router.get("/search/sites")
async def list_sites():
    """列出已配置的 PT 站点"""
    return {
        "sites": [
            {"name": "M-Team", "short": "MT", "url": "https://kp.m-team.cc"},
            {"name": "Rousi", "short": "RS", "url": "https://rousi.pro"},
            {"name": "NicePT", "short": "NPT", "url": "https://www.nicept.net"},
            {"name": "PTTime", "short": "PTT", "url": "https://www.pttime.org"},
        ]
    }