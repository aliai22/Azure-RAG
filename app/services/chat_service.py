from typing import Tuple, Optional
from app.data_models.conversation import Conversation
from app.services.storage.cosmos_storage import CosmosDB
from app.services.chatbot.rag_chatbot import RAGChatbot

class RAGService:
    def __init__(self):
        self.rag_chatbot = RAGChatbot()
        self.cosmos_service = CosmosDB()

    def process_message(self, query: str, conversation_id: Optional[str] = None) -> Tuple[str, str]:
        """Process a message and return response with conversation ID"""
        if not conversation_id:
            # Start a new conversation if no ID is provided
            conversation_id = self.start_new_conversation()
        
        # Get response from RAG chatbot
        response = self.rag_chatbot.answer_question(query, conversation_id)
        
        # Store in Cosmos DB
        self.cosmos_service.store_conversation(conversation_id, query, response)
        
        return response, conversation_id

    def get_conversation_history(self, conversation_id: str) -> Conversation:
        """Get conversation history from Cosmos DB"""
        items =  self.cosmos_service.get_conversation_history(conversation_id)
        return Conversation.from_cosmos_items(items)
    def start_new_conversation(self) -> str:
        """Start a new conversation"""
        new_id = self.cosmos_service.create_new_conversation()
        self.rag_chatbot.reset_conversation(new_id)
        return new_id