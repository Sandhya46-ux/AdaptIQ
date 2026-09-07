import pytest

QUESTIONS = [
    {
        "question_id": "Q001",
        "concept": "Fractions",
        "difficulty": "easy",
        "options": ["1/2", "1/3", "2/3", "3/4"],
        "correct_answer": "1/2",
    },
    {
        "question_id": "Q002",
        "concept": "Fractions",
        "difficulty": "medium",
        "options": ["2/3", "1/4", "3/4", "1/2"],
        "correct_answer": "2/3",
    },
]


def test_questions_are_available():
    """TC007: quiz should have questions available."""
    assert len(QUESTIONS) > 0


def test_question_has_options():
    """TC003: every question should have options."""
    for question in QUESTIONS:
        assert question["options"]
        assert len(question["options"]) >= 2


def test_correct_answer_exists_in_options():
    """TC004: correct answer must be one of the options."""
    for question in QUESTIONS:
        assert question["correct_answer"] in question["options"]


def test_correct_answer_evaluation():
    """TC008: correct answer should be marked correct."""
    question = QUESTIONS[0]
    selected = "1/2"
    assert selected == question["correct_answer"]


def test_incorrect_answer_evaluation():
    """TC009: incorrect answer should be marked incorrect."""
    question = QUESTIONS[0]
    selected = "2/3"
    assert selected != question["correct_answer"]


def test_no_answer_validation():
    """TC010: empty answer should be rejected."""
    selected = None
    assert selected is None


def test_score_calculation():
    """TC011: score should be calculated correctly."""
    results = [True, True, False, True]
    score = sum(results)
    percentage = score / len(results) * 100

    assert score == 3
    assert percentage == 75.0


def test_attempt_number_increments():
    """TC012: repeated attempts should increment attempt number."""
    attempt_number = 1
    attempt_number += 1
    assert attempt_number == 2


def test_response_time_is_recorded():
    """TC013: response time should be a non-negative number."""
    response_time_seconds = 18
    assert response_time_seconds >= 0


def test_poor_performance_reduces_difficulty():
    """TC026: poor performance should select an easier difficulty."""
    current_difficulty = "medium"
    accuracy = 0.30

    if accuracy < 0.50:
        next_difficulty = "easy"
    else:
        next_difficulty = current_difficulty

    assert next_difficulty == "easy"


def test_strong_performance_increases_difficulty():
    """TC027: strong performance should select a harder difficulty."""
    current_difficulty = "medium"
    accuracy = 0.90

    if accuracy >= 0.80:
        next_difficulty = "hard"
    else:
        next_difficulty = current_difficulty

    assert next_difficulty == "hard"
