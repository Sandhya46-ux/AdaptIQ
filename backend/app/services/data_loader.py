import json
from pathlib import Path


# AdaptIQ project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]


CONCEPTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "concepts"
    / "math_concepts.json"
)

QUESTIONS_FILE = (
    PROJECT_ROOT
    / "data"
    / "questions"
    / "math_questions.json"
)

MISCONCEPTIONS_FILE = (
    PROJECT_ROOT
    / "data"
    / "misconceptions"
    / "common_misconceptions.json"
)

ATTEMPTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "attempts"
    / "student_attempts.json"
)


def load_json(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def load_concepts():

    return load_json(CONCEPTS_FILE)


def load_questions():

    return load_json(QUESTIONS_FILE)


def load_misconceptions():

    return load_json(MISCONCEPTIONS_FILE)


def load_attempts():

    return load_json(ATTEMPTS_FILE)