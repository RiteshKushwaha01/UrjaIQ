from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import get_db


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


@router.get("/overview")
def get_factory_overview(
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
        ),

        aggregated AS (
            SELECT
                COUNT(*) AS batches_analyzed,

                COALESCE(
                    SUM(be.factory_energy_kwh),
                    0
                ) AS total_energy_kwh,

                COALESCE(
                    SUM(vb.production_units),
                    0
                ) AS production_units,

                COALESCE(
                    SUM(vb.good_units),
                    0
                ) AS good_units,

                COALESCE(
                    SUM(vb.rejected_units),
                    0
                ) AS rejected_units

            FROM valid_batches vb

            INNER JOIN batch_energy be
                ON vb.batch_id = be.batch_id
        )

        SELECT
            batches_analyzed,
            total_energy_kwh,
            production_units,
            good_units,
            rejected_units

        FROM aggregated;
    """)

    result = db.execute(query).mappings().one()

    batches_analyzed = int(
        result["batches_analyzed"] or 0
    )

    total_energy = float(
        result["total_energy_kwh"] or 0
    )

    production_units = int(
        result["production_units"] or 0
    )

    good_units = int(
        result["good_units"] or 0
    )

    rejected_units = int(
        result["rejected_units"] or 0
    )

    quality_rate = (
        (good_units / production_units) * 100
        if production_units > 0
        else 0
    )

    specific_energy = (
        total_energy / good_units
        if good_units > 0
        else 0
    )

    peak_power_query = text("""
        SELECT
            COALESCE(
                MAX(power_kw),
                0
            ) AS peak_power_kw

        FROM telemetry;
    """)

    peak_power = float(
        db.execute(peak_power_query)
        .scalar()
        or 0
    )

    return {
        "batches_analyzed": batches_analyzed,

        "total_energy_kwh": round(
            total_energy,
            4,
        ),

        "peak_power_kw": round(
            peak_power,
            2,
        ),

        "production_units": production_units,

        "good_units": good_units,

        "rejected_units": rejected_units,

        "quality_rate": round(
            quality_rate,
            2,
        ),

        "specific_energy_kwh_per_good_unit": round(
            specific_energy,
            4,
        ),
    }