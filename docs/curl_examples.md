# CURL Examples – Miner Bitaxe Dashboard

## Health Check
curl.exe http://localhost:8000/api/health

## Miner Status
curl.exe http://localhost:8000/api/miner/status

## Miner History (20 entries)
curl.exe "http://localhost:8000/api/miner/history?limit=20"

## Crypto Prices
curl.exe http://localhost:8000/api/crypto/prices
