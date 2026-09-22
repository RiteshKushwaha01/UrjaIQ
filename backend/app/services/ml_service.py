from pathlib import Path
import os
import time

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.ml.anomaly_detector import (
    train_anomaly_detector,
    detect_anomalies,
)


ROOT_DIR = Path(__file__).resolve().parents[3]

load_dotenv(ROOT_DIR / ".env")


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


MODEL_REFRESH_SECONDS = 60

_cached_model = None
_model_created_at = 0.0


def load_telemetry(limit: int = 500) -> pd.DataFrame:
    query = f"""
        SELECT
            timestamp,
            machine_id,
            machine_type,
            power_kw,
            temperature,
            vibration,
            voltage,
            current,
            operating_state
        FROM telemetry
        ORDER BY timestamp DESC
        LIMIT {limit}
    """

    return pd.read_sql(query, engine)


def get_anomaly_results(limit: int = 500) -> pd.DataFrame:
    global _cached_model
    global _model_created_at

    telemetry = load_telemetry(limit)

    if telemetry.empty:
        return telemetry

    current_time = time.monotonic()

    model_expired = (
        _cached_model is None
        or current_time - _model_created_at >= MODEL_REFRESH_SECONDS
    )

    if model_expired:
        _cached_model = train_anomaly_detector(telemetry)
        _model_created_at = current_time

    return detect_anomalies(
        _cached_model,
        telemetry,
    )