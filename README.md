# Case Tracking Application

- Full-stack case tracking app — create, list, edit, and close cases(backend) and login and get data(frontend) with role-based access (admin/user)
- Backend: FastAPI + PostgreSQL (SQLAlchemy, Alembic migrations, JWT auth)
- Frontend: Angular + TypeScript
- Run everything: `docker compose up -d --build`
- Backend API docs: http://localhost:8001/docs · Frontend: http://localhost:4200
- Tests: `pytest` in `backend/`, runs automatically via GitHub Actions on every push