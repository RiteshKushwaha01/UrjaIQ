from sqlalchemy.orm import Session

from app.models.telemetry import Telemetry
from app.schemas.telemetry import TelemetryCreate


def save_telemetry(
    db: Session,
    telemetry_data: TelemetryCreate,
) -> Telemetry:

    telemetry = Telemetry(
        timestamp=telemetry_data.timestamp,
        batch_id=telemetry_data.batch_id,
        machine_id=telemetry_data.machine_id,
        machine_type=telemetry_data.machine_type,
        power_kw=telemetry_data.power_kw,
        energy_kwh=telemetry_data.energy_kwh,
        temperature=telemetry_data.temperature,
        vibration=telemetry_data.vibration,
        voltage=telemetry_data.voltage,
        current=telemetry_data.current,
        operating_state=telemetry_data.operating_state,
        production_units=telemetry_data.production_units,
        good_units=telemetry_data.good_units,
        rejected_units=telemetry_data.rejected_units,
    )

    try:
        db.add(telemetry)
        db.commit()
        db.refresh(telemetry)

        return telemetry

    except Exception:
        db.rollback()
        raise