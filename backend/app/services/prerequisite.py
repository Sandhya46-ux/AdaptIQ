from app.services.data_loader import (
    load_concepts
)


def get_concept(
    concept_id
):

    concepts = load_concepts()

    for concept in concepts:

        if concept["concept_id"] == concept_id:

            return concept

    return None


def get_prerequisites(
    concept_id
):

    concept = get_concept(
        concept_id
    )

    if not concept:
        return []

    return concept.get(
        "prerequisites",
        []
    )


def find_weak_prerequisites(
    concept_id,
    mastery_data,
    threshold=60
):

    prerequisites = get_prerequisites(
        concept_id
    )

    weak = []

    for prerequisite in prerequisites:

        mastery = mastery_data.get(
            prerequisite,
            0
        )

        if mastery < threshold:

            weak.append({
                "concept_id": prerequisite,
                "mastery": mastery
            })

    return weak