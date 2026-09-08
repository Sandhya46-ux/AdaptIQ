import os

def get_tutor_explanation(concept: str, rag_docs_dir: str = "rag/documents") -> str:
    """
    Retrieves trusted educational content from local RAG documents 
    to provide a grounded explanation for a struggling student.
    """
    # Clean the concept name to match filename conventions (e.g., "Linear Equations" -> "linear_equations.txt")
    filename = f"{concept.lower().replace(' ', '_')}.txt"
    file_path = os.path.join(rag_docs_dir, filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Return a snippet or summary of the curated text
            return content[:500] + "..." if len(content) > 500 else content
            
    # Fallback explanation if specific document isn't found
    return f"Let's break down {concept} step by step. Make sure to review your prerequisites and practice the foundational rules before trying again."