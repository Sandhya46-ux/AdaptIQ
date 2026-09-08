import json
import os
import re
import time
from pathlib import Path

from google import genai


# ==========================================
# CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONCEPTS_FILE = (
    BASE_DIR
    / "data"
    / "concepts"
    / "physics_concepts.json"
)

QUESTIONS_FILE = (
    BASE_DIR
    / "data"
    / "questions"
    / "physics_questions.json"
)

# Gemini models in fallback order
MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]


# ==========================================
# GEMINI CLIENT
# ==========================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GEMINI_API_KEY is not set.")
    print(
        "Please set your Gemini API key "
        "as a Windows environment variable."
    )
    exit(1)

client = genai.Client(api_key=API_KEY)


# ==========================================
# LOAD CONCEPTS
# ==========================================

def load_concepts():

    with open(
        CONCEPTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================================
# LOAD EXISTING QUESTIONS
# ==========================================

def load_questions():

    if not QUESTIONS_FILE.exists():
        return []

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================================
# GENERATE QUESTION ID
# ==========================================

def generate_id(
    class_num,
    chapter,
    existing_questions
):

    chapter_code = re.sub(
        r"[^A-Za-z]",
        "",
        chapter
    ).upper()[:4]

    existing_numbers = []

    for question in existing_questions:

        question_id = question.get(
            "id",
            ""
        )

        match = re.search(
            r"_(\d+)$",
            question_id
        )

        if match:

            existing_numbers.append(
                int(match.group(1))
            )

    next_number = (
        max(existing_numbers, default=0)
        + 1
    )

    return (
        f"PHY{class_num}_"
        f"{chapter_code}_"
        f"{next_number:03d}"
    )


# ==========================================
# CLEAN GEMINI RESPONSE
# ==========================================

def clean_json_response(text):

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

    # Remove ending ```
    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


# ==========================================
# VALIDATE GENERATED QUESTIONS
# ==========================================

def validate_generated_questions(
    questions
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

    # --------------------------------------
    # Check list
    # --------------------------------------

    if not isinstance(
        questions,
        list
    ):

        print(
            "❌ Generated data is not a list."
        )

        return False

    # --------------------------------------
    # Check every question
    # --------------------------------------

    for index, question in enumerate(
        questions,
        start=1
    ):

        # Make sure question is object
        if not isinstance(
            question,
            dict
        ):

            errors.append(
                f"Question {index}: "
                "must be a JSON object"
            )

            continue

        # ----------------------------------
        # Required fields
        # ----------------------------------

        for field in required_fields:

            if field not in question:

                errors.append(
                    f"Question {index}: "
                    f"missing '{field}'"
                )

        # If fields are missing, skip
        # deeper validation
        if any(
            field not in question
            for field in required_fields
        ):

            continue

        # ----------------------------------
        # Concept
        # ----------------------------------

        if not isinstance(
            question["concept"],
            str
        ):

            errors.append(
                f"Question {index}: "
                "concept must be text"
            )

        elif not question[
            "concept"
        ].strip():

            errors.append(
                f"Question {index}: "
                "concept is empty"
            )

        # ----------------------------------
        # Difficulty
        # ----------------------------------

        if question[
            "difficulty"
        ] not in valid_difficulties:

            errors.append(
                f"Question {index}: "
                "invalid difficulty"
            )

        # ----------------------------------
        # Question text
        # ----------------------------------

        if not isinstance(
            question["question"],
            str
        ):

            errors.append(
                f"Question {index}: "
                "question must be text"
            )

        elif not question[
            "question"
        ].strip():

            errors.append(
                f"Question {index}: "
                "question is empty"
            )

        # ----------------------------------
        # Options
        # ----------------------------------

        options = question["options"]

        if not isinstance(
            options,
            list
        ):

            errors.append(
                f"Question {index}: "
                "options must be a list"
            )

            continue

        if len(options) != 4:

            errors.append(
                f"Question {index}: "
                "must have exactly 4 options"
            )

        # Check empty options
        for option_number, option in enumerate(
            options,
            start=1
        ):

            if not isinstance(
                option,
                str
            ) or not option.strip():

                errors.append(
                    f"Question {index}: "
                    f"option {option_number} "
                    "is empty"
                )

        # Check duplicate options
        if len(options) == 4:

            normalized_options = [
                option.strip().lower()
                for option in options
            ]

            if len(
                set(normalized_options)
            ) != 4:

                errors.append(
                    f"Question {index}: "
                    "duplicate options found"
                )

        # ----------------------------------
        # Answer
        # ----------------------------------

        if question[
            "answer"
        ] not in options:

            errors.append(
                f"Question {index}: "
                "answer is not present "
                "in options"
            )

        # ----------------------------------
        # Explanation
        # ----------------------------------

        if not isinstance(
            question["explanation"],
            str
        ):

            errors.append(
                f"Question {index}: "
                "explanation must be text"
            )

        elif not question[
            "explanation"
        ].strip():

            errors.append(
                f"Question {index}: "
                "explanation is empty"
            )

        # ----------------------------------
        # Tags
        # ----------------------------------

        if not isinstance(
            question["tags"],
            list
        ):

            errors.append(
                f"Question {index}: "
                "tags must be a list"
            )

    # ======================================
    # RESULT
    # ======================================

    if errors:

        print(
            "\n❌ Generated data "
            "failed validation:"
        )

        for error in errors:

            print(
                f"   → {error}"
            )

        return False

    print(
        f"\n✓ Generated "
        f"{len(questions)} questions "
        "passed validation."
    )

    return True


# ==========================================
# GENERATE QUESTIONS USING GEMINI
# ==========================================

def generate_questions(
    class_num,
    chapter,
    concept,
    count
):

    prompt = f"""
You are an educational question generator
for the AdaptIQ project.

Generate exactly {count} multiple-choice
Physics questions.

Educational information:

Class: {class_num}
Subject: Physics
Chapter: {chapter}
Concept: {concept}

Requirements:

1. Questions must be appropriate for
   Class {class_num}.

2. Questions must specifically test:
   "{concept}".

3. Questions must be scientifically
   correct.

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

    # ======================================
    # TRY MODELS
    # ======================================

    for model in MODELS:

        print(
            f"\nTrying model: {model}"
        )

        # ==================================
        # RETRY MODEL
        # ==================================

        for attempt in range(1, 4):

            try:

                print(
                    f"Attempt {attempt}/3..."
                )

                # Current Gemini Interactions API
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
                        "❌ Empty response "
                        "from Gemini."
                    )

                    continue

                # Clean response
                text = clean_json_response(
                    text
                )

                # Convert JSON text
                generated = json.loads(
                    text
                )

                # Make sure list
                if not isinstance(
                    generated,
                    list
                ):

                    print(
                        "❌ Gemini response "
                        "is not a JSON list."
                    )

                    continue

                print(
                    f"✓ Successfully "
                    f"generated "
                    f"{len(generated)} "
                    "questions."
                )

                return generated

            # --------------------------------
            # Invalid JSON
            # --------------------------------

            except json.JSONDecodeError as error:

                print(
                    "❌ Gemini returned "
                    "invalid JSON."
                )

                print(error)

            # --------------------------------
            # API errors
            # --------------------------------

            except Exception as error:

                error_text = str(error)

                print(
                    f"⚠️ Generation failed:"
                )

                print(
                    error_text
                )

                # Temporary API problems
                temporary_error = (
                    "503" in error_text
                    or
                    "UNAVAILABLE"
                    in error_text
                    or
                    "429" in error_text
                    or
                    "RESOURCE_EXHAUSTED"
                    in error_text
                )

                if temporary_error:

                    if attempt < 3:

                        wait_time = (
                            attempt * 3
                        )

                        print(
                            f"Waiting "
                            f"{wait_time} "
                            "seconds..."
                        )

                        time.sleep(
                            wait_time
                        )

                else:

                    # Don't retry permanent
                    # configuration errors
                    break

        # Move to next model
        print(
            "⚠️ Moving to fallback model..."
        )

    # Nothing worked
    return []


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("""
============================
   ADAPTIQ QUESTION GENERATOR
============================
""")

    # ======================================
    # CLASS
    # ======================================

    try:

        class_num = int(
            input(
                "Enter class (9-12): "
            )
        )

    except ValueError:

        print(
            "❌ Class must be a number."
        )

        return

    if class_num not in [
        9,
        10,
        11,
        12
    ]:

        print(
            "❌ Invalid class."
        )

        return

    # ======================================
    # SUBJECT
    # ======================================

    subject = input(
        "Enter subject: "
    ).strip()

    if subject.lower() != "physics":

        print(
            "❌ Currently only Physics "
            "is supported."
        )

        return

    # ======================================
    # CHAPTER
    # ======================================

    chapter = input(
        "Enter chapter: "
    ).strip()

    if not chapter:

        print(
            "❌ Chapter cannot be empty."
        )

        return

    # ======================================
    # LOAD CONCEPTS
    # ======================================

    try:

        concepts = load_concepts()

    except Exception as error:

        print(
            f"❌ Could not load concepts:"
        )

        print(error)

        return

    # ======================================
    # FIND MATCHING CONCEPTS
    # ======================================

    matching_concepts = [
        concept
        for concept in concepts
        if (
            concept["class"] == class_num
            and
            concept["chapter"].lower()
            == chapter.lower()
        )
    ]

    if not matching_concepts:

        print(
            "\n❌ No concepts found "
            "for this class and chapter."
        )

        print(
            "\nCheck:"
        )

        print(
            "data/concepts/"
            "physics_concepts.json"
        )

        return

    # ======================================
    # DISPLAY CONCEPTS
    # ======================================

    print(
        "\nAvailable concepts:"
    )

    for index, concept in enumerate(
        matching_concepts,
        start=1
    ):

        print(
            f"{index}. "
            f"{concept['concept']}"
        )

    # ======================================
    # SELECT CONCEPT
    # ======================================

    try:

        choice = int(
            input(
                "\nChoose concept: "
            )
        )

    except ValueError:

        print(
            "❌ Invalid concept choice."
        )

        return

    if (
        choice < 1
        or
        choice > len(matching_concepts)
    ):

        print(
            "❌ Invalid concept choice."
        )

        return

    selected_concept = (
        matching_concepts[
            choice - 1
        ]["concept"]
    )

    # ======================================
    # QUESTION COUNT
    # ======================================

    try:

        count = int(
            input(
                "Number of questions: "
            )
        )

    except ValueError:

        print(
            "❌ Number of questions "
            "must be a number."
        )

        return

    if count < 1 or count > 20:

        print(
            "❌ Enter between "
            "1 and 20 questions."
        )

        return

    # ======================================
    # GENERATE
    # ======================================

    print(
        "\n============================"
    )

    print(
        "GENERATING QUESTIONS"
    )

    print(
        "============================"
    )

    print(
        f"Class: {class_num}"
    )

    print(
        f"Chapter: {chapter}"
    )

    print(
        f"Concept: {selected_concept}"
    )

    print(
        f"Number: {count}"
    )

    generated = generate_questions(
        class_num,
        chapter,
        selected_concept,
        count
    )

    # ======================================
    # GENERATION FAILED
    # ======================================

    if not generated:

        print(
            """
❌ No questions generated.

Possible causes:
- Gemini temporary overload
- API quota/rate limit
- Network issue
- Invalid API key
- Model temporarily unavailable
"""
        )

        return

    # ======================================
    # VALIDATE BEFORE SAVING
    # ======================================

    print(
        "\nValidating generated questions..."
    )

    if not validate_generated_questions(
        generated
    ):

        print(
            "\n❌ Questions were NOT saved."
        )

        return

    # ======================================
    # LOAD EXISTING QUESTIONS
    # ======================================

    try:

        existing_questions = (
            load_questions()
        )

    except Exception as error:

        print(
            "❌ Could not load existing "
            "question data."
        )

        print(error)

        return

    # ======================================
    # ADD IDs AND METADATA
    # ======================================

    for question in generated:

        question["id"] = generate_id(
            class_num,
            chapter,
            existing_questions
        )

        question["class"] = (
            class_num
        )

        question["subject"] = (
            "Physics"
        )

        question["chapter"] = (
            chapter
        )

        existing_questions.append(
            question
        )

    # ======================================
    # SAVE
    # ======================================

    try:

        with open(
            QUESTIONS_FILE,
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
            "❌ Failed to save questions."
        )

        print(error)

        return

    # ======================================
    # SUCCESS
    # ======================================

    print(
        "\n============================"
    )

    print(
        "GENERATION COMPLETE ✓"
    )

    print(
        "============================"
    )

    print(
        f"\nGenerated: "
        f"{len(generated)} questions"
    )

    print(
        f"Concept: "
        f"{selected_concept}"
    )

    print(
        f"Saved to:"
    )

    print(
        QUESTIONS_FILE
    )


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()