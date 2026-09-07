import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Relative path from project root to the generated embeddings
EMBEDDINGS_PATH = "./rag/embeddings"

def retrieve_context(student_query: str, top_k: int = 3) -> str:
    """Searches ChromaDB for relevant document chunks."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if not os.path.exists(EMBEDDINGS_PATH):
        return "Error: Database not found. Run ingest.py first."
        
    vector_db = Chroma(
        persist_directory=EMBEDDINGS_PATH, 
        embedding_function=embeddings
    )
    
    relevant_docs = vector_db.similarity_search(student_query, k=top_k)
    
    if not relevant_docs:
        return "No relevant context found in the educational data."
        
    return "\n\n---\n\n".join([doc.page_content for doc in relevant_docs])
