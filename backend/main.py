from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import diagnostic, quiz, recommendation, tutor

app = FastAPI(title="AdaptIQ API Layer", version="1.0.0")

# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust port in production if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints
app.include_router(diagnostic.router, prefix="/api/diagnostic", tags=["Diagnostic"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(recommendation.router, prefix="/api/recommendation", tags=["Recommendation"])
app.include_router(tutor.router, prefix="/api/tutor", tags=["Tutor"])

@app.get("/")
def read_root():
    return {"status": "online", "message": "AdaptIQ FastAPI Backend Running"}
