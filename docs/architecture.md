# Architecture Overview – Miner Bitaxe Dashboard

## Components

- FastAPI backend  
  Exposes REST API endpoints, fetches data from the Bitaxe miner, stores data in PostgreSQL, and serves crypto prices.

- React + Vite frontend  
  Displays miner metrics, charts, history and price information in a web UI.

- Background scheduler (inside backend)  
  Periodically polls the Bitaxe miner and writes records into the database.

- PostgreSQL database  
  Stores persistent miner telemetry (`miner_status` table).

## Data Flow

1. Scheduler calls the Bitaxe HTTP API (`/api/system/info`) on the local network.
2. FastAPI parses the JSON payload and validates it using Pydantic models.
3. A new row is written into the `miner_status` table in PostgreSQL.
4. The frontend calls:
   - `/api/miner/status` for the latest status
   - `/api/miner/history` for historical data
   - `/api/crypto/prices` for BTC/ETH prices
5. The UI updates the dashboard with the latest values.
