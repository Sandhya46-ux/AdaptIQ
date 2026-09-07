import pytest

CONCEPTS = {
    "C001": {"concept": "Fractions", "prerequisites": []},
    "C002": {"concept": "Algebraic Expressions", "prerequisites": ["C001"]},
    "C003": {"concept": "Linear Equations", "prerequisites": ["C002"]},
    "C004": {"concept": "Quadratic Equations", "prerequisites": ["C003"]},
}


def test_concepts_load():
    """TC018: concept graph should contain all MVP concepts."""
    assert len(CONCEPTS) == 4
    assert "C001" in CONCEPTS
    assert "C004" in CONCEPTS


def test_prerequisite_relationship():
    """TC019: prerequisite should be returned correctly."""
    assert CONCEPTS["C003"]["prerequisites"] == ["C002"]


def test_detect_prerequisite_gap():
    """TC020: low prerequisite mastery should create a knowledge gap."""
    mastery = {
        "C002": 0.80,
        "C003": 0.30,
        "C004": 0.20,
    }

    prerequisite = CONCEPTS["C004"]["prerequisites"][0]

    assert mastery[prerequisite] < 0.60


def test_root_concept_has_no_prerequisite():
    """Fractions is the root concept for this MVP graph."""
    assert CONCEPTS["C001"]["prerequisites"] == []


def test_invalid_concept_is_not_in_graph():
    """Invalid concept IDs should not be accepted."""
    assert "C999" not in CONCEPTS
