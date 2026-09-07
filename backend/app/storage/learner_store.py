from app.services.data_loader import load_attempts


learners = {}


def create_student(student_id):

    if student_id not in learners:

        learners[student_id] = {
            "mastery": {},
            "attempts": [],
            "misconceptions": {}
        }

    return learners[student_id]


def get_student(student_id):

    return create_student(student_id)


def update_mastery(
    student_id,
    concept_id,
    mastery
):

    student = create_student(student_id)

    student["mastery"][concept_id] = mastery


def get_mastery(student_id):

    student = create_student(student_id)

    return student["mastery"]


def add_attempt(
    student_id,
    attempt
):

    student = create_student(student_id)

    student["attempts"].append(attempt)


def add_misconception(
    student_id,
    misconception_id
):

    student = create_student(student_id)

    if misconception_id:

        student["misconceptions"][
            misconception_id
        ] = (
            student["misconceptions"].get(
                misconception_id,
                0
            ) + 1
        )


def get_attempts(student_id):

    student = create_student(student_id)

    return student["attempts"]


def get_misconceptions(student_id):

    student = create_student(student_id)

    return student["misconceptions"]