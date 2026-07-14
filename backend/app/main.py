"""Oasisic Muse — FastAPI 主入口"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import init_db
from .routers import about, subscribe, download, library, settings as settings_router, notify, search, limits, health
from .services.subscribe_engine import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    # 启动
    Path(settings.database_url.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)
    init_db()
    engine.start()
    logger.info("Oasisic Muse 启动完成")
    yield
    # 关闭
    engine.stop()
    logger.info("Oasisic Muse 关闭")


app = FastAPI(
    title="Oasisic Muse",
    description="AV 自动化刮削下载工具",
    version="0.3.0",
    docs_url="/api/docs" if settings.debug else None,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(about.router, prefix="/api", tags=["关于"])
app.include_router(subscribe.router, prefix="/api", tags=["订阅"])
app.include_router(download.router, prefix="/api", tags=["下载"])
app.include_router(library.router, prefix="/api", tags=["媒体库"])
app.include_router(settings_router.router, prefix="/api", tags=["设置"])
app.include_router(notify.router, prefix="/api", tags=["通知"])
app.include_router(search.router, prefix="/api", tags=["搜索"])
app.include_router(limits.router, prefix="/api", tags=["安全限制"])
app.include_router(health.router, prefix="/api", tags=["连通性检测"])


# 静态文件
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.3.0", "engine_running": engine.scheduler.running}