from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Misconception(Base):
    __tablename__ = "misconceptions"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id = Column(
        String,
        nullable=False,
        index=True
    )

    concept_id = Column(
        String,
        nullable=True,
        index=True
    )

    misconception_id = Column(
        String,
        nullable=True,
        index=True
    )

    count = Column(
        Integer,
        default=1,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )