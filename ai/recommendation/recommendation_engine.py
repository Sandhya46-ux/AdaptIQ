# import networkx as nx
# from ai.knowledge_graph.graph import get_missing_prerequisites

# def get_next_recommendations(graph: nx.DiGraph, user_mastery: dict, threshold: float = 50.0) -> list:
#     """
#     Determines which concepts the user is ready to learn next.
#     A concept is recommended if:
#     1. The user hasn't mastered it yet (mastery < threshold).
#     2. All of its direct prerequisites have been met (mastery >= threshold).
#     """
#     recommendations = []
    
#     for node in graph.nodes():
#         current_mastery = user_mastery.get(node, 0.0)
        
#         # Skip if already mastered
#         if current_mastery >= threshold:
#             continue
            
#         # Check if there are any unmastered prerequisites
#         missing_prereqs = get_missing_prerequisites(graph, node, user_mastery, threshold)
        
#         # If all prerequisites are satisfied, recommend this concept
#         if not missing_prereqs:
#             recommendations.append(node)
            
#     return recommendations


def calculate_priority(
    mastery,
    misconception_count=0,
    prerequisite_weak=False
):

    score = 0

    # Low mastery
    if mastery < 40:
        score += 50

    elif mastery < 60:
        score += 35

    elif mastery < 80:
        score += 20

    # Misconceptions
    score += min(
        misconception_count * 10,
        30
    )

    # Weak prerequisite
    if prerequisite_weak:
        score += 20

    return score