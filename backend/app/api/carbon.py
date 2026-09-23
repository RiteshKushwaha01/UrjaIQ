from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import get_db


router = APIRouter(
    prefix="/api/carbon",
    tags=["Carbon"],
)


# Prototype assumption.
# kg CO2e emitted per kWh of electricity consumed.
ELECTRICITY_EMISSION_FACTOR = 0.70


@router.get("/overview")
def get_carbon_overview(
    db: Session = Depends(get_db),
):
    query = text(
        """
        WITH valid_batches AS (
            SELECT
                batch_id,
                MIN(timestamp) AS start_time,
                MAX(timestamp) AS end_time,

                MIN(production_units) AS production_units,
                MAX(production_units) AS max_production_units,

                MIN(good_units) AS good_units,
                MAX(good_units) AS max_good_units,

                MIN(rejected_units) AS rejected_units,
                MAX(rejected_units) AS max_rejected_units,

                SUM(energy_kwh) AS total_energy_kwh

            FROM telemetry

            WHERE machine_id = 'Furnace-01'

            GROUP BY batch_id

            HAVING
                MAX(timestamp) - MIN(timestamp)
                    >= INTERVAL '240 seconds'

                AND MIN(production_units)
                    = MAX(production_units)

                AND MIN(good_units)
                    = MAX(good_units)

                AND MIN(rejected_units)
                    = MAX(rejected_units)

                AND MIN(production_units)
                    = MIN(good_units) + MIN(rejected_units)

                AND MIN(good_units) > 0
        )

        SELECT
            COUNT(*) AS batches_analyzed,
            COALESCE(SUM(total_energy_kwh), 0)
                AS total_energy_kwh,
            COALESCE(SUM(good_units), 0)
                AS total_good_units

        FROM valid_batches
        """
    )

    result = db.execute(query).mappings().one()

    batches_analyzed = int(
        result["batches_analyzed"] or 0
    )

    total_energy = float(
        result["total_energy_kwh"] or 0
    )

    total_good_units = int(
        result["total_good_units"] or 0
    )

    estimated_co2e = (
        total_energy * ELECTRICITY_EMISSION_FACTOR
    )

    co2e_per_good_unit = (
        estimated_co2e / total_good_units
        if total_good_units > 0
        else 0
    )

    return {
        "batches_analyzed": batches_analyzed,

        "total_energy_kwh": round(
            total_energy,
            4,
        ),

        "emission_factor_kg_co2e_per_kwh": (
            ELECTRICITY_EMISSION_FACTOR
        ),

        "estimated_co2e_kg": round(
            estimated_co2e,
            4,
        ),

        "good_units": total_good_units,

        "estimated_co2e_per_good_unit_kg": round(
            co2e_per_good_unit,
            4,
        ),
    }