from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import concepts, flashcards, lectures, questions, uploads

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup hook for future connection validation and service warmups.
    yield
    # Shutdown hook placeholder.


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uploads.router)
app.include_router(lectures.router)
app.include_router(concepts.router)
app.include_router(flashcards.router)
app.include_router(questions.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
