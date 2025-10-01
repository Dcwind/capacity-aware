# Context-Aware WOP – Leave Planner (MVP)

Beautiful, responsive Next.js 14 + Tailwind + shadcn/ui + Framer Motion frontend with a Python FastAPI backend and Temporal (Python SDK) workflow for leave requests.

## Dev Setup

### Prerequisites
- Node 18+ and pnpm
- Python 3.11+
- Docker (for Temporal dev)

### Environment
- Set `NEXT_PUBLIC_API_URL=http://localhost:8000`

### Frontend
```bash
cd apps/web
pnpm i
pnpm dlx shadcn-ui init -y
pnpm dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Temporal
```bash
cd temporal
docker compose up -d
python ../backend/app/temporal/worker.py
```

## Repo Structure
```
repo/
  apps/web/                 # Next.js frontend
  backend/                  # FastAPI + SQLModel + Temporal SDK
  temporal/                 # Temporal dev docker compose
```

## Notes
- Timers shortened to 48s/72s for demo in dev.
- SQLite via SQLModel; Alembic migrations.
- Audit logs planned; minimal stub in MVP.

