from sqlalchemy import Column, Float, Integer, String

from app.database.database import Base


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)

    machine_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    machine_type = Column(
        String,
        nullable=False,
    )

    rated_power_kw = Column(
        Float,
        nullable=False,
    )

    status = Column(
        String,
        default="normal",
        nullable=False,
    )