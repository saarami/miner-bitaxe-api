
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional, List
from datetime import datetime, timedelta
from collections import deque
import httpx
from db import get_db, MinerStatusRecord, init_db, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import desc
import asyncio




class Settings(BaseSettings):
    BITAXE_BASE_URL: str = "http://192.168.1.132"  # change to your miner IP
    COINGECKO_API_BASE: str = "https://api.coingecko.com/api/v3"
    COINGECKO_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"  # 👈 חשוב!



settings = Settings()

app = FastAPI(title="Bitaxe Gamma 601 Dashboard API")

@app.on_event("startup")
async def on_startup():
    init_db()
    asyncio.create_task(miner_polling_loop())



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MinerStatus(BaseModel):
    timestamp: datetime
    online: bool
    hash_rate: Optional[float] = None
    temp_core: Optional[float] = None
    temp_vr: Optional[float] = None
    best_difficulty: Optional[float] = None
    shares_accepted: Optional[int] = None
    shares_rejected: Optional[int] = None
    frequency: Optional[float] = None
    core_voltage: Optional[float] = None
    raw: dict

class CryptoPrices(BaseModel):
    btc_usd: float
    eth_usd: float
    last_updated: datetime

last_prices: CryptoPrices | None = None
last_prices_time: datetime | None = None


# simple in-memory history buffer
HISTORY_LIMIT = 2000
POLL_INTERVAL_SECONDS = 5  # כל כמה שניות למשוך מהכורה
history_buffer: deque[MinerStatus] = deque(maxlen=HISTORY_LIMIT)

@app.get("/api/health")
async def health():
    return {"status": "ok"}

async def fetch_miner_info() -> MinerStatus:
    url = f"{settings.BITAXE_BASE_URL.rstrip('/')}/api/system/info"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        # if we have history, return last with online=False
        if history_buffer:
            last = history_buffer[-1]
            return MinerStatus(
                **last.dict(exclude={"online"}),
                online=False,
            )
        raise HTTPException(status_code=503, detail=f"Failed to reach miner: {e}")

    # map AxeOS fields -> our model (keys may vary by version, adjust if needed)
    status = MinerStatus(
        timestamp=datetime.utcnow(),
        online=True,
        hash_rate=data.get("hashRate") or data.get("hashrate"),
        temp_core=data.get("temp"),
        temp_vr=data.get("vrTemp"),
        best_difficulty=data.get("bestDiff") or data.get("bestDifficulty"),
        shares_accepted=data.get("sharesAccepted"),
        shares_rejected=data.get("sharesRejected"),
        frequency=data.get("frequency"),
        core_voltage=data.get("coreVoltageActual") or data.get("coreVoltage"),
        raw=data,
    )
    history_buffer.append(status)
    return status

async def miner_polling_loop():
    # ניתן זמן לשרת לעלות
    await asyncio.sleep(2)

    while True:
        try:
            status = await fetch_miner_info()
        except Exception as e:
            # פה אפשר להוסיף logging אם תרצה
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
            continue

        db = SessionLocal()
        try:
            record = MinerStatusRecord(
                timestamp=status.timestamp,
                online=status.online,
                hash_rate=status.hash_rate,
                temp_core=status.temp_core,
                temp_vr=status.temp_vr,
                best_difficulty=status.best_difficulty,
                shares_accepted=status.shares_accepted,
                shares_rejected=status.shares_rejected,
                frequency=status.frequency,
                core_voltage=status.core_voltage,
                raw=status.raw,
            )
            db.add(record)
            db.commit()
        except Exception:
            db.rollback()
            # אפשר להוסיף logging
        finally:
            db.close()

        await asyncio.sleep(POLL_INTERVAL_SECONDS)

async def fetch_crypto_prices() -> CryptoPrices:
    global last_prices, last_prices_time

    base = settings.COINGECKO_API_BASE.rstrip("/")
    url = f"{base}/simple/price"

    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd",
    }

    headers = {}
    if settings.COINGECKO_API_KEY:
        # אם בעתיד יהיה לך מפתח – אפשר לשלוח אותו פה
        headers["x-cg-demo-api-key"] = settings.COINGECKO_API_KEY

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=params, headers=headers)
        print("COINGECKO STATUS:", resp.status_code)
        print("COINGECKO BODY:", resp.text[:300])
        resp.raise_for_status()
        data = resp.json()

    btc = data["bitcoin"]["usd"]
    eth = data["ethereum"]["usd"]

    prices = CryptoPrices(
        btc_usd=btc,
        eth_usd=eth,
        last_updated=datetime.utcnow(),
    )

    # נשמור בזיכרון את הערך האחרון התקין
    last_prices = prices
    last_prices_time = prices.last_updated
    return prices


@app.get("/api/miner/status", response_model=MinerStatus)
async def get_miner_status(db: Session = Depends(get_db)):
    # לוקחים את הרשומה האחרונה מה-DB
    record = (
        db.query(MinerStatusRecord)
        .order_by(MinerStatusRecord.timestamp.desc())
        .first()
    )

    if record is None:
        # עדיין אין מדידות – אפשר להחזיר 503 או אובייקט offline
        raise HTTPException(status_code=503, detail="No miner data yet")

    status = MinerStatus(
        timestamp=record.timestamp,
        online=record.online,
        hash_rate=record.hash_rate,
        temp_core=record.temp_core,
        temp_vr=record.temp_vr,
        best_difficulty=record.best_difficulty,
        shares_accepted=record.shares_accepted,
        shares_rejected=record.shares_rejected,
        frequency=record.frequency,
        core_voltage=record.core_voltage,
        raw=record.raw or {},
    )
    return status



@app.get("/api/miner/history", response_model=List[MinerStatus])
async def get_miner_history(
    limit: int = 200,
    db: Session = Depends(get_db),
):
    if limit <= 0:
        limit = 1
    if limit > HISTORY_LIMIT:
        limit = HISTORY_LIMIT

    # newest first מה־DB
    records = (
        db.query(MinerStatusRecord)
        .order_by(MinerStatusRecord.timestamp.desc())
        .limit(limit)
        .all()
    )

    # נהפוך לרשימת MinerStatus (oldest → newest)
    items: List[MinerStatus] = []
    for r in reversed(records):
        items.append(
            MinerStatus(
                timestamp=r.timestamp,
                online=r.online,
                hash_rate=r.hash_rate,
                temp_core=r.temp_core,
                temp_vr=r.temp_vr,
                best_difficulty=r.best_difficulty,
                shares_accepted=r.shares_accepted,
                shares_rejected=r.shares_rejected,
                frequency=r.frequency,
                core_voltage=r.core_voltage,
                raw=r.raw or {},
            )
        )

    return items


# add btc and eth prices:

@app.get("/api/crypto/prices", response_model=CryptoPrices)
async def get_crypto_prices():
    global last_prices, last_prices_time
    try:
        return await fetch_crypto_prices()
    except Exception as e:
        print("CRYPTO ERROR:", repr(e))

        # אם יש ערך אחרון תקין מה-5 דקות האחרונות – נחזיר אותו במקום 502
        if last_prices and last_prices_time and datetime.utcnow() - last_prices_time < timedelta(minutes=5):
            return last_prices

        # אם אין שום ערך תקין – נחזיר 502
        raise HTTPException(status_code=502, detail=f"Failed to fetch crypto prices: {e}")

# Entry point for uvicorn: uvicorn main:app --reload
