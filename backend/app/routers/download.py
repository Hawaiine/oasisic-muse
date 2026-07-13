"""下载任务 API"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.subscribe import DownloadTask

router = APIRouter()


@router.get("/downloads")
async def list_downloads(db: Session = Depends(get_db)):
    """获取下载列表"""
    items = db.query(DownloadTask).order_by(DownloadTask.created_at.desc()).all()
    return {"items": items, "total": len(items)}


@router.get("/downloads/stats")
async def download_stats(db: Session = Depends(get_db)):
    """下载统计"""
    total = db.query(DownloadTask).count()
    done = db.query(DownloadTask).filter(DownloadTask.status == "done").count()
    downloading = db.query(DownloadTask).filter(DownloadTask.status == "downloading").count()
    pending = db.query(DownloadTask).filter(DownloadTask.status == "pending").count()
    return {"total": total, "done": done, "downloading": downloading, "pending": pending}


@router.delete("/downloads/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """删除下载任务"""
    task = db.query(DownloadTask).filter(DownloadTask.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return {"ok": True}