from fastapi import APIRouter
from pydantic import BaseModel
from rag.retrieval.generator import generate_grounded_answer

router = APIRouter(prefix="/api/tutor", tags=["Tutor"])

class QueryRequest(BaseModel):
    query: str

@router.post("/ask")
async def ask_tutor(request: QueryRequest):
    response = generate_grounded_answer(request.query)
    return response