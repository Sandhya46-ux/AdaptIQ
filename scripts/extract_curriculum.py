import json
import os
import sys
from pathlib import Path

from google import genai


# ---------------------------------------
# Configuration
# ---------------------------------------

MODEL = "gemini-3.8-flash"

OUTPUT_DIR = Path("data/curriculum/drafts")


# ---------------------------------------
# Gemini client
# ---------------------------------------

def create_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("ERROR: GEMINI_API_KEY is not set.")
        print(
            "Set the environment variable before "
            "running this script."
        )
        return None

    return genai.Client(api_key=api_key)


# ---------------------------------------
# Prompt
# ---------------------------------------

def build_prompt(
    curriculum_text,
    class_number,
    subject,
    version
):

    return f"""
You are a curriculum data extraction assistant
for the AdaptIQ educational platform.

Convert the supplied official curriculum text into
the required AdaptIQ JSON structure.

Target:

Class: {class_number}
Subject: {subject}
Curriculum version: {version}
Board: CBSE

IMPORTANT RULES:

1. Use ONLY information present in the supplied text.
2. Do NOT invent chapters.
3. Do NOT invent concepts.
4. Do NOT add topics that are not supported by the source.
5. Preserve the wording of chapter names where possible.
6. Create stable concept IDs using this format:

   SUBJECT + CLASS + short concept name

   Example:
   PHY12_ELECTRIC_FIELD

7. If prerequisites are not explicitly stated,
   use an empty list.
8. If learning outcomes are not explicitly stated,
   use an empty list.
9. Return ONLY valid JSON.
10. Do not use Markdown.
11. Do not include explanations outside the JSON.

Required structure:

{{
  "curriculum_version": "{version}",
  "board": "CBSE",
  "class": {class_number},
  "subject": "{subject}",
  "source": {{
    "type": "official_document",
    "reference": "Provided curriculum document"
  }},
  "chapters": [
    {{
      "chapter_id": "SUBJECTCLASS_CH01",
      "chapter": "Chapter Name",
      "concepts": [
        {{
          "concept_id": "SUBJECTCLASS_CONCEPT",
          "concept": "Concept Name",
          "prerequisites": [],
          "learning_outcomes": []
        }}
      ]
    }}
  ]
}}

SOURCE TEXT:

{curriculum_text}
"""


# ---------------------------------------
# Gemini call
# ---------------------------------------

def generate_curriculum(
    client,
    curriculum_text,
    class_number,
    subject,
    version
):

    prompt = build_prompt(
        curriculum_text,
        class_number,
        subject,
        version
    )

    print("\nSending curriculum to Gemini...")

    try:

        response = client.interactions.create(
            model=MODEL,
            input=prompt
        )

        return response

    except Exception as error:

        print("\nERROR while calling Gemini:")
        print(error)

        return None


# ---------------------------------------
# Extract JSON
# ---------------------------------------

def extract_json(response_text):

    text = response_text.strip()

    # Remove accidental Markdown fences
    if text.startswith("```"):
        lines = text.splitlines()

        if lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError as error:

        print("\nERROR: Gemini did not return valid JSON.")
        print(error)

        return None


# ---------------------------------------
# Save draft
# ---------------------------------------

def save_draft(data, class_number, subject, version):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    subject_file = subject.lower()

    output_file = (
        OUTPUT_DIR
        / f"class_{class_number}_{subject_file}_{version}.json"
    )

    with open(
        output_file,
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

    print("\nDraft curriculum saved:")
    print(output_file)

    return output_file


# ---------------------------------------
# Main
# ---------------------------------------

def main():

    print("\n==========================================")
    print("    ADAPTIQ AI CURRICULUM EXTRACTOR")
    print("==========================================")

    # -----------------------------------
    # Arguments
    # -----------------------------------

    if len(sys.argv) != 5:

        print(
            "\nUsage:"
        )

        print(
            "python scripts\\extract_curriculum.py "
            "<file.txt> <class> <subject> <version>"
        )

        print(
            "\nExample:"
        )

        print(
            "python scripts\\extract_curriculum.py "
            "physics_2027.txt 12 Physics 2027-28"
        )

        return 1

    input_file = Path(sys.argv[1])
    class_number = int(sys.argv[2])
    subject = sys.argv[3]
    version = sys.argv[4]

    # -----------------------------------
    # Validate input
    # -----------------------------------

    if not input_file.exists():

        print(
            f"\nERROR: File not found:"
            f"\n{input_file}"
        )

        return 1

    # -----------------------------------
    # Read curriculum
    # -----------------------------------

    try:

        curriculum_text = input_file.read_text(
            encoding="utf-8"
        )

    except Exception as error:

        print(
            f"\nERROR reading input file: {error}"
        )

        return 1

    if not curriculum_text.strip():

        print("\nERROR: Input file is empty.")
        return 1

    # -----------------------------------
    # Gemini
    # -----------------------------------

    client = create_client()

    if client is None:
        return 1

    response = generate_curriculum(
        client,
        curriculum_text,
        class_number,
        subject,
        version
    )

    if response is None:
        return 1

    # -----------------------------------
    # Get response text
    # -----------------------------------

    response_text = getattr(
        response,
        "output_text",
        None
    )

    if not response_text:

        response_text = str(response)

    # -----------------------------------
    # Parse JSON
    # -----------------------------------

    data = extract_json(response_text)

    if data is None:
        return 1

    # -----------------------------------
    # Save draft
    # -----------------------------------

    save_draft(
        data,
        class_number,
        subject,
        version
    )

    print("\n==========================================")
    print("CURRICULUM EXTRACTION COMPLETE")
    print("==========================================")

    print(
        "\nIMPORTANT:"
        "\nThis is a DRAFT."
        "\nValidate and review it before using it."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())