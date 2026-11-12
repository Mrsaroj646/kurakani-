"""Kurakani - a local AI parenting assistant built with FastAPI and Ollama."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.config import settings
from app.services import AIServiceError, ai_service

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Kurakani AI Assistant",
    description="A local AI chatbot that gives parenting and child-development advice.",
    version="1.0.0",
)

# Serve CSS, JavaScript and images from the /static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str


@app.get("/", include_in_schema=False)
def index():
    """Return the chat web page."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "model": settings.OLLAMA_MODEL}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the AI model and return its reply."""
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        # The HTTP call to Ollama is blocking, so run it in a worker thread
        reply = await run_in_threadpool(ai_service.generate_chat_response, message)
    except AIServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ChatResponse(reply=reply)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
