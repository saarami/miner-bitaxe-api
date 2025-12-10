# Miner Bitaxe API (FastAPI + React + Docker + PostgreSQL)

A production-ready full‑stack dashboard for monitoring a Bitaxe Gamma 601 Bitcoin miner.  
The system provides real‑time telemetry, historical logging, crypto price tracking, and a complete Docker deployment environment with Nginx reverse proxy.

---

## 🚀 Features

- Real‑time miner monitoring (hashrate, temperature, voltage, shares)
- Background scheduler that continuously collects stats
- PostgreSQL‑based historical logging
- FastAPI backend with Pydantic models
- React + Vite frontend served via Nginx
- Unified `/api/*` routing through reverse proxy (no CORS issues)
- CURL examples & Postman automated tests
- Full project documentation in the `/docs` directory

---

## 🏗 Architecture (Production Setup)

```
┌────────────┐      ┌──────────────┐
│  Frontend  │ ---> │   Backend    │ ---> Bitaxe Miner
│  (Nginx)   │      │  (FastAPI)   │
└────────────┘      └──────────────┘
       │                     │
       │                     └── PostgreSQL (logging)
       │
       └────── Browser (http://localhost)
```

---

## 📦 Running with Docker

Build and start all services:

```bash
docker compose build
docker compose up
```

Access the dashboard:

👉 http://localhost

---

## 🗂 Services Included

| Service   | Description                         | Port |
|-----------|-------------------------------------|-------|
| frontend  | React/Vite served by Nginx          | 80    |
| backend   | FastAPI + scheduler                 | internal: 8000 |
| db        | PostgreSQL 16 with persistent data  | internal: 5432 |

Reverse proxy from Nginx:
```
/api/*  →  backend:8000
```

---

## ⚙ Environment Variables

Create `.env` inside `backend/` for local dev:

```
BITAXE_BASE_URL=http://192.168.1.132
COINGECKO_API_BASE=https://api.coingecko.com/api/v3
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/bitaxe_db
```

In Docker, DATABASE_URL is automatically overridden inside `docker-compose.yml`.

---

## 🧪 Testing

### Postman Collection  
Located at:
```
docs/postman/miner-bitaxe-api.postman_collection.json
```

### CURL Examples  
Located at:
```
docs/curl_examples.md
```

---

## 📚 Documentation

Full documentation is located under the `/docs` directory:

- API endpoints  
- Architecture overview  
- Database schema  
- Environment variables  
- Scheduler & monitoring logic  
- CURL examples  
- Postman tests  

---

## 🛠 Local Development Mode

**Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Docker mode should *not* be combined with the dev servers.

---

## ✨ Author

**Saar Amikam**
