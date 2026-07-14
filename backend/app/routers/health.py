"""连通性检测 API"""

from __future__ import annotations

from fastapi import APIRouter

from ..services.connectivity import ConnectivityCheck

router = APIRouter()
checker = ConnectivityCheck()


@router.get("/health/connectivity")
async def check_connectivity():
    """检测所有服务连通性"""
    return await checker.check_all()


@router.get("/health/qb-version")
async def check_qb_version():
    """检测 qBittorrent API 版本兼容性"""
    from ..services.downloader import DownloaderService
    dl = DownloaderService()
    return await dl.check_version_compatibility()