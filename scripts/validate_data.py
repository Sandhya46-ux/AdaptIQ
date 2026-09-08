import json
import sys
from pathlib import Path


# ============================================================
# ADAPTIQ DATA VALIDATOR
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_FILE = (
    BASE_DIR
    / "data"
    / "questions"
    / "physics_questions.json"
)


REQUIRED_FIELDS = [
    "id",
    "class",
    "subject",
    "chapter",
    "concept",
    "difficulty",
    "question",
    "options",
    "answer",
    "explanation",
    "tags"
]


VALID_CLASSES = [9, 10, 11, 12]

VALID_DIFFICULTIES = [
    "easy",
    "medium",
    "hard"
]


# ============================================================
# VALIDATE ONE QUESTION
# ============================================================

def validate_question(question):

    errors = []

    # Required fields
    for field in REQUIRED_FIELDS:

        if field not in question:

            errors.append(
                f"Missing field: {field}"
            )

    if errors:
        return errors

    # Class
    if question["class"] not in VALID_CLASSES:

        errors.append(
            f"Invalid class: {question['class']}"
        )

    # Subject
    if question["subject"].lower() != "physics":

        errors.append(
            f"Invalid subject: "
            f"{question['subject']}"
        )

    # Difficulty
    if (
        question["difficulty"].lower()
        not in VALID_DIFFICULTIES
    ):

        errors.append(
            f"Invalid difficulty: "
            f"{question['difficulty']}"
        )

    # Question
    if not question["question"].strip():

        errors.append(
            "Question cannot be empty"
        )

    # Concept
    if not question["concept"].strip():

        errors.append(
            "Concept cannot be empty"
        )

    # Options
    options = question["options"]

    if not isinstance(options, list):

        errors.append(
            "Options must be a list"
        )

    elif len(options) != 4:

        errors.append(
            "Exactly 4 options are required"
        )

    else:

        # Correct answer must be an option
        if question["answer"] not in options:

            errors.append(
                "Correct answer is not "
                "present in options"
            )

    return errors


# ============================================================
# VALIDATE COMPLETE DATASET
# ============================================================

def validate_dataset(data):

    total_errors = 0

    seen_ids = set()

    seen_questions = set()

    print(
        "\n============================"
    )

    print(
        "   ADAPTIQ DATA VALIDATOR"
    )

    print(
        "============================\n"
    )

    for index, question in enumerate(
        data,
        start=1
    ):

        question_id = question.get(
            "id",
            f"Question #{index}"
        )

        errors = validate_question(
            question
        )

        # Duplicate ID
        if question_id in seen_ids:

            errors.append(
                f"Duplicate ID: {question_id}"
            )

        seen_ids.add(question_id)

        # Duplicate question
        question_text = (
            question.get(
                "question",
                ""
            )
            .strip()
            .lower()
        )

        if question_text in seen_questions:

            errors.append(
                "Duplicate question text"
            )

        seen_questions.add(
            question_text
        )

        if errors:

            total_errors += len(errors)

            print(
                f"❌ {question_id}"
            )

            for error in errors:

                print(
                    f"   → {error}"
                )

        else:

            print(
                f"✓ {question_id}"
            )

    print(
        "\n----------------------------"
    )

    print(
        f"Questions checked: {len(data)}"
    )

    print(
        f"Errors found: {total_errors}"
    )

    if total_errors == 0:

        print(
            "Status: PASS ✓"
        )

    else:

        print(
            "Status: FAIL ❌"
        )

    print(
        "----------------------------"
    )

    return total_errors == 0


# ============================================================
# LOAD JSON
# ============================================================

def load_json(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):

            print(
                "❌ Dataset must be a JSON array."
            )

            return None

        return data

    except FileNotFoundError:

        print(
            f"❌ File not found:\n{file_path}"
        )

        return None

    except json.JSONDecodeError as error:

        print(
            "❌ Invalid JSON:"
        )

        print(error)

        return None


# ============================================================
# MAIN
# ============================================================

def main():

    # Allow optional file path
    if len(sys.argv) > 1:

        file_path = Path(
            sys.argv[1]
        )

    else:

        file_path = DEFAULT_FILE

    data = load_json(
        file_path
    )

    if data is None:

        sys.exit(1)

    valid = validate_dataset(
        data
    )

    if valid:

        sys.exit(0)

    else:

        sys.exit(1)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()