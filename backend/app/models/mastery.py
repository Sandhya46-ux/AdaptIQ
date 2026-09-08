from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Mastery(Base):
    __tablename__ = "mastery"

    id = Column(
        String,
        primary_key=True
    )

    student_id = Column(
        String,
        nullable=False,
        index=True
    )

    concept_id = Column(
        String,
        nullable=False,
        index=True
    )

    mastery = Column(
        Float,
        default=0.0,
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )