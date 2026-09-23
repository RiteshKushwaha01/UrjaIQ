import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.ml_service import get_anomaly_results


ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")


def get_factory_context(db: Session) -> dict:
    """
    Build a grounded snapshot of the current UrjaIQ factory state.
    """

    # ---------------------------------------------------------
    # FACTORY ANALYTICS
    # ---------------------------------------------------------

    analytics_query = text("""
        WITH valid_batches AS (
            SELECT
                batch_id,
                MIN(production_units) AS production_units,
                MIN(good_units) AS good_units,
                MIN(rejected_units) AS rejected_units,
                SUM(energy_kwh) AS total_energy_kwh
            FROM telemetry
            WHERE machine_id = 'Furnace-01'
            GROUP BY batch_id
            HAVING
                MAX(timestamp) - MIN(timestamp) >= INTERVAL '240 seconds'
                AND MIN(production_units) = MAX(production_units)
                AND MIN(good_units) = MAX(good_units)
                AND MIN(rejected_units) = MAX(rejected_units)
                AND MIN(production_units) =
                    MIN(good_units) + MIN(rejected_units)
                AND MIN(good_units) > 0
        )
        SELECT
            COUNT(*) AS batches_analyzed,
            COALESCE(SUM(total_energy_kwh), 0) AS total_energy_kwh,
            COALESCE(SUM(production_units), 0) AS production_units,
            COALESCE(SUM(good_units), 0) AS good_units,
            COALESCE(SUM(rejected_units), 0) AS rejected_units
        FROM valid_batches
    """)

    result = db.execute(analytics_query).mappings().one()

    batches = int(result["batches_analyzed"] or 0)
    total_energy = float(result["total_energy_kwh"] or 0)
    production_units = int(result["production_units"] or 0)
    good_units = int(result["good_units"] or 0)
    rejected_units = int(result["rejected_units"] or 0)

    quality_rate = (
        good_units / production_units * 100
        if production_units > 0
        else 0
    )

    sec = (
        total_energy / good_units
        if good_units > 0
        else 0
    )

    peak_power = float(
        db.execute(
            text("""
                SELECT COALESCE(MAX(power_kw), 0)
                FROM telemetry
            """)
        ).scalar()
        or 0
    )

    # ---------------------------------------------------------
    # LATEST MACHINE TELEMETRY
    # ---------------------------------------------------------

    latest_machine_query = text("""
        SELECT DISTINCT ON (machine_id)
            machine_id,
            machine_type,
            power_kw,
            temperature,
            vibration,
            voltage,
            current,
            operating_state,
            timestamp
        FROM telemetry
        ORDER BY machine_id, timestamp DESC
    """)

    latest_machines = db.execute(
        latest_machine_query
    ).mappings().all()

    machines = [
        {
            "machine_id": row["machine_id"],
            "machine_type": row["machine_type"],
            "power_kw": round(float(row["power_kw"]), 2),
            "temperature": round(float(row["temperature"]), 2),
            "vibration": round(float(row["vibration"]), 2),
            "voltage": round(float(row["voltage"]), 2),
            "current": round(float(row["current"]), 2),
            "operating_state": row["operating_state"],
            "timestamp": row["timestamp"].isoformat(),
        }
        for row in latest_machines
    ]

    # ---------------------------------------------------------
    # MACHINE ENERGY DISTRIBUTION
    # ---------------------------------------------------------

    machine_energy_query = text("""
        SELECT
            machine_id,
            machine_type,
            ROUND(SUM(energy_kwh)::numeric, 4) AS total_energy_kwh,
            ROUND(AVG(power_kw)::numeric, 2) AS average_power_kw,
            ROUND(MAX(power_kw)::numeric, 2) AS peak_power_kw
        FROM telemetry
        GROUP BY machine_id, machine_type
        ORDER BY SUM(energy_kwh) DESC
    """)

    machine_energy_rows = db.execute(
        machine_energy_query
    ).mappings().all()

    factory_energy = sum(
        float(row["total_energy_kwh"])
        for row in machine_energy_rows
    )

    machine_energy = []

    for row in machine_energy_rows:
        energy = float(row["total_energy_kwh"])

        share = (
            energy / factory_energy * 100
            if factory_energy > 0
            else 0
        )

        machine_energy.append({
            "machine_id": row["machine_id"],
            "machine_type": row["machine_type"],
            "total_energy_kwh": round(energy, 4),
            "average_power_kw": float(row["average_power_kw"]),
            "peak_power_kw": float(row["peak_power_kw"]),
            "energy_share_percent": round(share, 2),
        })

    # ---------------------------------------------------------
    # OPTIMIZATION RECOMMENDATIONS
    # ---------------------------------------------------------

    recommendations = []

    for machine in machine_energy:
        share = machine["energy_share_percent"]

        if share >= 30:
            priority = "high"
        elif share >= 20:
            priority = "medium"
        else:
            priority = "low"

        recommendations.append({
            "machine_id": machine["machine_id"],
            "priority": priority,
            "energy_share_percent": share,
            "energy_kwh": machine["total_energy_kwh"],
        })

    # ---------------------------------------------------------
    # ML ANOMALIES
    # ---------------------------------------------------------

    anomalies = []

    try:
        ml_results = get_anomaly_results(limit=500)

        if not ml_results.empty:
            latest_by_machine = (
                ml_results
                .sort_values("timestamp", ascending=False)
                .drop_duplicates(
                    subset=["machine_id"],
                    keep="first",
                )
            )

            detected = latest_by_machine[
                latest_by_machine["anomaly_prediction"] == -1
            ]

            for _, row in detected.head(10).iterrows():
                anomalies.append({
                    "machine_id": row["machine_id"],
                    "machine_type": row["machine_type"],
                    "power_kw": round(float(row["power_kw"]), 2),
                    "temperature": round(
                        float(row["temperature"]),
                        2,
                    ),
                    "vibration": round(
                        float(row["vibration"]),
                        2,
                    ),
                    "anomaly_score": round(
                        float(row["anomaly_score"]),
                        4,
                    ),
                })

    except Exception:
        anomalies = []

    # ---------------------------------------------------------
    # CARBON
    # ---------------------------------------------------------

    emission_factor = 0.70

    estimated_co2e = (
        factory_energy * emission_factor
    )

    co2e_per_good_unit = (
        estimated_co2e / good_units
        if good_units > 0
        else 0
    )

    # ---------------------------------------------------------
    # FINAL CONTEXT
    # ---------------------------------------------------------

    return {
        "factory": {
            "batches_analyzed": batches,
            "total_energy_kwh": round(
                factory_energy,
                4,
            ),
            "peak_power_kw": round(
                peak_power,
                2,
            ),
            "production_units": production_units,
            "good_units": good_units,
            "rejected_units": rejected_units,
            "quality_rate_percent": round(
                quality_rate,
                2,
            ),
            "specific_energy_kwh_per_good_unit": round(
                sec,
                4,
            ),
        },
        "machines": machines,
        "machine_energy": machine_energy,
        "optimization_recommendations": recommendations,
        "ml_anomalies": anomalies,
        "carbon": {
            "emission_factor_kg_co2e_per_kwh": emission_factor,
            "estimated_co2e_kg": round(
                estimated_co2e,
                4,
            ),
            "estimated_co2e_per_good_unit_kg": round(
                co2e_per_good_unit,
                4,
            ),
        },
    }

