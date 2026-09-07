def calculate_mastery(
    correct,
    total
):

    if total == 0:
        return 0.0

    return round(
        (correct / total) * 100,
        2
    )


def update_mastery(
    previous_mastery,
    quiz_percentage
):

    updated = (
        previous_mastery * 0.8
        + quiz_percentage * 0.2
    )

    return round(
        min(updated, 100),
        2
    )