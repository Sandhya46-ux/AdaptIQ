from app.services.data_loader import (
    load_questions
)


def get_questions_for_concept(
    concept_id,
    difficulty=None
):

    questions = load_questions()

    result = []

    for question in questions:

        if question.get(
            "concept_id"
        ) != concept_id:

            continue

        if difficulty:

            if (
                question["difficulty"].lower()
                != difficulty.lower()
            ):

                continue

        result.append(question)

    return result


def evaluate_answers(
    questions,
    submitted_answers
):

    answer_map = {
        item.question_id:
            item.answer

        for item in submitted_answers
    }

    correct = 0

    details = []

    for question in questions:

        question_id = question[
            "question_id"
        ]

        selected = answer_map.get(
            question_id
        )

        is_correct = (
            selected
            == question["correct_answer"]
        )

        if is_correct:

            correct += 1

        details.append({

            "question_id":
                question_id,

            "correct":
                is_correct,

            "selected_answer":
                selected,

            "correct_answer":
                question["correct_answer"],

            "misconception":
                question.get(
                    "misconception"
                ),

            "intervention":
                question.get(
                    "intervention"
                )
        })

    total = len(questions)

    percentage = (
        (correct / total) * 100
        if total
        else 0
    )

    return {

        "correct": correct,

        "total": total,

        "percentage":
            round(
                percentage,
                2
            ),

        "details": details
    }


def choose_next_difficulty(
    percentage
):

    if percentage >= 80:

        return "Hard"

    if percentage >= 50:

        return "Medium"

    return "Easy"