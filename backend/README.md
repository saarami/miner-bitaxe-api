
# Backend – Bitaxe Dashboard API (FastAPI)

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configure miner IP

Create a file named `.env` in this folder:

```env
BITAXE_BASE_URL=http://192.168.1.123
```

(Replace with the actual IP of your Bitaxe Gamma 601.)

## Run

```bash
uvicorn main:app --reload --port 8000
```

API will be available at: `http://localhost:8000`
