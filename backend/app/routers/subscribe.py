"""订阅管理 API"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.subscribe import Subscribe

router = APIRouter()


@router.get("/subscribes")
async def list_subscribes(db: Session = Depends(get_db)):
    """获取订阅列表"""
    items = db.query(Subscribe).all()
    return {"items": items, "total": len(items)}


@router.post("/subscribes")
async def create_subscribe(keyword: str, actor: str = "", db: Session = Depends(get_db)):
    """创建订阅"""
    sub = Subscribe(keyword=keyword, actor=actor)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


@router.delete("/subscribes/{subscribe_id}")
async def delete_subscribe(subscribe_id: int, db: Session = Depends(get_db)):
    """删除订阅"""
    sub = db.query(Subscribe).filter(Subscribe.id == subscribe_id).first()
    if sub:
        db.delete(sub)
        db.commit()
    return {"ok": True}


@router.patch("/subscribes/{subscribe_id}/toggle")
async def toggle_subscribe(subscribe_id: int, db: Session = Depends(get_db)):
    """启用/禁用订阅"""
    sub = db.query(Subscribe).filter(Subscribe.id == subscribe_id).first()
    if sub:
        sub.enabled = not sub.enabled
        db.commit()
    return {"ok": True}