from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    student_id = Column(
        String,
        primary_key=True,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )