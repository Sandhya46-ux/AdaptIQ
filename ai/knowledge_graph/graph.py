'''import json
import networkx as nx

def build_prerequisite_graph(json_path: str) -> nx.DiGraph:
    """
    Loads concept prerequisites from a JSON file, automatically handling 
    lists, nested dicts, or direct dict mappings.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    G = nx.DiGraph()
    items = {}

    # Case 1: Data is a list of concept objects
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                name = item.get("name") or item.get("concept") or item.get("id")
                if name:
                    items[name] = item

    # Case 2: Data is a dictionary
    elif isinstance(data, dict):
        # Check if it has a 'concepts' wrapper key
        raw_items = data.get('concepts', data)
        if isinstance(raw_items, dict):
            items = raw_items
        elif isinstance(raw_items, list):
            for item in raw_items:
                if isinstance(item, dict):
                    name = item.get("name") or item.get("concept") or item.get("id")
                    if name:
                        items[name] = item

    # Build the NetworkX graph from the parsed items
    for concept, details in items.items():
        G.add_node(concept)
        prereqs = []
        if isinstance(details, dict):
            prereqs = details.get('prerequisites', []) or details.get('prereqs', [])
        
        for prereq in prereqs:
            G.add_edge(prereq, concept)
            
    return G

def get_missing_prerequisites(graph: nx.DiGraph, target_concept: str, user_mastery: dict, threshold: float = 50.0) -> list:
    """
    Identifies direct prerequisites of the target concept that the user has not yet mastered.
    """
    if target_concept not in graph:
        return []
    
    prereqs = list(graph.predecessors(target_concept))
    missing = [p for p in prereqs if user_mastery.get(p, 0.0) < threshold]
    return missing'''
    
    
    from collections import defaultdict


class KnowledgeGraph:

    def __init__(self, concepts):

        self.graph = defaultdict(list)

        for concept in concepts:

            concept_id = concept["concept_id"]

            prerequisites = concept.get(
                "prerequisites",
                []
            )

            for prerequisite in prerequisites:

                self.graph[concept_id].append(
                    prerequisite
                )


    def get_prerequisites(self, concept_id):

        return self.graph.get(
            concept_id,
            []
        )


    def get_all_prerequisites(self, concept_id):

        visited = set()

        def dfs(current):

            if current in visited:
                return

            visited.add(current)

            for prerequisite in self.get_prerequisites(current):

                dfs(prerequisite)

        dfs(concept_id)

        visited.discard(concept_id)

        return list(visited)