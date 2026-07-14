"""搜索 API — 对接 PT 站点"""

from __future__ import annotations

from fastapi import APIRouter

from ..services.pt_search import PTSearchService
from ..services.translate import TranslateService

router = APIRouter()
translator = TranslateService()


@router.get("/search")
async def search_pt(keyword: str = "", actor: str = "", category: str = "av", translate: bool = True):
    """搜索 PT 站点

    Args:
        keyword: 搜索关键词/番号
        actor: 演员名（可选）
        category: 分类，av=仅AV，all=全部
        translate: 是否翻译标题（日/英 → 中文）
    """
    service = PTSearchService()
    if actor:
        results = await service.search_subscribe(keyword, actor)
    else:
        results = await service.search_all(keyword)

    # 仅AV模式：过滤番号格式
    if category == "av":
        results = [r for r in results if _is_av_title(r.title)]

    items = [r.__dict__ for r in results]

    # 翻译标题
    if translate and items:
        titles = [item["title"] for item in items]
        translated = await translator.batch_translate(titles)
        for item, t_title in zip(items, translated):
            if t_title and t_title != item["title"]:
                item["title_cn"] = t_title
            else:
                item["title_cn"] = ""

    return {
        "items": items,
        "total": len(items),
        "category": category,
    }


def _is_av_title(title: str) -> bool:
    """判断标题是否包含AV番号特征"""
    import re
    return bool(re.search(r"[A-Z]{2,6}[-_\s]?\d{2,6}", title.upper()))


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