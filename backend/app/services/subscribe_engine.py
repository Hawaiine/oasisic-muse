"""订阅引擎 — 定时搜索 + 安全下载"""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..config import settings
from ..database import SessionLocal
from ..models.subscribe import DownloadTask, Subscribe
from ..services.downloader import DownloaderService
from ..services.media_library import MediaLibraryService
from ..services.notifier import NotifierService
from ..services.pt_search import PTSearchService
from ..services.pt_sites.base import TorrentResult

logger = logging.getLogger(__name__)


@dataclass
class SubscribeLimits:
    """订阅安全限制"""
    # 全局
    max_daily_downloads: int = 10       # 每日最大下载数
    max_concurrent_downloads: int = 3   # 最大同时下载数
    disk_threshold_gb: int = 50         # 磁盘剩余空间阈值(GB)
    site_interval_minutes: int = 30     # 站点检查最小间隔(分钟)

    # 单文件
    min_size_gb: float = 0.5            # 最小文件大小(GB)
    max_size_gb: float = 20.0           # 最大文件大小(GB)
    min_seeders: int = 1                # 最少做种数

    # 过滤
    freeleech_only: bool = False        # 仅下载免费资源
    enabled: bool = True                # 总开关


class SubscribeEngine:
    """订阅引擎"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.limits = SubscribeLimits()
        self._daily_count = 0
        self._last_reset_date = datetime.now(timezone.utc).date()
        self.notifier = NotifierService()

    async def check_and_download(self):
        """检查所有订阅并下载"""
        if not self.limits.enabled:
            logger.info("订阅引擎已禁用")
            return

        # 重置每日计数
        today = datetime.now(timezone.utc).date()
        if today != self._last_reset_date:
            self._daily_count = 0
            self._last_reset_date = today

        # 检查每日限制
        if self._daily_count >= self.limits.max_daily_downloads:
            logger.info("今日下载已达上限 (%d)", self.limits.max_daily_downloads)
            return

        # 检查磁盘空间
        if not self._check_disk_space():
            logger.warning("磁盘空间不足，跳过下载")
            return

        # 检查并发下载数
        active = self._count_active_downloads()
        if active >= self.limits.max_concurrent_downloads:
            logger.info("并发下载已达上限 (%d)", active)
            return

        # 获取所有启用的订阅
        db = SessionLocal()
        try:
            subscribes = db.query(Subscribe).filter(Subscribe.enabled == True).all()  # noqa: E712
        finally:
            db.close()

        if not subscribes:
            logger.info("无启用的订阅")
            return

        logger.info("开始检查 %d 个订阅", len(subscribes))
        service = PTSearchService()

        for sub in subscribes:
            try:
                results = await service.search_subscribe(sub.keyword, sub.actor or "")

                # 过滤结果
                filtered = self._filter_results(results)

                if filtered:
                    best = filtered[0]
                    # 检查已下载
                    if self._is_already_downloaded(best.title):
                        logger.info("已下载过: %s", best.title)
                        continue

                    # 添加到下载
                    success = await self._add_download(best, sub.id)
                    if success:
                        self._daily_count += 1
                        logger.info("✅ 已添加下载: %s (%s)", best.title, best.site)

                        # 通知
                        await self.notifier.send(
                            title="📥 新下载任务",
                            message=f"{best.title}\n站点: {best.site_name}\n大小: {best.size}",
                            level="info",
                        )

                        if self._daily_count >= self.limits.max_daily_downloads:
                            break

                # 订阅级冷却
                await asyncio.sleep(5)

            except Exception as e:
                logger.error("订阅检查失败 (%s): %s", sub.keyword, e)
                continue

    def _filter_results(self, results: list[TorrentResult]) -> list[TorrentResult]:
        """过滤结果"""
        filtered = []
        for r in results:
            # 做种数过滤
            if r.seeders < self.limits.min_seeders:
                continue

            # 大小过滤（如果能解析到大小）
            if r.size:
                size_gb = self._parse_size_to_gb(r.size)
                if size_gb is not None:
                    if size_gb < self.limits.min_size_gb:
                        continue
                    if size_gb > self.limits.max_size_gb:
                        continue

            filtered.append(r)

        # 按做种数降序（选最活跃的种子）
        filtered.sort(key=lambda r: r.seeders, reverse=True)
        return filtered

    async def _add_download(self, result: TorrentResult, subscribe_id: int) -> bool:
        """添加下载任务"""
        if not result.torrent_url:
            logger.warning("无下载链接: %s", result.title)
            return False

        downloader = DownloaderService()
        r = await downloader.add_torrent(result.torrent_url)

        # 记录到数据库
        db = SessionLocal()
        try:
            task = DownloadTask(
                subscribe_id=subscribe_id,
                title=result.title,
                site=result.site,
                torrent_url=result.torrent_url,
                status="pending" if r.get("success") else "failed",
            )
            db.add(task)
            db.commit()
        except Exception as e:
            logger.error("记录下载任务失败: %s", e)
        finally:
            db.close()

        return r.get("success", False)

    def _is_already_downloaded(self, title: str) -> bool:
        """检查是否已下载过"""
        db = SessionLocal()
        try:
            existing = db.query(DownloadTask).filter(
                DownloadTask.title.ilike(f"%{title[:30]}%")
            ).first()
            return existing is not None
        finally:
            db.close()

    @staticmethod
    def _count_active_downloads() -> int:
        """当前活跃下载数"""
        db = SessionLocal()
        try:
            return db.query(DownloadTask).filter(
                DownloadTask.status.in_(["pending", "downloading"])
            ).count()
        finally:
            db.close()

    @staticmethod
    def _check_disk_space() -> bool:
        """检查磁盘空间"""
        try:
            data_dir = settings.database_url.replace("sqlite:///", "")
            usage = shutil.disk_usage(os.path.dirname(data_dir) or "/data")
            free_gb = usage.free / (1024 ** 3)
            limits = SubscribeLimits()
            return free_gb > limits.disk_threshold_gb
        except Exception:
            return True

    @staticmethod
    def _parse_size_to_gb(size_str: str) -> float | None:
        """解析大小字符串到 GB"""
        try:
            size_str = size_str.upper().strip()
            if "TB" in size_str:
                return float(size_str.replace("TB", "").strip()) * 1024
            if "GB" in size_str:
                return float(size_str.replace("GB", "").strip())
            if "MB" in size_str:
                return float(size_str.replace("MB", "").strip()) / 1024
            return None
        except (ValueError, AttributeError):
            return None

    def start(self):
        """启动调度器"""
        # 每60分钟检查一次订阅
        self.scheduler.add_job(
            self.check_and_download,
            "interval",
            minutes=60,
            id="subscribe_check",
            max_instances=1,
        )
        self.scheduler.start()
        logger.info("订阅引擎已启动 (间隔: 60分钟, 每日上限: %d)", self.limits.max_daily_downloads)

    def stop(self):
        """停止调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            logger.info("订阅引擎已停止")