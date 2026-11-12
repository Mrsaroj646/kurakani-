"""Kurakani - a local AI parenting assistant built with FastAPI and Ollama."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
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

# Allow the page to call the API even when it is opened directly as a file
# or from another dev server (e.g. VS Code Live Server on port 5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    reply: str


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


# Serve the chat page, CSS, JavaScript and images.
# Mounted last so it does not override the /api routes above.
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
