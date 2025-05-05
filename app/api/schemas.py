from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

class ConversationTurn(BaseModel):
    query: str
    response: str
    timestamp: datetime

class ConversationHistory(BaseModel):
    conversation_id: str
    turns: List[ConversationTurn]

class NewConversationResponse(BaseModel):
    conversation_id: str
    message: str = "New conversation started" 