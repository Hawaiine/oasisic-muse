"""订阅模型"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from ..database import Base


class Subscribe(Base):
    """订阅规则"""

    __tablename__ = "subscribes"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), comment="搜索关键词 / 番号")
    actor = Column(String(255), comment="演员")
    category = Column(String(50), default="all", comment="分类")
    quality = Column(String(50), default="HD", comment="画质偏好")
    enabled = Column(Boolean, default=True)
    interval = Column(Integer, default=3600, comment="检查间隔(秒)")
    last_check = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DownloadTask(Base):
    """下载任务"""

    __tablename__ = "download_tasks"

    id = Column(Integer, primary_key=True, index=True)
    subscribe_id = Column(Integer, nullable=True)
    title = Column(String(500))
    site = Column(String(50))
    torrent_url = Column(Text)
    status = Column(String(20), default="pending")  # pending/downloading/seeding/done/failed
    progress = Column(Integer, default=0)
    qb_hash = Column(String(100), nullable=True)
    save_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))