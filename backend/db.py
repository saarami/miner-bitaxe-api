from sqlalchemy import create_engine, Column, Integer, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from pydantic_settings import BaseSettings  # 👈 חשוב


class DBSettings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"   # 👈 יתעלם מ-BITAXE_BASE_URL וכו'


settings = DBSettings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class MinerStatusRecord(Base):
    __tablename__ = "miner_status"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    online = Column(Boolean, nullable=False)

    hash_rate = Column(Float, nullable=True)
    temp_core = Column(Float, nullable=True)
    temp_vr = Column(Float, nullable=True)
    best_difficulty = Column(Float, nullable=True)
    shares_accepted = Column(Integer, nullable=True)
    shares_rejected = Column(Integer, nullable=True)
    frequency = Column(Float, nullable=True)
    core_voltage = Column(Float, nullable=True)

    raw = Column(JSONB, nullable=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
