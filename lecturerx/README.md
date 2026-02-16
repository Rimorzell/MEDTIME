# LectureRx Monorepo

LectureRx is a full-stack web application for medical students to upload lecture files and process them into board-focused study assets.

## Structure

- `frontend/`: Next.js 14 + TypeScript + Tailwind + Clerk
- `backend/`: FastAPI + SQLAlchemy + Celery + Redis
- `docker-compose.yml`: Local PostgreSQL (pgvector) + Redis services

## Quickstart

1. Copy env examples:
   - `cp frontend/.env.local.example frontend/.env.local`
   - `cp backend/.env.example backend/.env`
2. Start infrastructure:
   - `docker compose up -d`
3. Run backend:
   - `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`
4. Run frontend:
   - `cd frontend && npm install && npm run dev`
