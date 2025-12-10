
# Bitaxe Gamma 601 – Home Miner Dashboard

Full-stack example project:

- Backend: **FastAPI** (Python) – talks to the Bitaxe AxeOS REST API
- Frontend: **React + Vite** – dashboard UI

## Structure

- `backend/` – FastAPI app (`/api/miner/status`, `/api/miner/history`)
- `frontend/` – React + Vite app (cards + hashrate history chart)

## Quick start

1. **Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```env
BITAXE_BASE_URL=http://192.168.1.123
```

Then run:

```bash
uvicorn main:app --reload --port 8000
```

2. **Frontend**

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the URL Vite prints (usually `http://localhost:5173`).

The UI will poll:

- `GET /api/miner/status` every 3 seconds
- `GET /api/miner/history` every 10 seconds
```

