from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse
from .logic import process_message
from .database import init_db

app = FastAPI()

# This is insecure for production, but fine for this assignment
# In production, list the specific frontend URL
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # Establishes the DB and table if they don't exist
    init_db()

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    if not request.message or not request.session_id:
        raise HTTPException(status_code=400, detail="Message and session_id are required.")
    
    try:
        reply = process_message(request.session_id, request.message)
        return ChatResponse(reply=reply, session_id=request.session_id)
    except Exception as e:
        # Avoid leaking internal error details to the client
        print(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")