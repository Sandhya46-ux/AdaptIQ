from app.services.data_loader import (
    load_misconceptions
)


def get_misconception(
    misconception_id
):

    misconceptions = load_misconceptions()

    for item in misconceptions:

        if (
            item["misconception_id"]
            == misconception_id
        ):

            return item

    return None


def get_concept_misconceptions(
    concept_id
):

    misconceptions = load_misconceptions()

    return [
        item
        for item in misconceptions
        if item["concept_id"] == concept_id
    ]


def detect_from_attempt(
    attempt
):

    misconception_id = attempt.get(
        "misconception_id"
    )

    if not misconception_id:

        return None

    return get_misconception(
        misconception_id
    )