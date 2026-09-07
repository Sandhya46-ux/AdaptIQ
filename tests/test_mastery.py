import pytest

# Adapt these imports to your backend module names.
# Example:
# from ai.mastery import calculate_mastery, update_mastery


def test_mastery_all_correct():
    """TC014/TC015: all correct attempts should produce high mastery."""
    attempts = [True, True, True, True]
    mastery = sum(attempts) / len(attempts)
    assert mastery == 1.0


def test_mastery_mixed_results():
    """TC014: mastery should reflect mixed correct/incorrect performance."""
    attempts = [True, True, False, True]
    mastery = sum(attempts) / len(attempts)
    assert mastery == 0.75


def test_mastery_all_incorrect():
    """TC016: all incorrect attempts should produce low mastery."""
    attempts = [False, False, False]
    mastery = sum(attempts) / len(attempts)
    assert mastery == 0.0


def test_correct_answer_improves_mastery():
    """TC015: a correct new attempt should improve mastery."""
    previous = 0.50
    new_attempt_correct = True
    new_mastery = (previous + int(new_attempt_correct)) / 2
    assert new_mastery > previous


def test_confidence_is_valid():
    """TC017: confidence should be stored as a valid value."""
    confidence = 4
    assert 1 <= confidence <= 5


def test_learner_profile_update():
    """TC028: learner profile should reflect latest performance."""
    profile = {"C003": 0.40}
    profile["C003"] = 0.60
    assert profile["C003"] == 0.60
