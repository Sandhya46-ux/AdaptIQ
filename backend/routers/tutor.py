from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag.retrieval import retrieve_context  # Imports your RAG logic!

router = APIRouter()

class TutorRequest(BaseModel):
    student_query: str
    concept: str = "General"

class TutorResponse(BaseModel):
    query: str
    grounded_context: str
    answer: str

router = APIRouter()

@router.post("/ask", response_model=TutorResponse)
def ask_tutor(request: TutorRequest):
    if not request.student_query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # 1. Fetch relevant context from your rag/ embeddings
    retrieved_text = retrieve_context(request.student_query)
    
    # 2. Mock or call LLM with retrieved context (for MVP)
    answer = f"Based on our course material: {retrieved_text[:200]}..."
    
    return TutorResponse(
        query=request.student_query,
        grounded_context=retrieved_text,
        answer=answer
    )