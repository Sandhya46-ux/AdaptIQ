from ai.knowledge_graph.graph import build_prerequisite_graph
from AdaptIQ.ai.recommendation.recommendation_engine import get_next_recommendations

def t_path():
    return "data/concepts/math_concepts.json"

def test_get_recommendations():
    G = build_prerequisite_graph(t_path())
    # Suppose the user has mastered Fractions (>= 50), but Algebra is still low (< 50)
    user_mastery = {"Fractions": 80.0, "Algebra": 20.0}
    
    recs = get_next_recommendations(G, user_mastery, threshold=50.0)
    
    # Since Fractions is mastered, Algebra should be recommended. 
    # Linear Equations shouldn't be recommended yet because its prerequisite (Algebra) is unmastered.
    assert isinstance(recs, list)
    assert len(recs) > 0