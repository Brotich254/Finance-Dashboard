# FinFlow — Finance Dashboard

FastAPI (Python) + Vue 3 + PostgreSQL.

## Stack
- Backend: Python, FastAPI, SQLAlchemy, Pydantic v2, JWT (python-jose), bcrypt
- Frontend: Vue 3, Vite, Pinia, Tailwind, Chart.js (vue-chartjs)
- Database: PostgreSQL

## Setup

### Prerequisites
- Python 3.11+, pip
- PostgreSQL
- Node.js 18+

### Database
```bash
psql -U postgres -c "CREATE DATABASE finance_dashboard;"
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in your values
uvicorn app.main:app --reload   # runs on port 8000
# Tables created automatically on first run
```

### Frontend
```bash
cd frontend
npm install
npm run dev   # runs on port 5173
```

## Features
- Transaction tracking (income & expense) with categories, dates, notes
- Filter transactions by type, category, month
- Monthly budgets per category with progress bars (green/yellow/red)
- Dashboard with 6-month income vs expense bar chart
- Spending breakdown by category with percentage bars
- Total balance, monthly income/expenses/savings stats
- JWT auth with Pinia state management
