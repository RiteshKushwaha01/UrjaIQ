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
    query = text("""
        WITH valid_batches AS (
            SELECT
                batch_id,

                MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN production_units
                    END
                ) AS production_units,

                MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN good_units
                    END
                ) AS good_units,

                MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN rejected_units
                    END
                ) AS rejected_units

            FROM telemetry

            GROUP BY batch_id

            HAVING
                COUNT(DISTINCT machine_id) = 4

                AND EXTRACT(
                    EPOCH FROM (
                        MAX(timestamp) - MIN(timestamp)
                    )
                ) >= 240

                AND MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN production_units
                    END
                )
                =
                MAX(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN production_units
                    END
                )

                AND MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN good_units
                    END
                )
                =
                MAX(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN good_units
                    END
                )

                AND MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN rejected_units
                    END
                )
                =
                MAX(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN rejected_units
                    END
                )

                AND MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN production_units
                    END
                )
                =
                MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN good_units
                    END
                )
                +
                MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN rejected_units
                    END
                )

                AND MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN good_units
                    END
                ) > 0
        ),

        batch_energy AS (
            SELECT
                t.batch_id,

                SUM(t.energy_kwh)
                    AS factory_energy_kwh

            FROM telemetry t

            INNER JOIN valid_batches vb
                ON t.batch_id = vb.batch_id

            GROUP BY t.batch_id
        )

        SELECT
            COUNT(*) AS batches_analyzed,

            COALESCE(
                SUM(be.factory_energy_kwh),
                0
            ) AS total_energy_kwh,

            COALESCE(
                SUM(vb.good_units),
                0
            ) AS total_good_units

        FROM valid_batches vb

        INNER JOIN batch_energy be
            ON vb.batch_id = be.batch_id;
    """)

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
        total_energy
        * ELECTRICITY_EMISSION_FACTOR
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