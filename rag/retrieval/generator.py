import os
from rag.retrieval.retrieval import retrieve_context

def generate_grounded_answer(student_query: str) -> dict:
    """Retrieves context and generates a grounded response."""
    context = retrieve_context(student_query, top_k=3)
    
    if "Error: Database not found" in context or "No relevant context" in context:
        return {
            "query": student_query,
            "context_used": "None",
            "answer": "I don't have enough information in my educational material to answer this question accurately."
        }

    system_prompt = f"""
You are AdaptIQ's AI Tutor. Use ONLY the following retrieved educational context to answer the student's question.
If the answer cannot be deduced directly from the context, state that you do not have sufficient course information.

--- RETRIEVED CONTEXT ---
{context}
-------------------------

STUDENT QUESTION: {student_query}

TUTOR ANSWER:
"""

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(system_prompt)
            answer_text = response.text
        except Exception as e:
            answer_text = f"Grounded Context Found:\n{context}\n\n(LLM API Error: {str(e)})"
    else:
        answer_text = f"Based on your course materials:\n\n{context}\n\n[Note: Add GEMINI_API_KEY to .env for AI generation]"

    return {
        "query": student_query,
        "context_used": context,
        "answer": answer_text
    }
