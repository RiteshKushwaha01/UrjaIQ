from datetime import datetime

from pydantic import BaseModel, Field


class TelemetryCreate(BaseModel):
    timestamp: datetime
    batch_id: str = Field(min_length=1)

    machine_id: str = Field(min_length=1)
    machine_type: str = Field(min_length=1)

    power_kw: float = Field(ge=0)
    energy_kwh: float = Field(ge=0)

    temperature: float
    vibration: float = Field(ge=0)

    voltage: float = Field(gt=0)
    current: float = Field(ge=0)

    operating_state: str = Field(min_length=1)

    production_units: int = Field(ge=0)
    good_units: int = Field(ge=0)
    rejected_units: int = Field(ge=0)