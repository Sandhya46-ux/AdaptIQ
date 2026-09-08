import json
import sys
from pathlib import Path


# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MISCONCEPTIONS_FILE = (
    BASE_DIR
    / "data"
    / "misconceptions"
    / "physics_misconceptions.json"
)

VALID_CLASSES = [9, 10, 11, 12]

VALID_SEVERITIES = [
    "low",
    "medium",
    "high"
]

REQUIRED_FIELDS = [
    "misconception_id",
    "class",
    "subject",
    "chapter",
    "concept",
    "misconception",
    "correct_understanding",
    "common_wrong_answer",
    "severity",
    "tags"
]


# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    if not MISCONCEPTIONS_FILE.exists():

        print(
            f"❌ File not found:\n"
            f"{MISCONCEPTIONS_FILE}"
        )

        return None

    try:

        with open(
            MISCONCEPTIONS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError as error:

        print("❌ Invalid JSON format.")
        print(error)

        return None

    except Exception as error:

        print("❌ Could not read file.")
        print(error)

        return None


# ==========================================
# VALIDATE ONE MISCONCEPTION
# ==========================================

def validate_misconception(
    misconception,
    index
):

    errors = []

    # --------------------------------------
    # Object check
    # --------------------------------------

    if not isinstance(
        misconception,
        dict
    ):

        errors.append(
            f"Record {index}: "
            "must be a JSON object"
        )

        return errors

    # --------------------------------------
    # Required fields
    # --------------------------------------

    for field in REQUIRED_FIELDS:

        if field not in misconception:

            errors.append(
                f"Record {index}: "
                f"missing '{field}'"
            )

    # Stop deeper validation if fields missing
    if any(
        field not in misconception
        for field in REQUIRED_FIELDS
    ):

        return errors

    # --------------------------------------
    # Misconception ID
    # --------------------------------------

    if not isinstance(
        misconception["misconception_id"],
        str
    ):

        errors.append(
            f"Record {index}: "
            "misconception_id must be text"
        )

    elif not misconception[
        "misconception_id"
    ].strip():

        errors.append(
            f"Record {index}: "
            "misconception_id is empty"
        )

    # --------------------------------------
    # Class
    # --------------------------------------

    if misconception["class"] not in VALID_CLASSES:

        errors.append(
            f"Record {index}: "
            "invalid class"
        )

    # --------------------------------------
    # Subject
    # --------------------------------------

    if misconception[
        "subject"
    ].lower() != "physics":

        errors.append(
            f"Record {index}: "
            "subject must be Physics"
        )

    # --------------------------------------
    # Text fields
    # --------------------------------------

    text_fields = [
        "chapter",
        "concept",
        "misconception",
        "correct_understanding",
        "common_wrong_answer"
    ]

    for field in text_fields:

        value = misconception[field]

        if not isinstance(
            value,
            str
        ):

            errors.append(
                f"Record {index}: "
                f"'{field}' must be text"
            )

        elif not value.strip():

            errors.append(
                f"Record {index}: "
                f"'{field}' is empty"
            )

    # --------------------------------------
    # Severity
    # --------------------------------------

    if misconception[
        "severity"
    ] not in VALID_SEVERITIES:

        errors.append(
            f"Record {index}: "
            f"invalid severity "
            f"'{misconception['severity']}'"
        )

    # --------------------------------------
    # Tags
    # --------------------------------------

    tags = misconception["tags"]

    if not isinstance(
        tags,
        list
    ):

        errors.append(
            f"Record {index}: "
            "tags must be a list"
        )

    else:

        if len(tags) == 0:

            errors.append(
                f"Record {index}: "
                "tags cannot be empty"
            )

        for tag in tags:

            if not isinstance(
                tag,
                str
            ) or not tag.strip():

                errors.append(
                    f"Record {index}: "
                    "tags must contain "
                    "non-empty text"
                )

    return errors


# ==========================================
# VALIDATE COMPLETE DATASET
# ==========================================

def validate_dataset(data):

    errors = []

    # --------------------------------------
    # Dataset must be list
    # --------------------------------------

    if not isinstance(
        data,
        list
    ):

        print(
            "❌ Dataset must be a JSON list."
        )

        return False

    # --------------------------------------
    # Empty dataset
    # --------------------------------------

    if len(data) == 0:

        print(
            "⚠️ Dataset contains no misconceptions."
        )

        return False

    # --------------------------------------
    # Duplicate IDs
    # --------------------------------------

    misconception_ids = set()

    # --------------------------------------
    # Duplicate descriptions
    # --------------------------------------

    misconception_texts = set()

    # --------------------------------------
    # Validate each record
    # --------------------------------------

    for index, misconception in enumerate(
        data,
        start=1
    ):

        record_errors = validate_misconception(
            misconception,
            index
        )

        errors.extend(record_errors)

        # Check duplicates only for valid objects
        if isinstance(
            misconception,
            dict
        ):

            misconception_id = (
                misconception.get(
                    "misconception_id"
                )
            )

            if misconception_id:

                if misconception_id in misconception_ids:

                    errors.append(
                        f"Record {index}: "
                        f"duplicate misconception_id "
                        f"'{misconception_id}'"
                    )

                else:

                    misconception_ids.add(
                        misconception_id
                    )

            misconception_text = (
                misconception.get(
                    "misconception"
                )
            )

            if misconception_text:

                normalized_text = (
                    misconception_text
                    .strip()
                    .lower()
                )

                if normalized_text in misconception_texts:

                    errors.append(
                        f"Record {index}: "
                        "duplicate misconception text"
                    )

                else:

                    misconception_texts.add(
                        normalized_text
                    )

    # ======================================
    # RESULT
    # ======================================

    if errors:

        print(
            "\n❌ Validation errors found:"
        )

        for error in errors:

            print(
                f"   → {error}"
            )

        return False

    # Success
    print(
        "\n✓ All misconception records "
        "passed validation."
    )

    print(
        f"Misconceptions checked: {len(data)}"
    )

    return True


# ==========================================
# MAIN
# ==========================================

def main():

    print("""
============================
 ADAPTIQ MISCONCEPTION
       VALIDATOR
============================
""")

    data = load_data()

    if data is None:

        print(
            "\nStatus: FAIL ❌"
        )

        sys.exit(1)

    success = validate_dataset(
        data
    )

    print(
        "\n----------------------------"
    )

    if success:

        print(
            "Status: PASS ✓"
        )

        print(
            "----------------------------"
        )

        sys.exit(0)

    else:

        print(
            "Status: FAIL ❌"
        )

        print(
            "----------------------------"
        )

        sys.exit(1)


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()