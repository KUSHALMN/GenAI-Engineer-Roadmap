# AI Auth API — Day 12

FastAPI + PostgreSQL + JWT Authentication API.

## Architecture

```
config.py    ← all settings (DB URL, JWT secret, expiry)
models.py    ← Pydantic request/response models
database.py  ← PostgreSQL connection + CRUD
auth.py      ← password hashing, JWT create/verify
routes.py    ← API endpoints (register, login, me)
app.py       ← FastAPI app entry point
```

## Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Health check | ❌ |
| POST | `/auth/register` | Register new user | ❌ |
| POST | `/auth/login` | Login, get JWT token | ❌ |
| GET | `/auth/me` | Get current user | ✅ |

## Setup

```bash
pip install -r requirements.txt
```

Create `.env`:
```
DATABASE_URL=postgresql://postgres:password@localhost/ai_auth_db
SECRET_KEY=your-secret-key-here
```

## Run

```bash
uvicorn app:app --reload
```

Visit `http://127.0.0.1:8000/docs` for Swagger UI.

## Auth Flow

```
POST /auth/register → create user with hashed password
POST /auth/login    → verify password → return JWT token
GET  /auth/me       → verify JWT → return user info
```
