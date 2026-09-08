from ai.adaptive_quiz.selector import select_adaptive_question

def test_select_adaptive_question():
    # Test with a low mastery score, expecting an easy question if available
    question = select_adaptive_question("data/questions/math_questions.json", "Fractions", 25.0)
    assert isinstance(question, dict)