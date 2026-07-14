"""Oasisic Muse 数据库 — SQLite"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def init_db():
    """初始化数据库表（线程安全）"""
    import logging
    logger = logging.getLogger(__name__)
    for attempt in range(3):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except Exception as e:
            if "already exists" in str(e):
                logger.debug("数据库表已存在（并发创建），跳过")
                return
            if attempt < 2:
                import time
                time.sleep(1)
            else:
                raise


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()