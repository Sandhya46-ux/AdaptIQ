def update_mastery(current_mastery: dict, concept: str, is_correct: bool) -> dict:
    """
    Updates a student's mastery score for a specific concept based on quiz performance.
    Increases score by 15% on correct answers and decreases by 10% on incorrect answers,
    bounding the score between 0.0 and 100.0.
    """
    current_score = current_mastery.get(concept, 0.0)
    adjustment = 15.0 if is_correct else -10.0
    
    new_score = max(0.0, min(100.0, current_score + adjustment))
    current_mastery[concept] = new_score
    return current_mastery