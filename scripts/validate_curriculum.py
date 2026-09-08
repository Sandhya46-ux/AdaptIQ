import json
import re
from pathlib import Path


# ============================================================
# ADAPTIQ CURRICULUM VALIDATOR
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CURRICULUM_DIR = BASE_DIR / "data" / "curriculum"

VALID_CLASSES = [9, 10, 11, 12]

VALID_SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology"
]

# Only directories such as:
# 2026-27
# 2027-28
# 2028-29
# will be treated as curriculum versions.
VERSION_PATTERN = re.compile(r"^\d{4}-\d{2}$")


# ============================================================
# HELPERS
# ============================================================

def load_json(file_path):
    """Load JSON file safely."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON: {error}"
        )

    except Exception as error:
        raise ValueError(
            f"Could not read file: {error}"
        )


def validate_required_fields(data, required_fields):
    """Check whether required fields exist."""
    errors = []

    for field in required_fields:
        if field not in data:
            errors.append(
                f"Missing required field '{field}'"
            )

    return errors


# ============================================================
# VALIDATE ONE CURRICULUM FILE
# ============================================================

def validate_file(file_path):
    """Validate one curriculum JSON file."""

    errors = []

    try:
        data = load_json(file_path)
    except ValueError as error:
        return [str(error)]

    # --------------------------------------------------------
    # Required top-level fields
    # --------------------------------------------------------

    required_fields = [
        "curriculum_version",
        "board",
        "class",
        "subject",
        "source",
        "chapters"
    ]

    errors.extend(
        validate_required_fields(
            data,
            required_fields
        )
    )

    if errors:
        return errors

    # --------------------------------------------------------
    # Basic information
    # --------------------------------------------------------

    curriculum_version = data["curriculum_version"]
    class_number = data["class"]
    subject = data["subject"]
    chapters = data["chapters"]

    # --------------------------------------------------------
    # Version validation
    # --------------------------------------------------------

    if not VERSION_PATTERN.match(
        str(curriculum_version)
    ):
        errors.append(
            f"Invalid curriculum_version "
            f"'{curriculum_version}'. "
            f"Expected format YYYY-YY."
        )

    # --------------------------------------------------------
    # Class validation
    # --------------------------------------------------------

    if class_number not in VALID_CLASSES:
        errors.append(
            f"Invalid class '{class_number}'. "
            f"Allowed classes: {VALID_CLASSES}"
        )

    # --------------------------------------------------------
    # Subject validation
    # --------------------------------------------------------

    if subject not in VALID_SUBJECTS:
        errors.append(
            f"Invalid subject '{subject}'. "
            f"Allowed subjects: {VALID_SUBJECTS}"
        )

    # --------------------------------------------------------
    # Chapters validation
    # --------------------------------------------------------

    if not isinstance(chapters, list):
        errors.append(
            "'chapters' must be a list."
        )
        return errors

    if len(chapters) == 0:
        errors.append(
            "Curriculum contains no chapters."
        )
        return errors

    # --------------------------------------------------------
    # First pass:
    # Collect every concept ID in this curriculum file.
    #
    # This allows a concept to use another concept as a
    # prerequisite even if that prerequisite appears later
    # in the JSON file.
    # --------------------------------------------------------

    all_concept_ids = set()

    for chapter in chapters:

        if not isinstance(chapter, dict):
            continue

        concepts = chapter.get(
            "concepts",
            []
        )

        if not isinstance(concepts, list):
            continue

        for concept in concepts:

            if not isinstance(concept, dict):
                continue

            concept_id = concept.get(
                "concept_id"
            )

            if concept_id:
                all_concept_ids.add(
                    concept_id
                )

    # --------------------------------------------------------
    # Duplicate tracking
    # --------------------------------------------------------

    chapter_ids = set()
    concept_ids = set()

    # --------------------------------------------------------
    # Second pass:
    # Validate chapters and concepts
    # --------------------------------------------------------

    for chapter_index, chapter in enumerate(chapters):

        if not isinstance(chapter, dict):

            errors.append(
                f"Chapter {chapter_index + 1} "
                f"must be an object."
            )

            continue

        # ----------------------------------------------------
        # Chapter required fields
        # ----------------------------------------------------

        chapter_required = [
            "chapter_id",
            "chapter",
            "concepts"
        ]

        for field in chapter_required:

            if field not in chapter:

                errors.append(
                    f"Chapter {chapter_index + 1}: "
                    f"missing '{field}'."
                )

        chapter_id = chapter.get(
            "chapter_id"
        )

        chapter_name = chapter.get(
            "chapter"
        )

        concepts = chapter.get(
            "concepts"
        )

        # ----------------------------------------------------
        # Chapter ID
        # ----------------------------------------------------

        if chapter_id:

            if chapter_id in chapter_ids:

                errors.append(
                    f"Duplicate chapter_id "
                    f"'{chapter_id}'."
                )

            chapter_ids.add(
                chapter_id
            )

        # ----------------------------------------------------
        # Chapter name
        # ----------------------------------------------------

        if not chapter_name:

            errors.append(
                f"Chapter {chapter_index + 1}: "
                f"chapter name cannot be empty."
            )

        # ----------------------------------------------------
        # Concepts
        # ----------------------------------------------------

        if not isinstance(concepts, list):

            errors.append(
                f"Chapter '{chapter_name}': "
                f"'concepts' must be a list."
            )

            continue

        if len(concepts) == 0:

            errors.append(
                f"Chapter '{chapter_name}': "
                f"no concepts found."
            )

            continue

        # ----------------------------------------------------
        # Validate each concept
        # ----------------------------------------------------

        for concept_index, concept in enumerate(
            concepts
        ):

            if not isinstance(concept, dict):

                errors.append(
                    f"Chapter '{chapter_name}', "
                    f"concept {concept_index + 1}: "
                    f"must be an object."
                )

                continue

            concept_required = [
                "concept_id",
                "concept",
                "prerequisites",
                "learning_outcomes"
            ]

            for field in concept_required:

                if field not in concept:

                    errors.append(
                        f"Chapter '{chapter_name}', "
                        f"concept {concept_index + 1}: "
                        f"missing '{field}'."
                    )

            concept_id = concept.get(
                "concept_id"
            )

            concept_name = concept.get(
                "concept"
            )

            prerequisites = concept.get(
                "prerequisites"
            )

            learning_outcomes = concept.get(
                "learning_outcomes"
            )

            # ------------------------------------------------
            # Concept ID
            # ------------------------------------------------

            if concept_id:

                if concept_id in concept_ids:

                    errors.append(
                        f"Duplicate concept_id "
                        f"'{concept_id}'."
                    )

                concept_ids.add(
                    concept_id
                )

            # ------------------------------------------------
            # Concept name
            # ------------------------------------------------

            if not concept_name:

                errors.append(
                    f"Concept '{concept_id}': "
                    f"concept name cannot be empty."
                )

            # ------------------------------------------------
            # Prerequisites
            # ------------------------------------------------

            if not isinstance(
                prerequisites,
                list
            ):

                errors.append(
                    f"Concept '{concept_id}': "
                    f"'prerequisites' must be a list."
                )

            else:

                for prerequisite in prerequisites:

                    if prerequisite not in all_concept_ids:

                        errors.append(
                            f"Concept '{concept_id}': "
                            f"prerequisite "
                            f"'{prerequisite}' "
                            f"does not exist."
                        )

            # ------------------------------------------------
            # Learning outcomes
            # ------------------------------------------------

            if not isinstance(
                learning_outcomes,
                list
            ):

                errors.append(
                    f"Concept '{concept_id}': "
                    f"'learning_outcomes' "
                    f"must be a list."
                )

    return errors


# ============================================================
# FIND CURRICULUM VERSIONS
# ============================================================

def find_versions():
    """
    Find only valid curriculum version directories.

    Valid:
        2026-27
        2027-28

    Ignored:
        class_9
        class_10
        class_11
        class_12
        drafts
        reports
    """

    if not CURRICULUM_DIR.exists():
        return []

    versions = []

    for directory in CURRICULUM_DIR.iterdir():

        if not directory.is_dir():
            continue

        if VERSION_PATTERN.match(
            directory.name
        ):
            versions.append(
                directory
            )

    return sorted(
        versions,
        key=lambda path: path.name
    )


# ============================================================
# FIND CURRICULUM FILES
# ============================================================

def find_curriculum_files(version_dir):
    """Find curriculum JSON files under class folders."""

    files = []

    for class_dir in sorted(
        version_dir.glob("class_*")
    ):

        if not class_dir.is_dir():
            continue

        # Only class_9 to class_12
        class_name = class_dir.name

        if not re.match(
            r"^class_(9|10|11|12)$",
            class_name
        ):
            continue

        for json_file in sorted(
            class_dir.glob("*.json")
        ):

            files.append(
                json_file
            )

    return files


# ============================================================
# VALIDATE VERSION
# ============================================================

def validate_version(version_dir):

    print()
    print(
        f"CURRICULUM VERSION: "
        f"{version_dir.name}"
    )
    print("-" * 40)

    files = find_curriculum_files(
        version_dir
    )

    if not files:

        print(
            "WARNING: No curriculum files found."
        )

        return 0, 0

    passed = 0
    failed = 0

    for file_path in files:

        errors = validate_file(
            file_path
        )

        if errors:

            failed += 1

            print(
                f"FAIL: {file_path}"
            )

            for error in errors:

                print(
                    f"  - {error}"
                )

        else:

            passed += 1

            print(
                f"PASS: {file_path}"
            )

    return passed, failed


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 40)
    print(
        "      ADAPTIQ CURRICULUM VALIDATOR"
    )
    print("=" * 40)

    if not CURRICULUM_DIR.exists():

        print()
        print(
            "ERROR: Curriculum directory "
            "does not exist:"
        )

        print(
            CURRICULUM_DIR
        )

        return 1

    versions = find_versions()

    if not versions:

        print()
        print(
            "ERROR: No curriculum versions found."
        )

        print(
            "Expected folders such as:"
        )

        print(
            "  data/curriculum/2026-27/"
        )

        return 1

    total_files = 0
    total_passed = 0
    total_failed = 0

    for version_dir in versions:

        passed, failed = validate_version(
            version_dir
        )

        total_passed += passed
        total_failed += failed

        total_files += (
            passed + failed
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 40)
    print("VALIDATION SUMMARY")
    print("=" * 40)

    print(
        f"Total files : {total_files}"
    )

    print(
        f"Passed      : {total_passed}"
    )

    print(
        f"Failed      : {total_failed}"
    )

    print()

    if total_failed == 0:

        print(
            "CURRICULUM VALIDATION PASSED"
        )

        return 0

    else:

        print(
            "CURRICULUM VALIDATION FAILED"
        )

        return 1


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    raise SystemExit(
        main()
    )