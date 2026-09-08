from app.storage.learner_store import (
    create_student,
    get_student,
    update_mastery,
)


def test_create_student():
    student_id = "pytest_student"

    student = create_student(student_id)

    assert "mastery" in student
    assert "attempts" in student
    assert "misconceptions" in student


def test_update_mastery():
    student_id = "pytest_student"
    concept_id = "algebra"

    update_mastery(student_id, concept_id, 85.0)

    student = get_student(student_id)

    assert student["mastery"]["algebra"] == 85.0