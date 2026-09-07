from fastapi import APIRouter

from app.models.schemas import TutorRequest
from app.storage.learner_store import get_mastery
from app.services.data_loader import load_concepts

router = APIRouter()


def get_concept_name(concept_id: str):
    """
    Find the concept name using concept_id.
    """

    concepts = load_concepts()

    for concept in concepts:
        if concept["concept_id"] == concept_id:
            return concept["concept"]

    return concept_id


@router.post("/ask")
def ask_tutor(request: TutorRequest):
    """
    Basic adaptive tutor prototype.

    The response changes according to
    the student's mastery level.
    """

    mastery = get_mastery(
        request.student_id
    ).get(
        request.concept_id,
        0
    )

    concept_name = get_concept_name(
        request.concept_id
    )

    # Hindi response
    if request.language.lower() == "hindi":

        response = (
            f"Aapki {concept_name} mein current mastery "
            f"{mastery}% hai. "
            "Chaliye ise step-by-step samajhte hain. "
            "Pehle bataiye ki question mein kya find karna hai."
        )

    # Beginner level
    elif mastery < 40:

        response = (
            f"Your mastery in {concept_name} is {mastery}%. "
            "Let's start with the basics. "
            "What information is given in the question?"
        )

    # Intermediate level
    elif mastery < 70:

        response = (
            f"Your mastery in {concept_name} is {mastery}%. "
            "You're making progress. "
            "Let's solve the problem step by step. "
            "What should we do first?"
        )

    # Strong learner
    else:

        response = (
            f"Your mastery in {concept_name} is {mastery}%. "
            "You have a good understanding. "
            "Try solving the problem first, "
            "and I'll guide you if needed."
        )

    return {
        "student_id": request.student_id,
        "concept_id": request.concept_id,
        "concept": concept_name,
        "mastery": mastery,
        "response": response,
    }