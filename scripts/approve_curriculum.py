import json
import shutil
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CURRICULUM_DIR = BASE_DIR / "data" / "curriculum"
DRAFT_DIR = CURRICULUM_DIR / "drafts"
HISTORY_FILE = CURRICULUM_DIR / "update_history.json"


SUBJECT_FILES = {
    "mathematics": "mathematics.json",
    "physics": "physics.json",
    "chemistry": "chemistry.json",
    "biology": "biology.json"
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        return load_json(HISTORY_FILE)
    except Exception:
        return []


def main():

    print("=" * 50)
    print("       ADAPTIQ CURRICULUM APPROVAL")
    print("=" * 50)

    if len(sys.argv) != 2:
        print()
        print("Usage:")
        print("python scripts\\approve_curriculum.py <draft_file>")
        print()
        print("Example:")
        print(
            "python scripts\\approve_curriculum.py "
            "data\\curriculum\\drafts\\class_12_physics_2027-28.json"
        )
        return 1

    draft_path = Path(sys.argv[1])

    if not draft_path.is_absolute():
        draft_path = BASE_DIR / draft_path

    if not draft_path.exists():
        print()
        print(f"ERROR: Draft file not found:")
        print(draft_path)
        return 1

    # -------------------------------------------------
    # Load draft
    # -------------------------------------------------

    try:
        draft = load_json(draft_path)
    except Exception as e:
        print()
        print(f"ERROR: Invalid JSON: {e}")
        return 1

    required_fields = [
        "curriculum_version",
        "board",
        "class",
        "subject",
        "source",
        "chapters"
    ]

    missing = [
        field for field in required_fields
        if field not in draft
    ]

    if missing:
        print()
        print("ERROR: Draft is missing required fields:")
        for field in missing:
            print(f"  - {field}")
        return 1

    version = str(draft["curriculum_version"])
    class_number = draft["class"]
    subject = str(draft["subject"]).strip()

    subject_key = subject.lower()

    if subject_key not in SUBJECT_FILES:
        print()
        print(f"ERROR: Unsupported subject: {subject}")
        print("Supported subjects:")
        print("  Mathematics")
        print("  Physics")
        print("  Chemistry")
        print("  Biology")
        return 1

    if class_number not in [9, 10, 11, 12]:
        print()
        print(f"ERROR: Invalid class: {class_number}")
        return 1

    # -------------------------------------------------
    # Display draft summary
    # -------------------------------------------------

    chapters = draft.get("chapters", [])

    concept_count = 0

    for chapter in chapters:
        concept_count += len(
            chapter.get("concepts", [])
        )

    print()
    print("DRAFT INFORMATION")
    print("-" * 50)
    print(f"Version  : {version}")
    print(f"Class    : {class_number}")
    print(f"Subject  : {subject}")
    print(f"Chapters : {len(chapters)}")
    print(f"Concepts : {concept_count}")
    print()

    # -------------------------------------------------
    # Check destination
    # -------------------------------------------------

    destination = (
        CURRICULUM_DIR
        / version
        / f"class_{class_number}"
        / SUBJECT_FILES[subject_key]
    )

    print("TARGET FILE")
    print("-" * 50)
    print(destination)
    print()

    if destination.exists():
        print("ERROR: Target curriculum file already exists.")
        print()
        print("The approval script will NOT overwrite an existing")
        print("active curriculum file.")
        print()
        print("Create a new version or manually handle the existing")
        print("file if replacement is required.")
        return 1

    # -------------------------------------------------
    # Ask for approval
    # -------------------------------------------------

    print("=" * 50)
    print("IMPORTANT")
    print("=" * 50)
    print()
    print("This will promote the draft to ACTIVE curriculum.")
    print()
    print("The old curriculum versions will NOT be modified.")
    print()

    approval = input(
        "Type APPROVE to continue: "
    ).strip()

    if approval != "APPROVE":
        print()
        print("Approval cancelled.")
        return 0

    # -------------------------------------------------
    # Promote draft
    # -------------------------------------------------

    try:
        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            draft_path,
            destination
        )

    except Exception as e:
        print()
        print(f"ERROR: Could not promote draft: {e}")
        return 1

    # -------------------------------------------------
    # Update history
    # -------------------------------------------------

    history = load_history()

    history.append({
        "curriculum_version": version,
        "class": class_number,
        "subject": subject,
        "source_draft": str(
            draft_path.relative_to(BASE_DIR)
        ),
        "active_file": str(
            destination.relative_to(BASE_DIR)
        ),
        "status": "approved"
    })

    save_json(HISTORY_FILE, history)

    print()
    print("=" * 50)
    print("CURRICULUM APPROVED SUCCESSFULLY")
    print("=" * 50)
    print()
    print("Active curriculum:")
    print(destination)
    print()
    print("Approval history:")
    print(HISTORY_FILE)
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())