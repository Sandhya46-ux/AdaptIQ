from app.services.data_loader import (
    load_concepts
)

from app.services.prerequisite import (
    find_weak_prerequisites
)


def get_priority(
    mastery
):

    if mastery < 40:
        return "Critical"

    if mastery < 60:
        return "High"

    if mastery < 80:
        return "Medium"

    return "Low"


def generate_recommendations(
    mastery_data
):

    concepts = load_concepts()

    recommendations = []

    for concept in concepts:

        concept_id = concept[
            "concept_id"
        ]

        concept_name = concept[
            "concept"
        ]

        mastery = mastery_data.get(
            concept_id,
            0
        )

        priority = get_priority(
            mastery
        )

        weak_prerequisites = (
            find_weak_prerequisites(
                concept_id,
                mastery_data
            )
        )

        if mastery < 40:

            reason = (
                "Concept requires immediate "
                "attention."
            )

        elif weak_prerequisites:

            reason = (
                "A prerequisite concept "
                "needs improvement."
            )

        elif mastery < 80:

            reason = (
                "Additional practice "
                "is recommended."
            )

        else:

            reason = (
                "Concept is well mastered."
            )

        recommendations.append({

            "concept_id": concept_id,

            "concept": concept_name,

            "mastery": mastery,

            "priority": priority,

            "reason": reason,

            "weak_prerequisites":
                weak_prerequisites
        })

    recommendations.sort(
        key=lambda item: (
            item["mastery"]
        )
    )

    return recommendations