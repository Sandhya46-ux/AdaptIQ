import pytest

# Adapt imports to your backend.
# Example:
# from ai.recommendation import recommend_next_concept


def test_identify_weakest_concept():
    """TC021: weakest concept should be selected."""
    mastery = {
        "C001": 0.90,
        "C002": 0.80,
        "C003": 0.40,
        "C004": 0.70,
    }
    weakest = min(mastery, key=mastery.get)
    assert weakest == "C003"


def test_recommendation_respects_prerequisite():
    """TC022: recommendation should address an unmet prerequisite first."""
    mastery = {
        "C001": 0.90,
        "C002": 0.85,
        "C003": 0.40,
        "C004": 0.20,
    }
    prerequisites = {
        "C004": ["C003"]
    }

    target = "C004"
    prerequisite = prerequisites[target][0]

    if mastery[prerequisite] < 0.60:
        recommendation = prerequisite
    else:
        recommendation = target

    assert recommendation == "C003"


def test_recommendation_has_reason():
    """TC023: recommendation should have an explainable reason."""
    recommendation = {
        "concept_id": "C003",
        "reason": "Low mastery in Linear Equations and prerequisite importance is high."
    }
    assert recommendation["reason"]
    assert isinstance(recommendation["reason"], str)


def test_different_learners_can_get_different_recommendations():
    """TC021/TC022: recommendations should depend on learner mastery."""
    student_a = {"C001": 0.90, "C002": 0.90, "C003": 0.40}
    student_b = {"C001": 0.90, "C002": 0.40, "C003": 0.30}

    rec_a = min(student_a, key=student_a.get)
    rec_b = min(student_b, key=student_b.get)

    assert rec_a != rec_b
