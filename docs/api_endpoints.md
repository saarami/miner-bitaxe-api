# API Endpoints – Miner Bitaxe Dashboard

## GET /api/health
Returns basic service health status.

### Example response
{
  "status": "ok"
}

---

## GET /api/miner/status
Returns the latest miner status stored in the database (pulled by the scheduler).

Fields include:
- `timestamp` (UTC datetime)
- `online` (boolean)
- `hash_rate`
- `temp_core`
- `temp_vr`
- `best_difficulty`
- `shares_accepted`
- `shares_rejected`
- `frequency`
- `core_voltage`
- `raw` (full JSON from the miner)

---

## GET /api/miner/history?limit={n}
Returns the last *n* records from the in-memory history buffer.

Query parameters:
- `limit` – optional, default 200, max 2000

---

## GET /api/crypto/prices
Returns current BTC and ETH prices in USD (fetched from CoinGecko).

Fields:
- `btc_usd`
- `eth_usd`
- `last_updated`
