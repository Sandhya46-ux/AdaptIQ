from fastapi import APIRouter

from app.models.schemas import (
    DiagnosticSubmission
)

from app.services.data_loader import (
    load_questions
)

from app.services.mastery import (
    calculate_mastery
)

from app.storage.learner_store import (
    update_mastery,
    add_attempt,
    add_misconception
)


router = APIRouter()


@router.post("/submit")
def submit_diagnostic(
    submission: DiagnosticSubmission
):

    questions = load_questions()

    question_map = {
        q["question_id"]: q
        for q in questions
    }

    concept_results = {}

    total_correct = 0

    for answer in submission.answers:

        question = question_map.get(
            answer.question_id
        )

        if not question:
            continue

        concept_id = question[
            "concept_id"
        ]

        if concept_id not in concept_results:

            concept_results[
                concept_id
            ] = {
                "correct": 0,
                "total": 0
            }

        concept_results[
            concept_id
        ]["total"] += 1

        is_correct = (
            answer.answer
            == question["correct_answer"]
        )

        if is_correct:

            concept_results[
                concept_id
            ]["correct"] += 1

            total_correct += 1

        else:

            misconception_id = (
                question.get(
                    "misconception_id"
                )
            )

            if misconception_id:

                add_misconception(
                    submission.student_id,
                    misconception_id
                )

    mastery = {}

    for concept_id, result in (
        concept_results.items()
    ):

        concept_mastery = (
            calculate_mastery(
                result["correct"],
                result["total"]
            )
        )

        mastery[
            concept_id
        ] = concept_mastery

        update_mastery(
            submission.student_id,
            concept_id,
            concept_mastery
        )

    total = len(
        submission.answers
    )

    percentage = (
        total_correct / total * 100
        if total
        else 0
    )

    add_attempt(
        submission.student_id,
        {
            "type": "diagnostic",
            "score": total_correct,
            "total": total
        }
    )

    return {

        "student_id":
            submission.student_id,

        "score":
            total_correct,

        "total":
            total,

        "percentage":
            round(
                percentage,
                2
            ),

        "mastery":
            mastery
    }