import json
from pathlib import Path


CURRICULUM_DIR = Path("data/curriculum")

VALID_CLASSES = [9, 10, 11, 12]

VALID_SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology"
]

REQUIRED_TOP_LEVEL_FIELDS = [
    "curriculum_version",
    "board",
    "class",
    "subject",
    "source",
    "chapters"
]

REQUIRED_CONCEPT_FIELDS = [
    "concept_id",
    "concept",
    "prerequisites",
    "learning_outcomes"
]


def validate_file(file_path):

    errors = []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as error:

        return [f"Invalid JSON: {error}"]

    except Exception as error:

        return [f"Could not read file: {error}"]

    # -----------------------------------------
    # Top-level fields
    # -----------------------------------------

    for field in REQUIRED_TOP_LEVEL_FIELDS:

        if field not in data:

            errors.append(
                f"Missing top-level field: {field}"
            )

    if errors:
        return errors

    # -----------------------------------------
    # Class
    # -----------------------------------------

    if data["class"] not in VALID_CLASSES:

        errors.append(
            f"Invalid class: {data['class']}"
        )

    # -----------------------------------------
    # Subject
    # -----------------------------------------

    if data["subject"] not in VALID_SUBJECTS:

        errors.append(
            f"Invalid subject: {data['subject']}"
        )

    # -----------------------------------------
    # Source
    # -----------------------------------------

    if not isinstance(data["source"], dict):

        errors.append(
            "source must be an object"
        )

    # -----------------------------------------
    # Chapters
    # -----------------------------------------

    if not isinstance(data["chapters"], list):

        errors.append(
            "chapters must be a list"
        )

        return errors

    chapter_ids = set()
    concept_ids = set()

    # -----------------------------------------
    # First pass:
    # Collect all chapter and concept IDs
    # -----------------------------------------

    for chapter_index, chapter in enumerate(
        data["chapters"],
        start=1
    ):

        if not isinstance(chapter, dict):

            errors.append(
                f"Chapter {chapter_index} "
                f"must be an object"
            )

            continue

        chapter_id = chapter.get("chapter_id")

        if not chapter_id:

            errors.append(
                f"Chapter {chapter_index}: "
                f"missing chapter_id"
            )

        else:

            if chapter_id in chapter_ids:

                errors.append(
                    f"Duplicate chapter_id: "
                    f"{chapter_id}"
                )

            chapter_ids.add(chapter_id)

        if "chapter" not in chapter:

            errors.append(
                f"Chapter {chapter_index}: "
                f"missing chapter name"
            )

        if "concepts" not in chapter:

            errors.append(
                f"Chapter {chapter_id}: "
                f"missing concepts"
            )

            continue

        if not isinstance(
            chapter["concepts"],
            list
        ):

            errors.append(
                f"Chapter {chapter_id}: "
                f"concepts must be a list"
            )

            continue

        for concept in chapter["concepts"]:

            if not isinstance(concept, dict):

                errors.append(
                    f"Invalid concept in "
                    f"chapter {chapter_id}"
                )

                continue

            concept_id = concept.get(
                "concept_id"
            )

            if concept_id:

                if concept_id in concept_ids:

                    errors.append(
                        f"Duplicate concept_id: "
                        f"{concept_id}"
                    )

                concept_ids.add(concept_id)

    # -----------------------------------------
    # Second pass:
    # Validate concepts
    # -----------------------------------------

    for chapter in data["chapters"]:

        chapter_id = chapter.get(
            "chapter_id",
            "UNKNOWN"
        )

        concepts = chapter.get(
            "concepts",
            []
        )

        for concept in concepts:

            if not isinstance(concept, dict):
                continue

            concept_id = concept.get(
                "concept_id",
                "UNKNOWN"
            )

            # Required fields

            for field in REQUIRED_CONCEPT_FIELDS:

                if field not in concept:

                    errors.append(
                        f"Concept {concept_id}: "
                        f"missing field '{field}'"
                    )

            # Concept name

            concept_name = concept.get(
                "concept"
            )

            if not isinstance(
                concept_name,
                str
            ):

                errors.append(
                    f"Concept {concept_id}: "
                    f"concept must be text"
                )

            elif not concept_name.strip():

                errors.append(
                    f"Concept {concept_id}: "
                    f"concept cannot be empty"
                )

            # Prerequisites

            prerequisites = concept.get(
                "prerequisites"
            )

            if not isinstance(
                prerequisites,
                list
            ):

                errors.append(
                    f"Concept {concept_id}: "
                    f"prerequisites must be a list"
                )

            else:

                for prerequisite_id in prerequisites:

                    if prerequisite_id not in concept_ids:

                        errors.append(
                            f"Concept {concept_id}: "
                            f"prerequisite "
                            f"'{prerequisite_id}' "
                            f"does not exist"
                        )

            # Learning outcomes

            learning_outcomes = concept.get(
                "learning_outcomes"
            )

            if not isinstance(
                learning_outcomes,
                list
            ):

                errors.append(
                    f"Concept {concept_id}: "
                    f"learning_outcomes must be a list"
                )

    return errors


def main():

    if not CURRICULUM_DIR.exists():

        print(
            "ERROR: Curriculum directory not found."
        )

        return 1

    version_dirs = [
        path
        for path in CURRICULUM_DIR.iterdir()
        if path.is_dir()
        and path.name != "reports"
        and path.name != "drafts"
    ]

    if not version_dirs:

        print(
            "ERROR: No curriculum versions found."
        )

        return 1

    total_files = 0
    passed_files = 0
    failed_files = 0

    print("\n========================================")
    print("      ADAPTIQ CURRICULUM VALIDATOR")
    print("========================================\n")

    for version_dir in sorted(version_dirs):

        print(
            f"CURRICULUM VERSION: "
            f"{version_dir.name}"
        )

        print("-" * 40)

        json_files = sorted(
            version_dir.glob(
                "class_*/*.json"
            )
        )

        if not json_files:

            print(
                "WARNING: No curriculum files found.\n"
            )

            continue

        for file_path in json_files:

            total_files += 1

            errors = validate_file(
                file_path
            )

            if errors:

                failed_files += 1

                print(
                    f"FAIL: {file_path}"
                )

                for error in errors:

                    print(
                        f"  - {error}"
                    )

            else:

                passed_files += 1

                print(
                    f"PASS: {file_path}"
                )

        print()

    print("========================================")
    print("VALIDATION SUMMARY")
    print("========================================")

    print(
        f"Total files : {total_files}"
    )

    print(
        f"Passed      : {passed_files}"
    )

    print(
        f"Failed      : {failed_files}"
    )

    if (
        failed_files == 0
        and total_files > 0
    ):

        print(
            "\nCURRICULUM VALIDATION PASSED"
        )

        return 0

    print(
        "\nCURRICULUM VALIDATION FAILED"
    )

    return 1


if __name__ == "__main__":

    raise SystemExit(main())