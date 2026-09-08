import json
from pathlib import Path


CURRICULUM_DIR = Path("data/curriculum")


def load_curriculum(file_path):
    """Load a curriculum JSON file."""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
        return None


def get_chapters(data):
    """Return chapters indexed by chapter_id."""

    return {
        chapter["chapter_id"]: chapter
        for chapter in data.get("chapters", [])
    }


def get_concepts(chapter):
    """Return concepts indexed by concept_id."""

    return {
        concept["concept_id"]: concept
        for concept in chapter.get("concepts", [])
    }


def compare_file(old_file, new_file):

    old_data = load_curriculum(old_file)
    new_data = load_curriculum(new_file)

    if old_data is None or new_data is None:
        return

    print("\n" + "=" * 60)
    print(f"SUBJECT : {new_data.get('subject')}")
    print(f"CLASS   : {new_data.get('class')}")
    print("=" * 60)

    # -----------------------------
    # Compare chapters
    # -----------------------------

    old_chapters = get_chapters(old_data)
    new_chapters = get_chapters(new_data)

    old_chapter_ids = set(old_chapters.keys())
    new_chapter_ids = set(new_chapters.keys())

    added_chapters = new_chapter_ids - old_chapter_ids
    removed_chapters = old_chapter_ids - new_chapter_ids

    if added_chapters:
        print("\n+ NEW CHAPTERS:")

        for chapter_id in sorted(added_chapters):
            print(
                f"  + {chapter_id}: "
                f"{new_chapters[chapter_id].get('chapter')}"
            )

    if removed_chapters:
        print("\n- REMOVED CHAPTERS:")

        for chapter_id in sorted(removed_chapters):
            print(
                f"  - {chapter_id}: "
                f"{old_chapters[chapter_id].get('chapter')}"
            )

    # -----------------------------
    # Compare existing chapters
    # -----------------------------

    common_chapters = old_chapter_ids & new_chapter_ids

    for chapter_id in sorted(common_chapters):

        old_chapter = old_chapters[chapter_id]
        new_chapter = new_chapters[chapter_id]

        old_name = old_chapter.get("chapter")
        new_name = new_chapter.get("chapter")

        # Chapter name changed
        if old_name != new_name:

            print("\n↔ CHAPTER RENAMED:")
            print(f"  ID : {chapter_id}")
            print(f"  OLD: {old_name}")
            print(f"  NEW: {new_name}")

        # -----------------------------
        # Compare concepts
        # -----------------------------

        old_concepts = get_concepts(old_chapter)
        new_concepts = get_concepts(new_chapter)

        old_concept_ids = set(old_concepts.keys())
        new_concept_ids = set(new_concepts.keys())

        added_concepts = new_concept_ids - old_concept_ids
        removed_concepts = old_concept_ids - new_concept_ids

        if added_concepts:

            print(
                f"\n  + NEW CONCEPTS in '{new_name}':"
            )

            for concept_id in sorted(added_concepts):

                concept_name = new_concepts[
                    concept_id
                ].get("concept")

                print(
                    f"    + {concept_id}: {concept_name}"
                )

        if removed_concepts:

            print(
                f"\n  - REMOVED CONCEPTS from '{old_name}':"
            )

            for concept_id in sorted(removed_concepts):

                concept_name = old_concepts[
                    concept_id
                ].get("concept")

                print(
                    f"    - {concept_id}: {concept_name}"
                )

        # -----------------------------
        # Compare common concepts
        # -----------------------------

        common_concepts = (
            old_concept_ids & new_concept_ids
        )

        for concept_id in sorted(common_concepts):

            old_concept = old_concepts[concept_id]
            new_concept = new_concepts[concept_id]

            old_concept_name = old_concept.get(
                "concept"
            )

            new_concept_name = new_concept.get(
                "concept"
            )

            if old_concept_name != new_concept_name:

                print("\n  ↔ CONCEPT CHANGED:")
                print(f"    ID : {concept_id}")
                print(
                    f"    OLD: {old_concept_name}"
                )
                print(
                    f"    NEW: {new_concept_name}"
                )


def compare_versions(old_version, new_version):

    old_dir = CURRICULUM_DIR / old_version
    new_dir = CURRICULUM_DIR / new_version

    if not old_dir.exists():

        print(
            f"ERROR: Old curriculum version "
            f"'{old_version}' not found."
        )

        return

    if not new_dir.exists():

        print(
            f"ERROR: New curriculum version "
            f"'{new_version}' not found."
        )

        return

    print("\n==============================================")
    print("       ADAPTIQ CURRICULUM COMPARISON")
    print("==============================================")

    print(f"\nOLD VERSION : {old_version}")
    print(f"NEW VERSION : {new_version}")

    # -----------------------------
    # Find classes
    # -----------------------------

    old_classes = {
        p.name
        for p in old_dir.iterdir()
        if p.is_dir()
    }

    new_classes = {
        p.name
        for p in new_dir.iterdir()
        if p.is_dir()
    }

    all_classes = sorted(
        old_classes | new_classes
    )

    for class_name in all_classes:

        old_class_dir = old_dir / class_name
        new_class_dir = new_dir / class_name

        print(
            f"\n\n######## {class_name.upper()} ########"
        )

        if not old_class_dir.exists():

            print(
                f"\n+ NEW CLASS FOLDER: {class_name}"
            )

            continue

        if not new_class_dir.exists():

            print(
                f"\n- REMOVED CLASS FOLDER: {class_name}"
            )

            continue

        old_files = {
            p.name
            for p in old_class_dir.glob("*.json")
        }

        new_files = {
            p.name
            for p in new_class_dir.glob("*.json")
        }

        all_files = sorted(
            old_files | new_files
        )

        for file_name in all_files:

            old_file = old_class_dir / file_name
            new_file = new_class_dir / file_name

            if not old_file.exists():

                print(
                    f"\n+ NEW SUBJECT FILE: "
                    f"{class_name}/{file_name}"
                )

                continue

            if not new_file.exists():

                print(
                    f"\n- REMOVED SUBJECT FILE: "
                    f"{class_name}/{file_name}"
                )

                continue

            compare_file(
                old_file,
                new_file
            )

    print("\n")
    print("=" * 60)
    print("COMPARISON COMPLETE")
    print("=" * 60)


def main():

    print("\n==============================================")
    print("       ADAPTIQ CURRICULUM UPDATE CHECKER")
    print("==============================================")

    old_version = input(
        "\nEnter OLD curriculum version "
        "(example: 2026-27): "
    ).strip()

    new_version = input(
        "Enter NEW curriculum version "
        "(example: 2027-28): "
    ).strip()

    if not old_version or not new_version:

        print("\nERROR: Version cannot be empty.")
        return

    if old_version == new_version:

        print(
            "\nERROR: Old and new versions "
            "must be different."
        )

        return

    compare_versions(
        old_version,
        new_version
    )


if __name__ == "__main__":
    main()