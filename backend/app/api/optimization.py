from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import get_db

router = APIRouter(
    prefix="/api/optimization",
    tags=["Optimization"],
)


@router.get("/baseline")
def get_energy_baseline(
    db: Session = Depends(get_db),
):
    query = text("""
        WITH batch_metrics AS (
            SELECT
                batch_id,

                EXTRACT(
                    EPOCH FROM (
                        MAX(timestamp) - MIN(timestamp)
                    )
                ) AS duration_seconds,

                SUM(energy_kwh) AS factory_energy_kwh,

                MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN production_units
                    END
                ) AS production_units_min,

                MAX(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN production_units
                    END
                ) AS production_units_max,

                MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN good_units
                    END
                ) AS good_units_min,

                MAX(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN good_units
                    END
                ) AS good_units_max,

                MIN(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN rejected_units
                    END
                ) AS rejected_units_min,

                MAX(
                    CASE
                        WHEN machine_id = 'Furnace-01'
                        THEN rejected_units
                    END
                ) AS rejected_units_max

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
        ),

        valid_batches AS (
            SELECT
                batch_id,
                factory_energy_kwh,
                production_units_min AS production_units,
                good_units_min AS good_units,
                rejected_units_min AS rejected_units

            FROM batch_metrics

            WHERE
                production_units_min =
                    good_units_min + rejected_units_min

                AND good_units_min > 0
        ),

        calculated_metrics AS (
            SELECT
                *,
                factory_energy_kwh
                    / NULLIF(good_units, 0)
                    AS sec_kwh_per_good_unit,

                good_units
                    / NULLIF(production_units, 0)
                    * 100
                    AS quality_rate

            FROM valid_batches
        )

        SELECT
            COUNT(*) AS batches_analyzed,

            AVG(factory_energy_kwh)
                AS average_energy_kwh,

            AVG(production_units)
                AS average_production_units,

            AVG(good_units)
                AS average_good_units,

            AVG(rejected_units)
                AS average_rejected_units,

            AVG(quality_rate)
                AS average_quality_rate,

            AVG(sec_kwh_per_good_unit)
                AS average_sec

        FROM calculated_metrics;
    """)

    result = db.execute(query).mappings().one()

    return {
        "batches_analyzed": result["batches_analyzed"],
        "average_energy_kwh": round(
            float(result["average_energy_kwh"] or 0),
            4,
        ),
        "average_production_units": round(
            float(result["average_production_units"] or 0),
            2,
        ),
        "average_good_units": round(
            float(result["average_good_units"] or 0),
            2,
        ),
        "average_rejected_units": round(
            float(result["average_rejected_units"] or 0),
            2,
        ),
        "average_quality_rate": round(
            float(result["average_quality_rate"] or 0),
            2,
        ),
        "average_sec_kwh_per_good_unit": round(
            float(result["average_sec"] or 0),
            4,
        ),
    }

@router.get("/machine-energy")
def get_machine_energy(
    db: Session = Depends(get_db),
):
    query = text("""
        WITH valid_batches AS (
            SELECT
                batch_id

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
        )

        SELECT
            t.machine_id,
            t.machine_type,

            ROUND(
                SUM(t.energy_kwh)::numeric,
                4
            ) AS total_energy_kwh,

            ROUND(
                AVG(t.power_kw)::numeric,
                2
            ) AS average_power_kw,

            ROUND(
                MAX(t.power_kw)::numeric,
                2
            ) AS peak_power_kw

        FROM telemetry t

        INNER JOIN valid_batches vb
            ON t.batch_id = vb.batch_id

        GROUP BY
            t.machine_id,
            t.machine_type

        ORDER BY
            SUM(t.energy_kwh) DESC;
    """)

    results = db.execute(query).mappings().all()

    total_energy = sum(
        float(row["total_energy_kwh"] or 0)
        for row in results
    )

    machines = []

    for row in results:
        energy = float(row["total_energy_kwh"] or 0)

        energy_share = (
            (energy / total_energy) * 100
            if total_energy > 0
            else 0
        )

        machines.append({
            "machine_id": row["machine_id"],
            "machine_type": row["machine_type"],
            "total_energy_kwh": round(energy, 4),
            "average_power_kw": round(
                float(row["average_power_kw"] or 0),
                2,
            ),
            "peak_power_kw": round(
                float(row["peak_power_kw"] or 0),
                2,
            ),
            "energy_share_percent": round(
                energy_share,
                2,
            ),
        })

    return {
        "total_factory_energy_kwh": round(
            total_energy,
            4,
        ),
        "machines": machines,
    }


