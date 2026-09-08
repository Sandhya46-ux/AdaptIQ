from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Attempt(Base):
    __tablename__ = "attempts"

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

    question_id = Column(
        String,
        nullable=True,
        index=True
    )

    concept_id = Column(
        String,
        nullable=True,
        index=True
    )

    is_correct = Column(
        Boolean,
        nullable=True
    )

    score = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )