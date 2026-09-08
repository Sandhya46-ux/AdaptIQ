def build_tutor_context(
    learner,
    concept_id,
    concept_name
):

    concept_data = learner["concepts"].get(
        concept_id,
        {}
    )

    mastery = concept_data.get(
        "mastery",
        0
    )

    misconceptions = learner.get(
        "misconceptions",
        {}
    )

    return {
        "student_id": learner["student_id"],
        "concept": concept_name,
        "mastery": mastery,
        "misconceptions": misconceptions,
        "profile": learner["profile"]
    }