from ai.knowledge_graph.graph import build_prerequisite_graph, get_missing_prerequisites
from ai.learner_model.mastery import update_mastery
from AdaptIQ.ai.recommendation.recommendation_engine import get_next_recommendations

class AdaptiveLearningService:
    def __init__(self, concepts_path: str):
        self.graph = build_prerequisite_graph(concepts_path)
        
    def process_quiz_result(self, user_id: str, current_mastery: dict, concept: str, is_correct: bool) -> dict:
        """
        Updates student mastery based on a quiz attempt, checks for missing prerequisites,
        and returns the next recommended concepts to study.
        """
        # 1. Update mastery for the attempted concept
        updated_mastery = update_mastery(current_mastery, concept, is_correct)
        
        # 2. Check if there are any missing prerequisites for concepts the user wants to tackle
        missing_prereqs = get_missing_prerequisites(self.graph, concept, updated_mastery)
        
        # 3. Generate updated list of recommended next concepts
        recommendations = get_next_recommendations(self.graph, updated_mastery)
        
        return {
            "user_id": user_id,
            "updated_mastery": updated_mastery,
            "missing_prerequisites": missing_prereqs,
            "recommendations": recommendations
        }