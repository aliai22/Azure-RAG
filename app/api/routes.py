from fastapi import APIRouter, HTTPException
from app.services.chat_service import RAGService
from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationHistory,
    NewConversationResponse
)

router = APIRouter()
rag_service = RAGService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle a chat request"""
    try:
        response, conversation_id = rag_service.process_message(
            request.query,
            request.conversation_id
        )
        return ChatResponse(
            response=response,
            conversation_id=conversation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{conversation_id}", response_model=ConversationHistory)
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    try:
        history = rag_service.get_conversation_history(conversation_id)
        return {
            "conversation_id": conversation_id,
            "turns": history
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/conversation/new", response_model=NewConversationResponse)
async def start_new_conversation():
    """Start a new conversation"""
    try:
        conversation_id = rag_service.start_new_conversation()
        return NewConversationResponse(conversation_id=conversation_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 