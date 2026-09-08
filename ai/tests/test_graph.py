from ai.knowledge_graph.graph import build_prerequisite_graph, get_missing_prerequisites

def t_path():
    return "data/concepts/math_concepts.json"

def test_build_graph():
    G = build_prerequisite_graph(t_path())
    assert len(G.nodes) > 0
    # Check for nodes that actually exist in your math_concepts.json file
    assert "Fractions" in G.nodes or "Linear Equations" in G.nodes

def test_missing_prerequisites():
    G = build_prerequisite_graph(t_path())
    user_mastery = {"Fractions": 80.0, "Algebraic Expressions": 30.0}
    # Test with a target concept and check that the returned list is valid
    missing = get_missing_prerequisites(G, "Linear Equations", user_mastery, threshold=50.0)
    assert isinstance(missing, list)