from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str

class ConversationState(BaseModel):
    session_id: str
    state: str = "AWAITING_NAME"
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    move_in_date: Optional[str] = None
    beds: Optional[int] = None