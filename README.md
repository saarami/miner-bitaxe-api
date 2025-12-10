# Miner Bitaxe Dashboard (FastAPI + React + PostgreSQL)

A full-stack monitoring dashboard for the Bitaxe Gamma 601 Bitcoin miner.  
The system collects real-time miner telemetry, stores historical data in PostgreSQL, fetches crypto prices, and exposes everything through a clean REST API with a modern React/Vite frontend.

---

## 📌 Features

- Real-time miner status (hashrate, temperatures, voltage, shares)
- Background scheduler that continuously polls the Bitaxe device
- Persistent logging in PostgreSQL (`miner_status` table)
- Live BTC & ETH price integration (CoinGecko API)
- REST API built with FastAPI + Pydantic
- React + Vite frontend dashboard
- CURL examples + Postman collection with automated tests
- Documentation included under `docs/`

---

## 🏗 Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic / Pydantic Settings
- httpx
- Async background scheduler

### Frontend
- React + Vite
- Fetch API for real-time data updates

---

## 📁 Project Structure

```
backend/
frontend/
docs/
    api_endpoints.md
    curl_examples.md
    architecture.md
    database_schema.md
    environment_variables.md
    monitoring_alerts.md
    postman/
        miner-bitaxe-api.postman_collection.json
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd SoloLuck
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create `.env` file in backend/
Fill in your environment variables:

```
BITAXE_BASE_URL=http://192.168.1.132
COINGECKE_API_BASE=https://api.coingecko.com/api/v3
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/bitaxe_db
```

### 4. Start the backend
```bash
uvicorn main:app --reload
```

---

## 🚀 Frontend setup

```bash
cd frontend
npm install
npm run dev
```

UI available at:  
👉 http://localhost:5173

---

## 🧪 Testing the API

### Postman  
Import this collection:

`docs/postman/miner-bitaxe-api.postman_collection.json`

Includes:
- Health check
- Miner status
- History endpoint
- Crypto price endpoint
- Automated test scripts

### CURL examples  
See:  
`docs/curl_examples.md`

---

## 🗄 Database Schema  
Documented in:  
`docs/database_schema.md`

---

## 📚 API Documentation  
All endpoints documented in:  
`docs/api_endpoints.md`

FastAPI Swagger UI:  
👉 http://localhost:8000/docs  
FastAPI ReDoc UI:  
👉 http://localhost:8000/redoc

---

## 🧠 Architecture  
Full system architecture overview found in:  
`docs/architecture.md`

cs/monitoring_alerts.md`

---

## ✨ Author  
**Saar Amikam**  