def generate_ai_response(
    db: Session,
    user_message: str,
) -> str:

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    context = get_factory_context(db)

    prompt = f"""
You are the UrjaIQ Copilot.

Answer the user's question directly using the factory data below.

FACTORY DATA:
{json.dumps(context, indent=2)}

USER QUESTION:
{user_message}

Rules:
- Directly answer the user's question.
- Do not greet the user.
- Do not repeat the question.
- Do not discuss these rules.
- Do not mention prompts, instructions, tokens, or AI policies.
- Use actual numbers from FACTORY DATA when relevant.
- Never invent numbers.
- If data is unavailable, clearly say that it is unavailable.
- Keep the answer between 3 and 6 short sentences or bullet points.
- For machine questions, name the machine and explain why.
- For anomaly questions, say whether an anomaly is currently detected.
- An ML anomaly means unusual behavior, not confirmed equipment failure.
- Carbon values are estimates using a prototype/configurable emission factor.
- Optimization opportunities are recommendations, not guaranteed savings.
- Give the answer as if you are speaking directly to a factory manager.

Now answer the USER QUESTION.
"""

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{GEMINI_MODEL}:generateContent"
    )

    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ],
       "generationConfig": {
            "thinkingConfig": {
                "thinkingLevel": "low"
            },
            "maxOutputTokens": 1200,
        },
    }

    max_attempts = 3

    for attempt in range(max_attempts):
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=90,
        )

        if response.status_code not in {429, 500, 502, 503, 504}:
            break

        if attempt < max_attempts - 1:
            time.sleep(2 ** attempt)

    response.raise_for_status()

    data = response.json()

    try:
        answer = data["candidates"][0]["content"]["parts"][0]["text"]

        answer = answer.strip()

        if not answer:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return answer

    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            "Gemini returned an unexpected response."
        )