"""搜索 API — 对接 PT 站点"""

from __future__ import annotations

from fastapi import APIRouter

from ..services.pt_search import PTSearchService

router = APIRouter()


@router.get("/search")
async def search_pt(keyword: str = "", actor: str = ""):
    """搜索 PT 站点"""
    service = PTSearchService()
    if actor:
        results = await service.search_subscribe(keyword, actor)
    else:
        results = await service.search_all(keyword)

    return {
        "items": [r.__dict__ for r in results],
        "total": len(results),
    }


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