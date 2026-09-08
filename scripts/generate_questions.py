import json
import os
import re
import time
from pathlib import Path

from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = (
    BASE_DIR
    / "scripts"
    / "curriculum_source_config.json"
)

CURRICULUM_DIR = (
    BASE_DIR
    / "data"
    / "curriculum"
)

QUESTIONS_DIR = (
    BASE_DIR
    / "data"
    / "questions"
)

# Gemini models in fallback order
MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]

SUBJECT_FILES = {
    "Mathematics": "math_questions.json",
    "Physics": "physics_questions.json",
    "Chemistry": "chemistry_questions.json",
    "Biology": "biology_questions.json"
}


# ============================================================
# GEMINI CLIENT
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print(
        "ERROR: GEMINI_API_KEY environment variable "
        "is not set."
    )
    raise SystemExit(1)

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# LOAD CONFIGURATION
# ============================================================

def load_config():

    if not CONFIG_FILE.exists():

        print(
            f"ERROR: Configuration file not found:\n"
            f"{CONFIG_FILE}"
        )

        raise SystemExit(1)

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print(
            f"ERROR: Could not load configuration: "
            f"{error}"
        )

        raise SystemExit(1)


# ============================================================
# LOAD CURRICULUM
# ============================================================

def load_curriculum(
    version,
    class_num,
    subject
):

    subject_file = subject.lower() + ".json"

    curriculum_file = (
        CURRICULUM_DIR
        / version
        / f"class_{class_num}"
        / subject_file
    )

    # Mathematics filename is different
    if subject == "Mathematics":

        curriculum_file = (
            CURRICULUM_DIR
            / version
            / f"class_{class_num}"
            / "mathematics.json"
        )

    if not curriculum_file.exists():

        print()
        print(
            "ERROR: Curriculum file not found:"
        )

        print(curriculum_file)

        raise SystemExit(1)

    try:

        with open(
            curriculum_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except Exception as error:

        print(
            f"ERROR: Could not read curriculum: "
            f"{error}"
        )

        raise SystemExit(1)

    return data


# ============================================================
# GET CHAPTERS
# ============================================================

def get_chapters(
    curriculum
):

    return curriculum.get(
        "chapters",
        []
    )


# ============================================================
# GET CONCEPTS
# ============================================================

def get_concepts(
    chapter
):

    return chapter.get(
        "concepts",
        []
    )


# ============================================================
# CLEAN GEMINI JSON
# ============================================================

def clean_json_response(
    text
):

    if not text:
        return ""

    text = text.strip()

    # Remove ```json
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove ```
    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


# ============================================================
# VALIDATE GENERATED QUESTIONS
# ============================================================

def validate_generated_questions(
    questions,
    expected_concept
):

    errors = []

    valid_difficulties = [
        "easy",
        "medium",
        "hard"
    ]

    required_fields = [
        "concept",
        "difficulty",
        "question",
        "options",
        "answer",
        "explanation",
        "tags"
    ]

    # --------------------------------------------------------
    # Check list
    # --------------------------------------------------------

    if not isinstance(
        questions,
        list
    ):

        return [
            "Generated response is not a list."
        ]

    if len(questions) == 0:

        return [
            "No questions were generated."
        ]

    # --------------------------------------------------------
    # Validate each question
    # --------------------------------------------------------

    seen_questions = set()

    for index, question in enumerate(
        questions,
        start=1
    ):

        if not isinstance(
            question,
            dict
        ):

            errors.append(
                f"Question {index} is not an object."
            )

            continue

        # ----------------------------------------------------
        # Required fields
        # ----------------------------------------------------

        for field in required_fields:

            if field not in question:

                errors.append(
                    f"Question {index}: "
                    f"missing '{field}'."
                )

        if any(
            field not in question
            for field in required_fields
        ):
            continue

        # ----------------------------------------------------
        # Concept
        # ----------------------------------------------------

        if question["concept"] != expected_concept:

            errors.append(
                f"Question {index}: concept "
                f"'{question['concept']}' does not match "
                f"'{expected_concept}'."
            )

        # ----------------------------------------------------
        # Difficulty
        # ----------------------------------------------------

        if question["difficulty"] not in valid_difficulties:

            errors.append(
                f"Question {index}: invalid difficulty "
                f"'{question['difficulty']}'."
            )

        # ----------------------------------------------------
        # Question text
        # ----------------------------------------------------

        question_text = str(
            question["question"]
        ).strip()

        if not question_text:

            errors.append(
                f"Question {index}: question is empty."
            )

        normalized = question_text.lower()

        if normalized in seen_questions:

            errors.append(
                f"Question {index}: duplicate question."
            )

        seen_questions.add(
            normalized
        )

        # ----------------------------------------------------
        # Options
        # ----------------------------------------------------

        options = question["options"]

        if not isinstance(
            options,
            list
        ):

            errors.append(
                f"Question {index}: options must be a list."
            )

            continue

        if len(options) != 4:

            errors.append(
                f"Question {index}: expected exactly "
                f"4 options, got {len(options)}."
            )

        # ----------------------------------------------------
        # Duplicate options
        # ----------------------------------------------------

        normalized_options = [
            str(option).strip().lower()
            for option in options
        ]

        if len(normalized_options) != len(
            set(normalized_options)
        ):

            errors.append(
                f"Question {index}: duplicate options."
            )

        # ----------------------------------------------------
        # Answer
        # ----------------------------------------------------

        if question["answer"] not in options:

            errors.append(
                f"Question {index}: answer "
                f"'{question['answer']}' is not one "
                f"of the options."
            )

        # ----------------------------------------------------
        # Explanation
        # ----------------------------------------------------

        if not str(
            question["explanation"]
        ).strip():

            errors.append(
                f"Question {index}: explanation is empty."
            )

        # ----------------------------------------------------
        # Tags
        # ----------------------------------------------------

        if not isinstance(
            question["tags"],
            list
        ):

            errors.append(
                f"Question {index}: tags must be a list."
            )

    return errors


# ============================================================
# LOAD EXISTING QUESTIONS
# ============================================================

def load_existing_questions(
    questions_file
):

    if not questions_file.exists():

        return []

    try:

        with open(
            questions_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(
            data,
            list
        ):

            return data

        return []

    except Exception as error:

        print(
            f"WARNING: Could not read existing "
            f"questions: {error}"
        )

        return []


# ============================================================
# GENERATE QUESTIONS USING GEMINI
# ============================================================

def generate_questions(
    class_num,
    subject,
    chapter,
    concept,
    concept_id,
    count
):

    prompt = f"""
You are an educational question generator
for the AdaptIQ project.

Generate exactly {count} multiple-choice
questions.

Educational information:

Class: {class_num}
Subject: {subject}
Chapter: {chapter}
Concept: {concept}
Concept ID: {concept_id}

Requirements:

1. Questions must be appropriate for
   Class {class_num}.

2. Questions must specifically test:
   "{concept}".

3. Questions must be scientifically/
   mathematically correct according to
   the subject.

4. Include conceptual and numerical
   questions where appropriate.

5. Each question must have exactly
   4 options.

6. There must be exactly one correct
   answer.

7. The answer must EXACTLY match one
   of the four options.

8. Difficulty must be one of:
   easy
   medium
   hard

9. Do not repeat questions.

10. Provide a short explanation.

11. Add useful tags.

12. Return ONLY valid JSON.

13. Do NOT use markdown.

14. Do NOT write anything before or
    after the JSON.

Return exactly this structure:

[
  {{
    "concept": "{concept}",
    "difficulty": "easy",
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option",
    "explanation": "Short explanation",
    "tags": [
      "{concept}"
    ]
  }}
]
"""

    for model in MODELS:

        print(
            f"\nTrying model: {model}"
        )

        for attempt in range(1, 4):

            try:

                print(
                    f"Attempt {attempt}/3..."
                )

                interaction = (
                    client.interactions.create(
                        model=model,
                        input=prompt
                    )
                )

                text = (
                    interaction.output_text
                )

                if not text:

                    print(
                        "No output received."
                    )

                    continue

                text = clean_json_response(
                    text
                )

                questions = json.loads(
                    text
                )

                errors = (
                    validate_generated_questions(
                        questions,
                        concept
                    )
                )

                if errors:

                    print(
                        "\nGenerated questions "
                        "failed validation:"
                    )

                    for error in errors:

                        print(
                            f"   -> {error}"
                        )

                    continue

                print(
                    f"\nGenerated "
                    f"{len(questions)} questions "
                    "passed validation."
                )

                return questions

            except json.JSONDecodeError as error:

                print(
                    f"Invalid JSON returned by "
                    f"{model}: {error}"
                )

            except Exception as error:

                error_text = str(
                    error
                )

                print(
                    f"Error: {error_text}"
                )

                if (
                    "503" in error_text
                    or "429" in error_text
                    or "unavailable" in error_text.lower()
                    or "overloaded" in error_text.lower()
                ):

                    wait_time = 2 * attempt

                    print(
                        f"Temporary error. "
                        f"Waiting {wait_time} seconds..."
                    )

                    time.sleep(
                        wait_time
                    )

                else:

                    break

    print(
        "\nERROR: All Gemini models failed."
    )

    return None


# ============================================================
# SAVE QUESTIONS
# ============================================================

def save_questions(
    questions,
    class_num,
    subject,
    chapter,
    concept,
    concept_id,
    version
):

    QUESTIONS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = SUBJECT_FILES.get(
        subject
    )

    if not filename:

        print(
            f"ERROR: Unsupported subject: {subject}"
        )

        return False

    questions_file = (
        QUESTIONS_DIR / filename
    )

    existing_questions = (
        load_existing_questions(
            questions_file
        )
    )

    # --------------------------------------------------------
    # Existing IDs
    # --------------------------------------------------------

    existing_ids = {
        item.get("id")
        for item in existing_questions
        if isinstance(item, dict)
    }

    # --------------------------------------------------------
    # Generate ID prefix
    # --------------------------------------------------------

    subject_prefix = {
        "Mathematics": "MATH",
        "Physics": "PHY",
        "Chemistry": "CHEM",
        "Biology": "BIO"
    }[subject]

    chapter_code = re.sub(
        r"[^A-Z0-9]+",
        "_",
        chapter.upper()
    ).strip("_")

    # Shorten chapter code if needed
    chapter_code = chapter_code[:20]

    # --------------------------------------------------------
    # Add generated questions
    # --------------------------------------------------------

    added = []

    for question in questions:

        number = 1

        while True:

            question_id = (
                f"{subject_prefix}"
                f"{class_num}_"
                f"{chapter_code}_"
                f"{number:03d}"
            )

            if question_id not in existing_ids:

                break

            number += 1

        question_record = {
            "id": question_id,
            "class": class_num,
            "subject": subject,
            "chapter": chapter,
            "concept": concept,
            "concept_id": concept_id,
            "difficulty": question[
                "difficulty"
            ],
            "question": question[
                "question"
            ],
            "options": question[
                "options"
            ],
            "answer": question[
                "answer"
            ],
            "explanation": question[
                "explanation"
            ],
            "tags": question[
                "tags"
            ],
            "source": {
                "type": "curriculum",
                "curriculum_version": version,
                "concept_id": concept_id
            },
            "generated_by": "Gemini",
            "review_status": "pending"
        }

        existing_questions.append(
            question_record
        )

        existing_ids.add(
            question_id
        )

        added.append(
            question_record
        )

    try:

        with open(
            questions_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                existing_questions,
                file,
                indent=2,
                ensure_ascii=False
            )

    except Exception as error:

        print(
            f"ERROR: Could not save questions: "
            f"{error}"
        )

        return False

    print()
    print(
        f"Saved {len(added)} questions to:"
    )

    print(
        questions_file
    )

    return True


# ============================================================
# DISPLAY MENU
# ============================================================

def select_from_list(
    items,
    label
):

    print()
    print(label)
    print("-" * 40)

    for index, item in enumerate(
        items,
        start=1
    ):

        print(
            f"{index}. {item}"
        )

    while True:

        try:

            choice = int(
                input(
                    "\nEnter number: "
                )
            )

            if 1 <= choice <= len(items):

                return items[
                    choice - 1
                ]

            print(
                "Please select a valid number."
            )

        except ValueError:

            print(
                "Please enter a number."
            )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 50)
    print(
        "       ADAPTIQ QUESTION GENERATOR"
    )
    print("=" * 50)

    config = load_config()

    version = config.get(
        "current_version",
        "2026-27"
    )

    subjects = config.get(
        "subjects",
        list(SUBJECT_FILES.keys())
    )

    print()
    print(
        f"CURRICULUM VERSION: {version}"
    )

    # --------------------------------------------------------
    # Class
    # --------------------------------------------------------

    class_num = select_from_list(
        [9, 10, 11, 12],
        "SELECT CLASS"
    )

    # --------------------------------------------------------
    # Subject
    # --------------------------------------------------------

    available_subjects = [
        subject
        for subject in subjects
        if subject in SUBJECT_FILES
    ]

    subject = select_from_list(
        available_subjects,
        "SELECT SUBJECT"
    )

    # --------------------------------------------------------
    # Load curriculum
    # --------------------------------------------------------

    curriculum = load_curriculum(
        version,
        class_num,
        subject
    )

    chapters = get_chapters(
        curriculum
    )

    if not chapters:

        print(
            "ERROR: No chapters found "
            "in curriculum."
        )

        return 1

    # --------------------------------------------------------
    # Chapter
    # --------------------------------------------------------

    chapter_names = [
        chapter.get(
            "chapter"
        )
        for chapter in chapters
    ]

    chapter_name = select_from_list(
        chapter_names,
        "SELECT CHAPTER"
    )

    selected_chapter = next(
        chapter
        for chapter in chapters
        if chapter.get("chapter")
        == chapter_name
    )

    # --------------------------------------------------------
    # Concept
    # --------------------------------------------------------

    concepts = get_concepts(
        selected_chapter
    )

    if not concepts:

        print(
            "ERROR: No concepts found "
            "for this chapter."
        )

        return 1

    concept_names = [
        concept.get(
            "concept"
        )
        for concept in concepts
    ]

    concept_name = select_from_list(
        concept_names,
        "SELECT CONCEPT"
    )

    selected_concept = next(
        concept
        for concept in concepts
        if concept.get("concept")
        == concept_name
    )

    concept_id = selected_concept.get(
        "concept_id",
        ""
    )

    # --------------------------------------------------------
    # Number of questions
    # --------------------------------------------------------

    while True:

        try:

            count = int(
                input(
                    "\nNumber of questions: "
                )
            )

            if count > 0:

                break

            print(
                "Enter a number greater than 0."
            )

        except ValueError:

            print(
                "Please enter a valid number."
            )

    # --------------------------------------------------------
    # Display selection
    # --------------------------------------------------------

    print()
    print("=" * 50)
    print("GENERATION SETTINGS")
    print("=" * 50)

    print(
        f"Curriculum : {version}"
    )

    print(
        f"Class      : {class_num}"
    )

    print(
        f"Subject    : {subject}"
    )

    print(
        f"Chapter    : {chapter_name}"
    )

    print(
        f"Concept    : {concept_name}"
    )

    print(
        f"Concept ID : {concept_id}"
    )

    print(
        f"Questions  : {count}"
    )

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    questions = generate_questions(
        class_num,
        subject,
        chapter_name,
        concept_name,
        concept_id,
        count
    )

    if questions is None:

        return 1

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    success = save_questions(
        questions,
        class_num,
        subject,
        chapter_name,
        concept_name,
        concept_id,
        version
    )

    if not success:

        return 1

    print()
    print("=" * 50)
    print(
        "QUESTION GENERATION COMPLETE"
    )
    print("=" * 50)

    return 0


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    raise SystemExit(
        main()
    )