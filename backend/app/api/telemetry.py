from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.telemetry import Telemetry


router = APIRouter(
    prefix="/api/telemetry",
    tags=["Telemetry"],
)


@router.get("/recent")
def get_recent_telemetry(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    telemetry = (
        db.query(Telemetry)
        .order_by(Telemetry.timestamp.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": item.id,
            "timestamp": item.timestamp,
            "batch_id": item.batch_id,
            "machine_id": item.machine_id,
            "machine_type": item.machine_type,
            "power_kw": item.power_kw,
            "energy_kwh": item.energy_kwh,
            "temperature": item.temperature,
            "vibration": item.vibration,
            "voltage": item.voltage,
            "current": item.current,
            "operating_state": item.operating_state,
            "production_units": item.production_units,
            "good_units": item.good_units,
            "rejected_units": item.rejected_units,
        }
        for item in telemetry
    ]

@router.get("/machine/{machine_id}")
def get_machine_telemetry(
    machine_id: str,
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.machine_id == machine_id)
        .order_by(Telemetry.timestamp.desc())
        .limit(limit)
        .all()
    )

    if not telemetry:
        raise HTTPException(
            status_code=404,
            detail=f"Machine '{machine_id}' not found",
        )

    return [
        {
            "id": item.id,
            "timestamp": item.timestamp,
            "batch_id": item.batch_id,
            "machine_id": item.machine_id,
            "machine_type": item.machine_type,
            "power_kw": item.power_kw,
            "energy_kwh": item.energy_kwh,
            "temperature": item.temperature,
            "vibration": item.vibration,
            "voltage": item.voltage,
            "current": item.current,
            "operating_state": item.operating_state,
            "production_units": item.production_units,
            "good_units": item.good_units,
            "rejected_units": item.rejected_units,
        }
        for item in telemetry
    ]

@router.get("/machine/{machine_id}/latest")
def get_latest_machine_telemetry(
    machine_id: str,
    db: Session = Depends(get_db),
):
    telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.machine_id == machine_id)
        .order_by(Telemetry.timestamp.desc())
        .first()
    )

    if telemetry is None:
        raise HTTPException(
            status_code=404,
            detail=f"Machine '{machine_id}' not found",
        )

    return {
        "found": True,
        "id": telemetry.id,
        "timestamp": telemetry.timestamp,
        "batch_id": telemetry.batch_id,
        "machine_id": telemetry.machine_id,
        "machine_type": telemetry.machine_type,
        "power_kw": telemetry.power_kw,
        "energy_kwh": telemetry.energy_kwh,
        "temperature": telemetry.temperature,
        "vibration": telemetry.vibration,
        "voltage": telemetry.voltage,
        "current": telemetry.current,
        "operating_state": telemetry.operating_state,
        "production_units": telemetry.production_units,
        "good_units": telemetry.good_units,
        "rejected_units": telemetry.rejected_units,
    }

@router.get("/machines")
def get_machines(
    db: Session = Depends(get_db),
):
    machines = (
        db.query(Telemetry.machine_id, Telemetry.machine_type)
        .distinct()
        .order_by(Telemetry.machine_id)
        .all()
    )

    return [
        {
            "machine_id": machine_id,
            "machine_type": machine_type,
        }
        for machine_id, machine_type in machines
    ]