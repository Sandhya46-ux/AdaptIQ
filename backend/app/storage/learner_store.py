from sqlalchemy import func

from app.database import SessionLocal
from app.models.student import Student
from app.models.mastery import Mastery
from app.models.attempt import Attempt
from app.models.misconception import Misconception


def create_student(student_id):
    db = SessionLocal()

    try:
        student = (
            db.query(Student)
            .filter(Student.student_id == student_id)
            .first()
        )

        if not student:
            student = Student(student_id=student_id)
            db.add(student)
            db.commit()
            db.refresh(student)

        return {
            "mastery": get_mastery(student_id),
            "attempts": get_attempts(student_id),
            "misconceptions": get_misconceptions(student_id),
        }

    finally:
        db.close()


def get_student(student_id):
    return create_student(student_id)


def update_mastery(
    student_id,
    concept_id,
    mastery
):
    db = SessionLocal()

    try:
        student = (
            db.query(Student)
            .filter(Student.student_id == student_id)
            .first()
        )

        if not student:
            student = Student(student_id=student_id)
            db.add(student)
            db.flush()

        record = (
            db.query(Mastery)
            .filter(
                Mastery.student_id == student_id,
                Mastery.concept_id == concept_id
            )
            .first()
        )

        if record:
            record.mastery = mastery
        else:
            record = Mastery(
                id=f"{student_id}_{concept_id}",
                student_id=student_id,
                concept_id=concept_id,
                mastery=mastery
            )
            db.add(record)

        db.commit()

    finally:
        db.close()


def get_mastery(student_id):
    db = SessionLocal()

    try:
        records = (
            db.query(Mastery)
            .filter(Mastery.student_id == student_id)
            .all()
        )

        return {
            record.concept_id: record.mastery
            for record in records
        }

    finally:
        db.close()


def add_attempt(
    student_id,
    attempt
):
    db = SessionLocal()

    try:
        student = (
            db.query(Student)
            .filter(Student.student_id == student_id)
            .first()
        )

        if not student:
            student = Student(student_id=student_id)
            db.add(student)
            db.flush()

        record = Attempt(
            student_id=student_id,
            question_id=attempt.get("question_id"),
            concept_id=attempt.get("concept_id"),
            is_correct=attempt.get(
                "correct",
                False
            ),
            score=attempt.get("score")
        )

        db.add(record)
        db.commit()

    finally:
        db.close()


def add_misconception(
    student_id,
    misconception_id
):
    if not misconception_id:
        return

    db = SessionLocal()

    try:
        student = (
            db.query(Student)
            .filter(Student.student_id == student_id)
            .first()
        )

        if not student:
            student = Student(student_id=student_id)
            db.add(student)
            db.flush()

        record = (
            db.query(Misconception)
            .filter(
                Misconception.student_id == student_id,
                Misconception.misconception_id
                == misconception_id
            )
            .first()
        )

        if record:
            record.count += 1
        else:
            record = Misconception(
                student_id=student_id,
                misconception_id=misconception_id,
                count=1
            )
            db.add(record)

        db.commit()

    finally:
        db.close()


def get_attempts(student_id):
    db = SessionLocal()

    try:
        records = (
            db.query(Attempt)
            .filter(Attempt.student_id == student_id)
            .order_by(Attempt.created_at)
            .all()
        )

        return [
            {
                "question_id": record.question_id,
                "concept_id": record.concept_id,
                "correct": record.is_correct,
                "score": record.score,
            }
            for record in records
        ]

    finally:
        db.close()


def get_misconceptions(student_id):
    db = SessionLocal()

    try:
        records = (
            db.query(Misconception)
            .filter(
                Misconception.student_id == student_id
            )
            .all()
        )

        return {
            record.misconception_id: record.count
            for record in records
        }

    finally:
        db.close()