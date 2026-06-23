import os  # <-- Add this line right at the top!
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.ai_service import ai_service

app = FastAPI()

# Allow your webpage to communicate with your backend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    # This automatically finds the correct folder path no matter what
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "index.html")
    
    # If it's accidentally inside the app folder, check there too
    if not os.path.exists(file_path):
        file_path = os.path.join(base_dir, "app", "index.html")
        
    return FileResponse(file_path)

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    ai_response = ai_service.generate_chat_response(request.message)
    return ai_response