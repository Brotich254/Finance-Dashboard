from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from app.models import TransactionType

# Auth
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

# Transactions
class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: TransactionType
    category: str
    date: date
    note: Optional[str] = None

class TransactionOut(TransactionCreate):
    id: int
    user_id: int
    model_config = {"from_attributes": True}

# Budgets
class BudgetCreate(BaseModel):
    category: str
    amount: float
    month: int
    year: int

class BudgetOut(BudgetCreate):
    id: int
    user_id: int
    model_config = {"from_attributes": True}

class BudgetWithSpent(BudgetOut):
    spent: float
    remaining: float
    percentage: float

# Analytics
class MonthlySummary(BaseModel):
    month: int
    year: int
    income: float
    expenses: float
    net: float

class CategoryBreakdown(BaseModel):
    category: str
    amount: float
    percentage: float

class DashboardStats(BaseModel):
    total_balance: float
    monthly_income: float
    monthly_expenses: float
    monthly_savings: float
    top_categories: list[CategoryBreakdown]
    monthly_trend: list[MonthlySummary]
