from ai.tutor.tutor import get_tutor_explanation

def test_get_tutor_explanation():
    explanation = get_tutor_explanation("Linear Equations")
    assert isinstance(explanation, str)
    assert len(explanation) > 0