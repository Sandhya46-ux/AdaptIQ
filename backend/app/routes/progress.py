from fastapi import APIRouter

from app.storage.learner_store import (
    get_mastery,
    get_attempts,
    get_misconceptions,
)

router = APIRouter()


@router.get("/{student_id}")
def get_progress(student_id: str):
    """
    Return the student's overall learning progress.
    """

    mastery = get_mastery(student_id)
    attempts = get_attempts(student_id)
    misconceptions = get_misconceptions(student_id)

    # Calculate overall mastery
    if mastery:
        overall_mastery = sum(mastery.values()) / len(mastery)
    else:
        overall_mastery = 0

    return {
        "student_id": student_id,
        "overall_mastery": round(overall_mastery, 2),
        "concepts": mastery,
        "total_attempts": len(attempts),
        "misconceptions": misconceptions,
    }