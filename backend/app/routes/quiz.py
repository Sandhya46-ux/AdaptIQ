from fastapi import APIRouter

from app.models.schemas import QuizSubmission
from app.services.quiz_engine import (
    get_questions_for_concept,
    evaluate_answers,
    choose_next_difficulty,
)
from app.services.mastery import update_mastery
from app.storage.learner_store import (
    get_mastery,
    update_mastery as store_mastery,
    add_attempt,
    add_misconception,
)

router = APIRouter()


@router.get("/questions")
def get_questions(concept_id: str, difficulty: str = None):
    """
    Get quiz questions for a concept.
    Optional difficulty: Easy, Medium, or Hard.
    """
    return get_questions_for_concept(concept_id, difficulty)


@router.post("/submit")
def submit_quiz(submission: QuizSubmission):
    """
    Evaluate quiz answers and update student mastery.
    """

    # Get all questions for the selected concept
    questions = get_questions_for_concept(submission.concept_id)

    # Evaluate answers
    result = evaluate_answers(
        questions,
        submission.answers
    )

    # Get student's previous mastery
    mastery_data = get_mastery(submission.student_id)

    previous_mastery = mastery_data.get(
        submission.concept_id,
        0
    )

    # Calculate new mastery
    new_mastery = update_mastery(
        previous_mastery,
        result["percentage"]
    )

    # Save mastery
    store_mastery(
        submission.student_id,
        submission.concept_id,
        new_mastery
    )

    # Record misconceptions
    for detail in result["details"]:
        if not detail["correct"]:
            add_misconception(
                submission.student_id,
                detail.get("misconception_id")
            )

    # Decide next difficulty
    next_difficulty = choose_next_difficulty(
        result["percentage"]
    )

    # Save quiz attempt
    add_attempt(
        submission.student_id,
        {
            "type": "quiz",
            "concept_id": submission.concept_id,
            "score": result["correct"],
            "total": result["total"],
        }
    )

    return {
        "student_id": submission.student_id,
        "concept_id": submission.concept_id,
        "correct": result["correct"],
        "total": result["total"],
        "percentage": result["percentage"],
        "previous_mastery": previous_mastery,
        "new_mastery": new_mastery,
        "next_difficulty": next_difficulty,
        "details": result["details"],
    }