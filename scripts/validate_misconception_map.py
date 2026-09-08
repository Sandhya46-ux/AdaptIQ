import json
import sys
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


# ==========================================
# LOAD JSON FILE
# ==========================================

def load_json(file_path):

    if not file_path.exists():

        print(f"❌ File not found:")
        print(file_path)

        return None

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError as error:

        print(f"❌ Invalid JSON:")
        print(file_path)
        print(error)

        return None

    except Exception as error:

        print(f"❌ Could not read file:")
        print(error)

        return None


# ==========================================
# MAIN VALIDATION
# ==========================================

def main():

    print("""
============================
 ADAPTIQ MISCONCEPTION
     MAP VALIDATOR
============================
""")

    # --------------------------------------
    # Load all files
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

    # --------------------------------------
    # Stop if any file failed
    # --------------------------------------

    if (
        questions is None
        or misconceptions is None
        or mappings is None
    ):

        print(
            "\nStatus: FAIL ❌"
        )

        sys.exit(1)

    errors = []

    # ======================================
    # CREATE LOOKUP SETS
    # ======================================

    question_ids = {
        question.get("id")
        for question in questions
        if isinstance(question, dict)
    }

    misconception_ids = {
        misconception.get(
            "misconception_id"
        )
        for misconception in misconceptions
        if isinstance(misconception, dict)
    }

    question_lookup = {
        question.get("id"): question
        for question in questions
        if isinstance(question, dict)
    }

    # ======================================
    # VALIDATE EACH MAPPING
    # ======================================

    for index, mapping in enumerate(
        mappings,
        start=1
    ):

        # ----------------------------------
        # Mapping must be object
        # ----------------------------------

        if not isinstance(
            mapping,
            dict
        ):

            errors.append(
                f"Record {index}: "
                "must be an object"
            )

            continue

        # ----------------------------------
        # Question ID
        # ----------------------------------

        question_id = mapping.get(
            "question_id"
        )

        if not question_id:

            errors.append(
                f"Record {index}: "
                "missing question_id"
            )

            continue

        # ----------------------------------
        # Check question exists
        # ----------------------------------

        if question_id not in question_ids:

            errors.append(
                f"Record {index}: "
                f"question '{question_id}' "
                "does not exist"
            )

            continue

        question = question_lookup[
            question_id
        ]

        options = question.get(
            "options",
            []
        )

        correct_answer = question.get(
            "answer"
        )

        # ----------------------------------
        # Mapping list
        # ----------------------------------

        mapping_list = mapping.get(
            "mappings"
        )

        if not isinstance(
            mapping_list,
            list
        ):

            errors.append(
                f"{question_id}: "
                "mappings must be a list"
            )

            continue

        # ----------------------------------
        # Validate every wrong answer
        # ----------------------------------

        for map_index, item in enumerate(
            mapping_list,
            start=1
        ):

            if not isinstance(
                item,
                dict
            ):

                errors.append(
                    f"{question_id}: "
                    f"mapping {map_index} "
                    "must be an object"
                )

                continue

            wrong_answer = item.get(
                "wrong_answer"
            )

            misconception_id = item.get(
                "misconception_id"
            )

            # ------------------------------
            # Check wrong answer
            # ------------------------------

            if not wrong_answer:

                errors.append(
                    f"{question_id}: "
                    "missing wrong_answer"
                )

            elif wrong_answer not in options:

                errors.append(
                    f"{question_id}: "
                    f"'{wrong_answer}' "
                    "is not an option"
                )

            elif wrong_answer == correct_answer:

                errors.append(
                    f"{question_id}: "
                    "correct answer cannot "
                    "be mapped as a misconception"
                )

            # ------------------------------
            # Check misconception ID
            # ------------------------------

            if not misconception_id:

                errors.append(
                    f"{question_id}: "
                    "missing misconception_id"
                )

            elif (
                misconception_id
                not in misconception_ids
            ):

                errors.append(
                    f"{question_id}: "
                    f"misconception "
                    f"'{misconception_id}' "
                    "does not exist"
                )

    # ======================================
    # FINAL RESULT
    # ======================================

    print(
        "\n----------------------------"
    )

    if errors:

        print(
            "❌ Mapping errors found:"
        )

        for error in errors:

            print(
                f"   → {error}"
            )

        print(
            "\nStatus: FAIL ❌"
        )

        print(
            "----------------------------"
        )

        sys.exit(1)

    print(
        "✓ All misconception mappings "
        "are valid."
    )

    print(
        f"Questions checked: "
        f"{len(question_ids)}"
    )

    print(
        f"Mappings checked: "
        f"{len(mappings)}"
    )

    print(
        "\nStatus: PASS ✓"
    )

    print(
        "----------------------------"
    )

    sys.exit(0)


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()