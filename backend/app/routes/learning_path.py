from fastapi import APIRouter

from app.storage.learner_store import get_mastery
from app.services.recommendation import generate_recommendations

router = APIRouter()


@router.get("/{student_id}")
def get_learning_path(student_id: str):
    """
    Generate a personalized learning path
    based on the student's current mastery.
    """

    mastery = get_mastery(student_id)

    recommendations = generate_recommendations(
        mastery
    )

    return {
        "student_id": student_id,
        "learning_path": recommendations,
    }