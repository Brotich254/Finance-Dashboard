from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard", response_model=schemas.DashboardStats)
def dashboard(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    now = date.today()
    month, year = now.month, now.year

    def sum_by_type(t, m=None, y=None):
        q = db.query(func.sum(models.Transaction.amount)).filter(
            models.Transaction.user_id == user.id,
            models.Transaction.type == t
        )
        if m: q = q.filter(extract("month", models.Transaction.date) == m)
        if y: q = q.filter(extract("year", models.Transaction.date) == y)
        return round(q.scalar() or 0.0, 2)

    total_income = sum_by_type("income")
    total_expenses = sum_by_type("expense")
    monthly_income = sum_by_type("income", month, year)
    monthly_expenses = sum_by_type("expense", month, year)

    # Category breakdown for current month expenses
    cat_rows = db.query(
        models.Transaction.category,
        func.sum(models.Transaction.amount).label("total")
    ).filter(
        models.Transaction.user_id == user.id,
        models.Transaction.type == "expense",
        extract("month", models.Transaction.date) == month,
        extract("year", models.Transaction.date) == year
    ).group_by(models.Transaction.category).order_by(func.sum(models.Transaction.amount).desc()).all()

    top_categories = []
    for row in cat_rows:
        pct = round((row.total / monthly_expenses * 100) if monthly_expenses > 0 else 0, 1)
        top_categories.append(schemas.CategoryBreakdown(
            category=row.category, amount=round(row.total, 2), percentage=pct
        ))

    # Monthly trend — last 6 months
    trend = []
    for i in range(5, -1, -1):
        m = (month - i - 1) % 12 + 1
        y = year - ((month - i - 1) // 12)
        inc = sum_by_type("income", m, y)
        exp = sum_by_type("expense", m, y)
        trend.append(schemas.MonthlySummary(month=m, year=y, income=inc, expenses=exp, net=round(inc - exp, 2)))

    return schemas.DashboardStats(
        total_balance=round(total_income - total_expenses, 2),
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        monthly_savings=round(monthly_income - monthly_expenses, 2),
        top_categories=top_categories,
        monthly_trend=trend
    )
