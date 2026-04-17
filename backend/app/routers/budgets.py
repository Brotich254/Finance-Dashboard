from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.get("/", response_model=list[schemas.BudgetWithSpent])
def list_budgets(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    budgets = db.query(models.Budget).filter(
        models.Budget.user_id == user.id,
        models.Budget.month == month,
        models.Budget.year == year
    ).all()

    result = []
    for b in budgets:
        spent = db.query(func.sum(models.Transaction.amount)).filter(
            models.Transaction.user_id == user.id,
            models.Transaction.category == b.category,
            models.Transaction.type == "expense",
            extract("month", models.Transaction.date) == month,
            extract("year", models.Transaction.date) == year
        ).scalar() or 0.0

        remaining = max(b.amount - spent, 0)
        percentage = min((spent / b.amount * 100) if b.amount > 0 else 0, 100)
        result.append(schemas.BudgetWithSpent(
            **{c.name: getattr(b, c.name) for c in b.__table__.columns},
            spent=round(spent, 2),
            remaining=round(remaining, 2),
            percentage=round(percentage, 1)
        ))
    return result

@router.post("/", response_model=schemas.BudgetOut, status_code=201)
def create_budget(
    body: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    # Upsert: update if exists for same category/month/year
    existing = db.query(models.Budget).filter(
        models.Budget.user_id == user.id,
        models.Budget.category == body.category,
        models.Budget.month == body.month,
        models.Budget.year == body.year
    ).first()

    if existing:
        existing.amount = body.amount
        db.commit()
        db.refresh(existing)
        return existing

    budget = models.Budget(**body.model_dump(), user_id=user.id)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

@router.delete("/{budget_id}", status_code=204)
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    b = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.user_id == user.id
    ).first()
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(b)
    db.commit()
