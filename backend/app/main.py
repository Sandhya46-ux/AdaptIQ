from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import diagnostic
from app.routes import quiz
from app.routes import learning_path
from app.routes import progress
from app.routes import tutor


app = FastAPI(
    title="AdaptIQ API",
    description="Adaptive Learning Intelligence Platform",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

app.include_router(
    diagnostic.router,
    prefix="/diagnostic",
    tags=["Diagnostic"]
)

app.include_router(
    quiz.router,
    prefix="/quiz",
    tags=["Quiz"]
)

app.include_router(
    learning_path.router,
    prefix="/learning-path",
    tags=["Learning Path"]
)

app.include_router(
    progress.router,
    prefix="/progress",
    tags=["Progress"]
)

app.include_router(
    tutor.router,
    prefix="/tutor",
    tags=["AI Tutor"]
)


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to AdaptIQ API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }