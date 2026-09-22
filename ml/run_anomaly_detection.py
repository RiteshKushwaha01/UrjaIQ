from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from anomaly_detector import train_anomaly_detector, detect_anomalies


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)


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
    telemetry = load_telemetry(limit)

    if telemetry.empty:
        return telemetry

    model = train_anomaly_detector(telemetry)

    return detect_anomalies(model, telemetry)


if __name__ == "__main__":
    results = get_anomaly_results()

    anomalies = (
        results[results["anomaly_prediction"] == -1]
        .sort_values("anomaly_score")
    )

    print(f"Total records: {len(results)}")
    print(f"Anomalies: {len(anomalies)}")

    print("\nLatest anomalies:")

    print(
        anomalies[
            [
                "timestamp",
                "machine_id",
                "machine_type",
                "power_kw",
                "temperature",
                "vibration",
                "operating_state",
                "anomaly_score",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )