import json
from pathlib import Path
from datetime import datetime


CURRICULUM_DIR = Path("data/curriculum")
REPORT_DIR = Path("data/curriculum/reports")


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as error:
        print(f"ERROR reading {file_path}: {error}")
        return None


def get_chapters(data):
    return {
        chapter["chapter_id"]: chapter
        for chapter in data.get("chapters", [])
    }


def get_concepts(chapter):
    return {
        concept["concept_id"]: concept
        for concept in chapter.get("concepts", [])
    }


def compare_file(old_file, new_file, report):
    old_data = load_json(old_file)
    new_data = load_json(new_file)

    if old_data is None or new_data is None:
        return

    subject = new_data.get("subject", "Unknown")
    class_number = new_data.get("class", "Unknown")

    report.append("")
    report.append("=" * 60)
    report.append(f"CLASS {class_number} - {subject}")
    report.append("=" * 60)

    old_chapters = get_chapters(old_data)
    new_chapters = get_chapters(new_data)

    old_ids = set(old_chapters)
    new_ids = set(new_chapters)

    added_chapters = new_ids - old_ids
    removed_chapters = old_ids - new_ids
    common_chapters = old_ids & new_ids

    # -----------------------------
    # New chapters
    # -----------------------------

    for chapter_id in sorted(added_chapters):
        chapter_name = new_chapters[chapter_id].get(
            "chapter", "Unknown"
        )

        report.append(
            f"+ NEW CHAPTER: {chapter_name} "
            f"({chapter_id})"
        )

    # -----------------------------
    # Removed chapters
    # -----------------------------

    for chapter_id in sorted(removed_chapters):
        chapter_name = old_chapters[chapter_id].get(
            "chapter", "Unknown"
        )

        report.append(
            f"- REMOVED CHAPTER: {chapter_name} "
            f"({chapter_id})"
        )

    # -----------------------------
    # Existing chapters
    # -----------------------------

    for chapter_id in sorted(common_chapters):

        old_chapter = old_chapters[chapter_id]
        new_chapter = new_chapters[chapter_id]

        old_name = old_chapter.get("chapter", "")
        new_name = new_chapter.get("chapter", "")

        if old_name != new_name:
            report.append(
                f"<-> RENAMED CHAPTER: "
                f"{old_name} -> {new_name}"
            )

        old_concepts = get_concepts(old_chapter)
        new_concepts = get_concepts(new_chapter)

        old_concept_ids = set(old_concepts)
        new_concept_ids = set(new_concepts)

        added_concepts = new_concept_ids - old_concept_ids
        removed_concepts = old_concept_ids - new_concept_ids
        common_concepts = (
            old_concept_ids & new_concept_ids
        )

        for concept_id in sorted(added_concepts):
            name = new_concepts[concept_id].get(
                "concept", "Unknown"
            )

            report.append(
                f"  + NEW CONCEPT: {name} "
                f"({concept_id})"
            )

        for concept_id in sorted(removed_concepts):
            name = old_concepts[concept_id].get(
                "concept", "Unknown"
            )

            report.append(
                f"  - REMOVED CONCEPT: {name} "
                f"({concept_id})"
            )

        for concept_id in sorted(common_concepts):

            old_concept = old_concepts[concept_id]
            new_concept = new_concepts[concept_id]

            old_name = old_concept.get("concept", "")
            new_name = new_concept.get("concept", "")

            if old_name != new_name:
                report.append(
                    f"  <-> CHANGED CONCEPT: "
                    f"{old_name} -> {new_name}"
                )

            old_prerequisites = set(
                old_concept.get("prerequisites", [])
            )

            new_prerequisites = set(
                new_concept.get("prerequisites", [])
            )

            if old_prerequisites != new_prerequisites:
                report.append(
                    f"  <-> CHANGED PREREQUISITES: "
                    f"{concept_id}"
                )


def compare_versions(old_version, new_version):

    old_dir = CURRICULUM_DIR / old_version
    new_dir = CURRICULUM_DIR / new_version

    if not old_dir.exists():
        print(f"ERROR: {old_version} not found.")
        return

    if not new_dir.exists():
        print(f"ERROR: {new_version} not found.")
        return

    report = []

    report.append(
        "ADAPTIQ CURRICULUM CHANGE REPORT"
    )
    report.append("=" * 60)
    report.append(f"OLD VERSION: {old_version}")
    report.append(f"NEW VERSION: {new_version}")
    report.append(
        f"GENERATED: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    old_files = {
        (class_dir.name, file.name): file
        for class_dir in old_dir.glob("class_*")
        for file in class_dir.glob("*.json")
    }

    new_files = {
        (class_dir.name, file.name): file
        for class_dir in new_dir.glob("class_*")
        for file in class_dir.glob("*.json")
    }

    all_files = sorted(
        set(old_files) | set(new_files)
    )

    for key in all_files:

        old_file = old_files.get(key)
        new_file = new_files.get(key)

        class_name, file_name = key

        if old_file is None:
            report.append(
                f"\n+ NEW SUBJECT FILE: "
                f"{class_name}/{file_name}"
            )
            continue

        if new_file is None:
            report.append(
                f"\n- REMOVED SUBJECT FILE: "
                f"{class_name}/{file_name}"
            )
            continue

        compare_file(
            old_file,
            new_file,
            report
        )

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    report_file = (
        REPORT_DIR
        / f"curriculum_report_{new_version}.txt"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(report))

    print("\n==========================================")
    print("CURRICULUM COMPARISON COMPLETE")
    print("==========================================")

    print(f"\nReport saved to:")
    print(report_file)


def main():

    print("\n==========================================")
    print("    ADAPTIQ CURRICULUM CHANGE REPORT")
    print("==========================================")

    old_version = input(
        "\nEnter OLD version: "
    ).strip()

    new_version = input(
        "Enter NEW version: "
    ).strip()

    if not old_version or not new_version:
        print("ERROR: Version cannot be empty.")
        return

    if old_version == new_version:
        print("ERROR: Versions must be different.")
        return

    compare_versions(
        old_version,
        new_version
    )


if __name__ == "__main__":
    main()