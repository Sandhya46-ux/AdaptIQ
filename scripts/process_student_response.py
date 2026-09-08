import json
from pathlib import Path


# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

QUESTIONS_FILE = (
    BASE_DIR
    / "data"
    / "questions"
    / "physics_questions.json"
)

MISCONCEPTIONS_FILE = (
    BASE_DIR
    / "data"
    / "misconceptions"
    / "physics_misconceptions.json"
)

MAPPING_FILE = (
    BASE_DIR
    / "data"
    / "misconceptions"
    / "physics_question_misconception_map.json"
)

RESPONSES_FILE = (
    BASE_DIR
    / "data"
    / "responses"
    / "student_responses.json"
)


# ==========================================
# LOAD JSON
# ==========================================

def load_json(file_path):

    if not file_path.exists():

        print(
            f"❌ File not found:\n{file_path}"
        )

        return None

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError as error:

        print(
            f"❌ Invalid JSON:\n{file_path}"
        )

        print(error)

        return None


# ==========================================
# SAVE JSON
# ==========================================

def save_json(file_path, data):

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


# ==========================================
# FIND QUESTION
# ==========================================

def find_question(
    questions,
    question_id
):

    for question in questions:

        if question.get("id") == question_id:

            return question

    return None


# ==========================================
# FIND MISCONCEPTION
# ==========================================

def find_misconception(
    misconceptions,
    misconception_id
):

    for misconception in misconceptions:

        if (
            misconception.get(
                "misconception_id"
            )
            == misconception_id
        ):

            return misconception

    return None


# ==========================================
# FIND MISCONCEPTION FROM WRONG ANSWER
# ==========================================

def find_misconception_from_answer(
    mappings,
    question_id,
    selected_answer
):

    for mapping in mappings:

        if (
            mapping.get("question_id")
            != question_id
        ):

            continue

        for item in mapping.get(
            "mappings",
            []
        ):

            if (
                item.get("wrong_answer")
                == selected_answer
            ):

                return item.get(
                    "misconception_id"
                )

    return None


# ==========================================
# PROCESS STUDENT RESPONSE
# ==========================================

def process_response(
    student_id,
    question_id,
    selected_answer,
    questions,
    misconceptions,
    mappings
):

    # --------------------------------------
    # Find question
    # --------------------------------------

    question = find_question(
        questions,
        question_id
    )

    if question is None:

        print(
            f"❌ Question not found: "
            f"{question_id}"
        )

        return None

    # --------------------------------------
    # Validate selected answer
    # --------------------------------------

    options = question.get(
        "options",
        []
    )

    if selected_answer not in options:

        print(
            "\n❌ Invalid answer."
        )

        print(
            "Available options:"
        )

        for option in options:

            print(
                f"  - {option}"
            )

        return None

    correct_answer = question.get(
        "answer"
    )

    is_correct = (
        selected_answer
        == correct_answer
    )

    # --------------------------------------
    # Default result
    # --------------------------------------

    misconception_id = None
    misconception = None

    # --------------------------------------
    # If wrong, find misconception
    # --------------------------------------

    if not is_correct:

        misconception_id = (
            find_misconception_from_answer(
                mappings,
                question_id,
                selected_answer
            )
        )

        if misconception_id:

            misconception = (
                find_misconception(
                    misconceptions,
                    misconception_id
                )
            )

    # ======================================
    # CREATE RESPONSE RECORD
    # ======================================

    response = {

        "student_id": student_id,

        "question_id": question_id,

        "selected_answer": selected_answer,

        "correct_answer": correct_answer,

        "is_correct": is_correct,

        "concept": question.get(
            "concept"
        ),

        "misconception_id":
            misconception_id,

        "misconception":
            (
                misconception.get(
                    "misconception"
                )
                if misconception
                else None
            )
    }

    return response


# ==========================================
# DISPLAY RESULT
# ==========================================

def display_result(response):

    print(
        "\n============================"
    )

    print(
        "      RESPONSE RESULT"
    )

    print(
        "============================"
    )

    print(
        f"Student: "
        f"{response['student_id']}"
    )

    print(
        f"Question: "
        f"{response['question_id']}"
    )

    print(
        f"Selected: "
        f"{response['selected_answer']}"
    )

    print(
        f"Correct answer: "
        f"{response['correct_answer']}"
    )

    if response["is_correct"]:

        print(
            "\n✓ Correct answer"
        )

        print(
            "No misconception detected."
        )

    else:

        print(
            "\n❌ Incorrect answer"
        )

        if response[
            "misconception_id"
        ]:

            print(
                "\n⚠ Possible misconception:"
            )

            print(
                f"ID: "
                f"{response['misconception_id']}"
            )

            print(
                f"Description: "
                f"{response['misconception']}"
            )

        else:

            print(
                "\n⚠ No mapped misconception "
                "was found for this answer."
            )

    print(
        "============================"
    )


# ==========================================
# MAIN
# ==========================================

def main():

    print("""
============================
 ADAPTIQ STUDENT RESPONSE
       PROCESSOR
============================
""")

    # --------------------------------------
    # Load files
    # --------------------------------------

    questions = load_json(
        QUESTIONS_FILE
    )

    misconceptions = load_json(
        MISCONCEPTIONS_FILE
    )

    mappings = load_json(
        MAPPING_FILE
    )

    responses = load_json(
        RESPONSES_FILE
    )

    if (
        questions is None
        or misconceptions is None
        or mappings is None
        or responses is None
    ):

        print(
            "\n❌ Could not load required data."
        )

        return

    # --------------------------------------
    # Student ID
    # --------------------------------------

    student_id = input(
        "Enter student ID: "
    ).strip()

    if not student_id:

        print(
            "❌ Student ID cannot be empty."
        )

        return

    # --------------------------------------
    # Question ID
    # --------------------------------------

    question_id = input(
        "Enter question ID: "
    ).strip()

    question = find_question(
        questions,
        question_id
    )

    if question is None:

        print(
            f"❌ Question "
            f"{question_id} not found."
        )

        return

    # --------------------------------------
    # Display question
    # --------------------------------------

    print(
        "\nQuestion:"
    )

    print(
        question["question"]
    )

    print(
        "\nOptions:"
    )

    for index, option in enumerate(
        question["options"],
        start=1
    ):

        print(
            f"{index}. {option}"
        )

    # --------------------------------------
    # Student answer
    # --------------------------------------

    try:

        choice = int(
            input(
                "\nSelect option (1-4): "
            )
        )

    except ValueError:

        print(
            "❌ Enter a number from 1 to 4."
        )

        return

    if choice < 1 or choice > 4:

        print(
            "❌ Invalid option."
        )

        return

    selected_answer = (
        question["options"][
            choice - 1
        ]
    )

    # --------------------------------------
    # Process
    # --------------------------------------

    response = process_response(
        student_id,
        question_id,
        selected_answer,
        questions,
        misconceptions,
        mappings
    )

    if response is None:

        return

    # --------------------------------------
    # Save response
    # --------------------------------------

    responses.append(
        response
    )

    save_json(
        RESPONSES_FILE,
        responses
    )

    # --------------------------------------
    # Display result
    # --------------------------------------

    display_result(
        response
    )

    print(
        "\n✓ Response saved."
    )


# ==========================================
# ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()