from fastapi import APIRouter

from app.services.ml_service import get_anomaly_results


router = APIRouter(
    prefix="/api/ml",
    tags=["ML"],
)


@router.get("/anomalies")
def get_anomalies(limit: int = 10):
    results = get_anomaly_results()

    if results.empty:
        return []

    # Get the latest telemetry record for each machine.
    latest_by_machine = (
        results
        .sort_values("timestamp", ascending=False)
        .drop_duplicates(subset=["machine_id"], keep="first")
    )

    # Keep only machines whose latest reading is anomalous.
    anomalies = latest_by_machine[
        latest_by_machine["anomaly_prediction"] == -1
    ]

    anomalies = (
        anomalies
        .sort_values("anomaly_score")
        .head(limit)
    )

    return [
        {
            "timestamp": row["timestamp"].isoformat(),
            "machine_id": row["machine_id"],
            "machine_type": row["machine_type"],
            "power_kw": round(float(row["power_kw"]), 2),
            "temperature": round(float(row["temperature"]), 2),
            "vibration": round(float(row["vibration"]), 2),
            "operating_state": row["operating_state"],
            "anomaly_score": round(float(row["anomaly_score"]), 4),
        }
        for _, row in anomalies.iterrows()
    ]