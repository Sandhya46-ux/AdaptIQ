def calculate_behavior_score(
    accuracy,
    response_time,
    confidence,
    hint_rate
):

    score = accuracy * 0.5

    # Confidence contribution
    score += confidence * 0.2

    # Lower response time is generally better.
    if response_time <= 20:
        speed_score = 100
    elif response_time <= 40:
        speed_score = 75
    elif response_time <= 60:
        speed_score = 50
    else:
        speed_score = 25

    score += speed_score * 0.2

    # Lower hint dependency is better.
    score += (100 - hint_rate) * 0.1

    return round(
        min(score, 100),
        2
    )


def build_learner_profile(
    attempts
):

    if not attempts:

        return {
            "accuracy": 0,
            "average_response_time": 0,
            "average_confidence": 0,
            "hint_rate": 0,
            "behavior_score": 0
        }

    total = len(attempts)

    correct = sum(
        1
        for attempt in attempts
        if attempt["correct"]
    )

    accuracy = (
        correct / total
    ) * 100

    average_response_time = (
        sum(
            attempt[
                "response_time_seconds"
            ]
            for attempt in attempts
        )
        / total
    )

    average_confidence = (
        sum(
            attempt["confidence"]
            for attempt in attempts
        )
        / total
    )

    hints = sum(
        1
        for attempt in attempts
        if attempt["hint_used"]
    )

    hint_rate = (
        hints / total
    ) * 100

    behavior_score = calculate_behavior_score(
        accuracy,
        average_response_time,
        average_confidence,
        hint_rate
    )

    return {
        "accuracy": round(accuracy, 2),
        "average_response_time": round(
            average_response_time,
            2
        ),
        "average_confidence": round(
            average_confidence,
            2
        ),
        "hint_rate": round(
            hint_rate,
            2
        ),
        "behavior_score": behavior_score
    }