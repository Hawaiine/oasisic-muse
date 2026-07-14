"""安全限制 API — 订阅引擎参数"""

from __future__ import annotations

from fastapi import APIRouter

from ..services.subscribe_engine import engine

router = APIRouter()


@router.get("/limits")
async def get_limits():
    """获取当前安全限制配置"""
    l = engine.limits
    return {
        "max_daily_downloads": l.max_daily_downloads,
        "max_concurrent_downloads": l.max_concurrent_downloads,
        "disk_threshold_gb": l.disk_threshold_gb,
        "site_interval_minutes": l.site_interval_minutes,
        "min_size_gb": l.min_size_gb,
        "max_size_gb": l.max_size_gb,
        "min_seeders": l.min_seeders,
        "freeleech_only": l.freeleech_only,
        "enabled": l.enabled,
        "today_downloaded": engine._daily_count,
        "active_downloads": engine._count_active_downloads(),
    }


@router.post("/limits")
async def update_limits(
    max_daily_downloads: int | None = None,
    max_concurrent_downloads: int | None = None,
    disk_threshold_gb: int | None = None,
    min_size_gb: float | None = None,
    max_size_gb: float | None = None,
    min_seeders: int | None = None,
    freeleech_only: bool | None = None,
    enabled: bool | None = None,
):
    """更新安全限制"""
    l = engine.limits
    if max_daily_downloads is not None:
        l.max_daily_downloads = max(1, max_daily_downloads)
    if max_concurrent_downloads is not None:
        l.max_concurrent_downloads = max(1, max_concurrent_downloads)
    if disk_threshold_gb is not None:
        l.disk_threshold_gb = max(1, disk_threshold_gb)
    if min_size_gb is not None:
        l.min_size_gb = min_size_gb
    if max_size_gb is not None:
        l.max_size_gb = max_size_gb
    if min_seeders is not None:
        l.min_seeders = min_seeders
    if freeleech_only is not None:
        l.freeleech_only = freeleech_only
    if enabled is not None:
        l.enabled = enabled

    return {"updated": True, **await get_limits()}


@router.post("/limits/run-now")
async def run_engine_now():
    """立即执行一次订阅检查"""
    import asyncio
    asyncio.create_task(engine.check_and_download())
    return {"started": True}