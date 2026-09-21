from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.telemetry import Telemetry

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/overview")
def get_factory_overview(db: Session = Depends(get_db)):
    total_energy = (
        db.query(func.sum(Telemetry.energy_kwh))
        .scalar()
        or 0
    )

    peak_power = (
        db.query(func.max(Telemetry.power_kw))
        .scalar()
        or 0
    )

    latest_furnace = (
        db.query(Telemetry)
        .filter(Telemetry.machine_id == "Furnace-01")
        .order_by(Telemetry.timestamp.desc())
        .first()
    )

    if latest_furnace:
        production_units = latest_furnace.production_units
        good_units = latest_furnace.good_units
        rejected_units = latest_furnace.rejected_units
    else:
        production_units = 0
        good_units = 0
        rejected_units = 0

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

    return {
        "total_energy_kwh": round(total_energy, 2),
        "peak_power_kw": round(peak_power, 2),
        "production_units": production_units,
        "good_units": good_units,
        "rejected_units": rejected_units,
        "quality_rate": round(quality_rate, 2),
        "specific_energy_kwh_per_good_unit": round(
            specific_energy,
            4,
        ),
    }