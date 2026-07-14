"""媒体库 API — Jellyfin + EMBY"""

from __future__ import annotations

from fastapi import APIRouter

from ..services.media_library import MediaLibraryService

router = APIRouter()
library_service = MediaLibraryService()


@router.get("/library/status")
async def library_status():
    """媒体库连接状态"""
    return await library_service.check_connection()


@router.post("/library/refresh")
async def refresh_library(item_id: str = ""):
    """刷新媒体库"""
    ok = await library_service.refresh_library(item_id or None)
    return {"success": ok}


@router.get("/library/recent")
async def recent_media(limit: int = 10):
    """最近添加的媒体"""
    items = await library_service.get_recent(limit)
    return {"items": items}


@router.get("/library/search")
async def search_library(name: str):
    """搜索媒体库"""
    items = await library_service.search_media(name)
    return {"items": items}