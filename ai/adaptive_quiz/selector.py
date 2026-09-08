import json

def load_questions(json_path: str) -> list:
    """Loads questions from the JSON data file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle list or nested dictionary formats gracefully
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return data.get('questions', data.get('items', []))
    return []

def select_adaptive_question(questions_path: str, concept: str, user_mastery_score: float) -> dict:
    """
    Selects an appropriate quiz question for a specific concept based on the user's current mastery score.
    - Mastery < 40.0 -> Select 'easy' difficulty
    - Mastery between 40.0 and 75.0 -> Select 'medium' difficulty
    - Mastery > 75.0 -> Select 'hard' difficulty
    """
    questions = load_questions(questions_path)
    
    # Filter questions matching the target concept
    concept_questions = [
        q for q in questions 
        if q.get('concept', '').lower() == concept.lower() or q.get('topic', '').lower() == concept.lower()
    ]
    
    if not concept_questions:
        return {} # Fallback if no specific concept questions found
        
    # Determine target difficulty based on mastery score
    if user_mastery_score < 40.0:
        target_difficulty = "easy"
    elif user_mastery_score <= 75.0:
        target_difficulty = "medium"
    else:
        target_difficulty = "hard"
        
    # Try to find a question matching the target difficulty
    matched = [q for q in concept_questions if q.get('difficulty', '').lower() == target_difficulty]
    
    # Fallback: if exact difficulty isn't available, just return the first available concept question
    if matched:
        return matched[0]
    return concept_questions[0]