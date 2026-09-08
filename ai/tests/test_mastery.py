from ai.learner_model.mastery import update_mastery

def test_update_mastery_correct():
    mastery = {"Fractions": 50.0}
    updated = update_mastery(mastery, "Fractions", True)
    assert updated["Fractions"] == 65.0

def test_update_mastery_bounds():
    mastery = {"Algebra": 95.0}
    updated = update_mastery(mastery, "Algebra", True)
    assert updated["Algebra"] == 100.0  # Score cannot exceed 100%