from sqlalchemy import Column, DateTime, Float, Integer, String, Index
from app.database.database import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)

    batch_id = Column(String, nullable=False, index=True)

    machine_id = Column(String, nullable=False, index=True)
    machine_type = Column(String, nullable=False)

    power_kw = Column(Float, nullable=False)
    energy_kwh = Column(Float, nullable=False)

    temperature = Column(Float, nullable=False)
    vibration = Column(Float, nullable=False)

    voltage = Column(Float, nullable=False)
    current = Column(Float, nullable=False)

    operating_state = Column(String, nullable=False)

    production_units = Column(Integer, nullable=False)
    good_units = Column(Integer, nullable=False)
    rejected_units = Column(Integer, nullable=False)

    __table_args__ = (
        Index(
            "ix_telemetry_machine_timestamp",
            "machine_id",
            "timestamp",
        ),
    )