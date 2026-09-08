from ai.services.adaptive_service import AdaptiveLearningService

def test_adaptive_service_workflow():
    service = AdaptiveLearningService("data/concepts/math_concepts.json")
    
    initial_mastery = {"Fractions": 40.0}
    # User answers a question correctly for Fractions
    result = service.process_quiz_result("student_123", initial_mastery, "Fractions", True)
    
    assert result["updated_mastery"]["Fractions"] == 55.0
    assert isinstance(result["recommendations"], list)