@router.get("/recommendations")
def get_optimization_recommendations(
    db: Session = Depends(get_db),
):
    query = text("""
        WITH valid_batches AS (
            SELECT
                batch_id

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
        ),

        machine_energy AS (
            SELECT
                t.machine_id,
                t.machine_type,
                SUM(t.energy_kwh) AS total_energy_kwh,
                AVG(t.power_kw) AS average_power_kw

            FROM telemetry t

            INNER JOIN valid_batches vb
                ON t.batch_id = vb.batch_id

            GROUP BY
                t.machine_id,
                t.machine_type
        ),

        factory_energy AS (
            SELECT
                SUM(total_energy_kwh) AS total_energy_kwh
            FROM machine_energy
        )

        SELECT
            me.machine_id,
            me.machine_type,
            me.total_energy_kwh,
            me.average_power_kw,
            (
                me.total_energy_kwh
                / NULLIF(fe.total_energy_kwh, 0)
            ) * 100 AS energy_share_percent

        FROM machine_energy me
        CROSS JOIN factory_energy fe

        ORDER BY
            me.total_energy_kwh DESC;
    """)

    results = db.execute(query).mappings().all()

    recommendations = []

    for row in results:
        machine_id = row["machine_id"]
        machine_type = row["machine_type"]
        energy_share = float(
            row["energy_share_percent"] or 0
        )
        energy = float(
            row["total_energy_kwh"] or 0
        )

        if energy_share >= 30:
            recommendations.append({
                "machine_id": machine_id,
                "machine_type": machine_type,
                "priority": "high",
                "type": "energy_efficiency",
                "title": (
                    f"Review {machine_id} energy profile"
                ),
                "description": (
                    f"{machine_id} accounts for "
                    f"{energy_share:.1f}% of factory energy "
                    f"in the valid baseline window. "
                    "Review operating and idle periods "
                    "for energy-saving opportunities "
                    "without reducing production output "
                    "or quality."
                ),
                "energy_kwh": round(energy, 4),
                "energy_share_percent": round(
                    energy_share,
                    2,
                ),
            })

        elif energy_share >= 20:
            recommendations.append({
                "machine_id": machine_id,
                "machine_type": machine_type,
                "priority": "medium",
                "type": "energy_efficiency",
                "title": (
                    f"Monitor {machine_id} energy usage"
                ),
                "description": (
                    f"{machine_id} accounts for "
                    f"{energy_share:.1f}% of factory energy. "
                    "Review its operating profile and "
                    "identify avoidable energy consumption."
                ),
                "energy_kwh": round(energy, 4),
                "energy_share_percent": round(
                    energy_share,
                    2,
                ),
            })

    return {
        "recommendations": recommendations,
        "count": len(recommendations),
    }

@router.get("/savings")
def get_savings_estimate(
    db: Session = Depends(get_db),
):
    query = text("""
        WITH valid_batches AS (
            SELECT
                batch_id

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
        ),

        batch_metrics AS (
            SELECT
                t.batch_id,

                SUM(t.energy_kwh)
                    AS factory_energy_kwh,

                MAX(
                    CASE
                        WHEN t.machine_id = 'Furnace-01'
                        THEN t.good_units
                    END
                ) AS good_units

            FROM telemetry t

            INNER JOIN valid_batches vb
                ON t.batch_id = vb.batch_id

            GROUP BY t.batch_id
        )

        SELECT
            AVG(factory_energy_kwh)
                AS average_energy_kwh,

            AVG(good_units)
                AS average_good_units

        FROM batch_metrics;
    """)

    result = db.execute(query).mappings().one()

    average_energy = float(
        result["average_energy_kwh"] or 0
    )

    average_good_units = float(
        result["average_good_units"] or 0
    )

    # Simulation assumptions
    assumed_reduction_percent = 8.0
    electricity_tariff = 8.0

    estimated_energy_saving = (
        average_energy
        * assumed_reduction_percent
        / 100
    )

    estimated_cost_saving = (
        estimated_energy_saving
        * electricity_tariff
    )

    baseline_sec = (
        average_energy / average_good_units
        if average_good_units > 0
        else 0
    )

    optimized_energy = (
        average_energy
        - estimated_energy_saving
    )

    optimized_sec = (
        optimized_energy / average_good_units
        if average_good_units > 0
        else 0
    )

    sec_improvement = (
        (
            baseline_sec - optimized_sec
        )
        / baseline_sec
        * 100
        if baseline_sec > 0
        else 0
    )

    return {
        "assumptions": {
            "estimated_reduction_percent": (
                assumed_reduction_percent
            ),
            "electricity_tariff_inr_per_kwh": (
                electricity_tariff
            ),
        },
        "baseline": {
            "average_energy_kwh": round(
                average_energy,
                4,
            ),
            "average_good_units": round(
                average_good_units,
                2,
            ),
            "sec_kwh_per_good_unit": round(
                baseline_sec,
                4,
            ),
        },
        "optimized_scenario": {
            "estimated_energy_kwh": round(
                optimized_energy,
                4,
            ),
            "estimated_sec_kwh_per_good_unit": round(
                optimized_sec,
                4,
            ),
            "estimated_sec_improvement_percent": round(
                sec_improvement,
                2,
            ),
        },
        "savings": {
            "estimated_energy_saving_kwh": round(
                estimated_energy_saving,
                4,
            ),
            "estimated_cost_saving_inr": round(
                estimated_cost_saving,
                2,
            ),
        },
    }