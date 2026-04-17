from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from datetime import date
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/", response_model=list[schemas.TransactionOut])
def list_transactions(
    type: Optional[str] = None,
    category: Optional[str] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    q = db.query(models.Transaction).filter(models.Transaction.user_id == user.id)
    if type:
        q = q.filter(models.Transaction.type == type)
    if category:
        q = q.filter(models.Transaction.category == category)
    if month:
        q = q.filter(models.Transaction.date.extract("month") == month)  # type: ignore
    if year:
        q = q.filter(models.Transaction.date.extract("year") == year)  # type: ignore
    return q.order_by(desc(models.Transaction.date)).limit(limit).all()

@router.post("/", response_model=schemas.TransactionOut, status_code=201)
def create_transaction(
    body: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    tx = models.Transaction(**body.model_dump(), user_id=user.id)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

@router.delete("/{tx_id}", status_code=204)
def delete_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    tx = db.query(models.Transaction).filter(
        models.Transaction.id == tx_id,
        models.Transaction.user_id == user.id
    ).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(tx)
    db.commit()

@router.get("/categories", response_model=list[str])
def get_categories(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    rows = db.query(models.Transaction.category).filter(
        models.Transaction.user_id == user.id
    ).distinct().all()
    return [r[0] for r in rows]
