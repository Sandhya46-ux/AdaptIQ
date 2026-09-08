import json
import shutil
from pathlib import Path


BASE_DIR = Path("data/curriculum")
CONFIG_FILE = Path("scripts/curriculum_source_config.json")


def load_config():
    """Load curriculum update configuration."""

    if not CONFIG_FILE.exists():
        print("ERROR: Configuration file not found.")
        print(f"Expected: {CONFIG_FILE}")
        return None

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        print("ERROR: Invalid configuration JSON.")
        print(error)
        return None


def create_version_folder(version):
    """Create folders for a new curriculum version."""

    version_dir = BASE_DIR / version

    if version_dir.exists():
        print(f"\nVersion already exists: {version}")
        return version_dir

    version_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for class_number in [9, 10, 11, 12]:
        class_dir = version_dir / f"class_{class_number}"
        class_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    print(f"\nCreated curriculum version: {version}")

    return version_dir


def copy_current_curriculum(old_version, new_version):
    """
    Create a safe working copy of the current curriculum.

    The old version is never modified.
    """

    old_dir = BASE_DIR / old_version
    new_dir = BASE_DIR / new_version

    if not old_dir.exists():
        print(
            f"\nERROR: Current version '{old_version}' "
            "does not exist."
        )
        return False

    if new_dir.exists():
        print(
            f"\nERROR: '{new_version}' already exists."
        )
        print(
            "Delete it first if this is only a test."
        )
        return False

    shutil.copytree(old_dir, new_dir)

    print(
        f"\nCreated working copy:"
        f"\n  {old_version} → {new_version}"
    )

    return True


def update_version_metadata(version_dir, new_version):
    """Update curriculum_version inside JSON files."""

    json_files = list(
        version_dir.glob("class_*/*.json")
    )

    updated = 0

    for file_path in json_files:

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            data["curriculum_version"] = new_version

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

                file.write("\n")

            updated += 1

        except Exception as error:

            print(
                f"ERROR updating {file_path}: {error}"
            )

    print(
        f"\nUpdated version metadata in "
        f"{updated} files."
    )


def main():

    print("\n==============================================")
    print("     ADAPTIQ CURRICULUM UPDATE PREPARER")
    print("==============================================")

    config = load_config()

    if config is None:
        return 1

    old_version = config.get("current_version")
    new_version = config.get("next_version")

    if not old_version or not new_version:

        print(
            "\nERROR: current_version or "
            "next_version is missing."
        )

        return 1

    print(f"\nCurrent version : {old_version}")
    print(f"New version     : {new_version}")

    # -----------------------------------------
    # Create new version from current version
    # -----------------------------------------

    success = copy_current_curriculum(
        old_version,
        new_version
    )

    if not success:
        return 1

    new_dir = BASE_DIR / new_version

    # -----------------------------------------
    # Update version metadata
    # -----------------------------------------

    update_version_metadata(
        new_dir,
        new_version
    )

    print("\n==============================================")
    print("CURRICULUM UPDATE PREPARATION COMPLETE")
    print("==============================================")

    print(
        f"\nNew working curriculum:"
        f"\n{new_dir}"
    )

    print(
        "\nYou can now replace/update the JSON files "
        "inside this folder with the new official "
        "curriculum."
    )

    print(
        "\nIMPORTANT:"
        "\nThe original curriculum remains unchanged."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())