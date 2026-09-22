from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from anomaly_detector import train_anomaly_detector, detect_anomalies


# Load root .env
ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


# PostgreSQL connection
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{__import__('os').getenv('POSTGRES_USER')}:"
    f"{__import__('os').getenv('POSTGRES_PASSWORD')}@"
    f"{__import__('os').getenv('POSTGRES_HOST')}:"
    f"{__import__('os').getenv('POSTGRES_PORT')}/"
    f"{__import__('os').getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL)


# Load telemetry data
query = """
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
LIMIT 500
"""

telemetry = pd.read_sql(query, engine)

print(f"Loaded {len(telemetry)} telemetry records.")

if len(telemetry) < 20:
    print("Not enough telemetry data yet.")
    print("Keep the simulator running for a little longer.")
    raise SystemExit


# Train model
model = train_anomaly_detector(telemetry)

# Detect anomalies
results = detect_anomalies(model, telemetry)


# Display summary
anomaly_count = (
    results["anomaly_prediction"] == -1
).sum()

normal_count = (
    results["anomaly_prediction"] == 1
).sum()

print()
print("========== UrjaIQ Anomaly Detection ==========")
print(f"Normal records   : {normal_count}")
print(f"Anomaly records  : {anomaly_count}")
print(f"Total analyzed   : {len(results)}")

print()
print("Top anomaly scores:")
# print(
#     results[
#         [
#             "power_kw",
#             "temperature",
#             "vibration",
#             "voltage",
#             "current",
#             "anomaly_prediction",
#             "anomaly_score",
#         ]
#     ]
#     .sort_values("anomaly_score")
#     .head(10)
# )

anomalies = (
    results[results["anomaly_prediction"] == -1]
    .sort_values("anomaly_score")
)

print()
print("Top anomalies by machine:")

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
    ].head(10).to_string(index=False)
)