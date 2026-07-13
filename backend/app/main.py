"""Oasisic Muse — FastAPI 主入口"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import init_db
from .routers import about, subscribe, download, settings as settings_router, notify

app = FastAPI(
    title="Oasisic Muse",
    description="AV 自动化刮削下载工具",
    version="0.1.0",
    docs_url="/api/docs" if settings.debug else None,
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
app.include_router(settings_router.router, prefix="/api", tags=["设置"])
app.include_router(notify.router, prefix="/api", tags=["通知"])


@app.on_event("startup")
async def startup():
    """初始化"""
    # 确保数据目录存在
    Path(settings.database_url.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)
    init_db()


# 静态文件（Vue 构建产物）
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}