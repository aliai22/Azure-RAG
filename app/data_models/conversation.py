from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel

class ConversationTurn(BaseModel):
    query: str
    response: str
    timestamp: datetime

class Conversation(BaseModel):
    conversation_id: str
    turns: List[ConversationTurn]
    
    @classmethod
    def from_cosmos_items(cls, items: List[Dict]) -> 'Conversation':
        """Create a Conversation instance from Cosmos DB items"""
        if not items:
            raise ValueError("No conversation items found")
            
        conversation_id = items[0]["conversation_id"]
        turns = [
            ConversationTurn(
                query=item["query"],
                response=item["response"],
                timestamp=datetime.fromisoformat(item["timestamp"])
            )
            for item in items
        ]
        
        return cls(
            conversation_id=conversation_id,
            turns=turns
        ) 