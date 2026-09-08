import json
from pathlib import Path

# Root curriculum directory
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

    # -----------------------------
    # Load JSON
    # -----------------------------
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]
    except Exception as e:
        return [f"Could not read file: {e}"]

    # -----------------------------
    # Top-level fields
    # -----------------------------
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            errors.append(f"Missing top-level field: {field}")

    if errors:
        return errors

    # -----------------------------
    # Class validation
    # -----------------------------
    if data["class"] not in VALID_CLASSES:
        errors.append(
            f"Invalid class: {data['class']}. "
            f"Expected one of {VALID_CLASSES}"
        )

    # -----------------------------
    # Subject validation
    # -----------------------------
    if data["subject"] not in VALID_SUBJECTS:
        errors.append(
            f"Invalid subject: {data['subject']}. "
            f"Expected one of {VALID_SUBJECTS}"
        )

    # -----------------------------
    # Source validation
    # -----------------------------
    if not isinstance(data["source"], dict):
        errors.append("source must be an object")

    # -----------------------------
    # Chapters validation
    # -----------------------------
    if not isinstance(data["chapters"], list):
        errors.append("chapters must be a list")
        return errors

    chapter_ids = set()
    concept_ids = set()

    for chapter_index, chapter in enumerate(data["chapters"], start=1):

        if not isinstance(chapter, dict):
            errors.append(
                f"Chapter {chapter_index} must be an object"
            )
            continue

        # Chapter fields
        if "chapter_id" not in chapter:
            errors.append(
                f"Chapter {chapter_index}: missing chapter_id"
            )

        if "chapter" not in chapter:
            errors.append(
                f"Chapter {chapter_index}: missing chapter name"
            )

        if "concepts" not in chapter:
            errors.append(
                f"Chapter {chapter_index}: missing concepts"
            )
            continue

        # Duplicate chapter ID
        chapter_id = chapter.get("chapter_id")

        if chapter_id in chapter_ids:
            errors.append(
                f"Duplicate chapter_id: {chapter_id}"
            )

        chapter_ids.add(chapter_id)

        # Concepts must be list
        if not isinstance(chapter["concepts"], list):
            errors.append(
                f"Chapter {chapter_id}: concepts must be a list"
            )
            continue

        # -----------------------------
        # Concept validation
        # -----------------------------
        for concept_index, concept in enumerate(
            chapter["concepts"], start=1
        ):

            if not isinstance(concept, dict):
                errors.append(
                    f"Chapter {chapter_id}, concept "
                    f"{concept_index}: must be an object"
                )
                continue

            for field in REQUIRED_CONCEPT_FIELDS:
                if field not in concept:
                    errors.append(
                        f"Concept in {chapter_id}: "
                        f"missing field '{field}'"
                    )

            if "concept_id" not in concept:
                continue

            concept_id = concept["concept_id"]

            # Duplicate concept ID
            if concept_id in concept_ids:
                errors.append(
                    f"Duplicate concept_id: {concept_id}"
                )

            concept_ids.add(concept_id)

            # Concept name
            if "concept" in concept:
                if not isinstance(concept["concept"], str):
                    errors.append(
                        f"Concept {concept_id}: "
                        f"concept must be text"
                    )
                elif not concept["concept"].strip():
                    errors.append(
                        f"Concept {concept_id}: "
                        f"concept cannot be empty"
                    )

            # Prerequisites
            if "prerequisites" in concept:
                if not isinstance(
                    concept["prerequisites"], list
                ):
                    errors.append(
                        f"Concept {concept_id}: "
                        f"prerequisites must be a list"
                    )

            # Learning outcomes
            if "learning_outcomes" in concept:
                if not isinstance(
                    concept["learning_outcomes"], list
                ):
                    errors.append(
                        f"Concept {concept_id}: "
                        f"learning_outcomes must be a list"
                    )

    return errors


def main():

    if not CURRICULUM_DIR.exists():
        print("ERROR: Curriculum directory not found.")
        return 1

    # Find version folders such as 2026-27
    version_dirs = [
        p for p in CURRICULUM_DIR.iterdir()
        if p.is_dir()
    ]

    if not version_dirs:
        print("ERROR: No curriculum versions found.")
        return 1

    total_files = 0
    passed_files = 0
    failed_files = 0

    print("\n========================================")
    print("      ADAPTIQ CURRICULUM VALIDATOR")
    print("========================================\n")

    for version_dir in sorted(version_dirs):

        print(f"CURRICULUM VERSION: {version_dir.name}")
        print("-" * 40)

        json_files = sorted(
            version_dir.glob("class_*/*.json")
        )

        if not json_files:
            print("WARNING: No curriculum files found.\n")
            continue

        for file_path in json_files:

            total_files += 1

            errors = validate_file(file_path)

            if errors:
                failed_files += 1

                print(f"FAIL: {file_path}")

                for error in errors:
                    print(f"  - {error}")

            else:
                passed_files += 1
                print(f"PASS: {file_path}")

        print()

    # -----------------------------
    # Final summary
    # -----------------------------
    print("========================================")
    print("VALIDATION SUMMARY")
    print("========================================")

    print(f"Total files : {total_files}")
    print(f"Passed      : {passed_files}")
    print(f"Failed      : {failed_files}")

    if failed_files == 0 and total_files > 0:
        print("\nCURRICULUM VALIDATION PASSED")
        return 0

    print("\nCURRICULUM VALIDATION FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())