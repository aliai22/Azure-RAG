import os
from typing import List, Dict
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential 
from openai import AzureOpenAI
from collections import deque
from typing import Optional
from app.services.storage.cosmos_storage import CosmosDB

from dotenv import load_dotenv
load_dotenv()

class RAGChatbot:
    def __init__(self, max_history: int = 5):
        self.chat_client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-12-01-preview"
        )

        self.embeddings_client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01"
        )

        self.search_client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT"),
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY")),
            index_name=os.getenv("AZURE_SEARCH_INDEX_NAME")
        )

        # Initialize conversation history
        self.conversation_history = deque(maxlen=max_history)

        # Initialize Cosmos DB storage      
        self.storage = CosmosDB()
        self.conversation_id = self.storage.create_new_conversation()

    def _get_query_embedding(self, query: str) -> List[float]:
        """Get embedding for the query using Azure OpenAI"""
        response = self.embeddings_client.embeddings.create(
            model=os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
            input=query
        )
        return response.data[0].embedding

    def search_relevant_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant documents using vector search"""
        # Get the query embedding
        query_vector = self._get_query_embedding(query)
        
        # Use vector search to find relevant documents
        results = self.search_client.search(
            search_text=query,
            select=["chunk", "title"],
            top=top_k,
            vector_queries=[
                {
                    "kind": "vector",
                    "vector": query_vector,
                    "k": top_k,
                    "fields": "text_vector"  # The field in your index that contains the document vectors
                }
            ]
        )
        
        return [{"text": result.get("chunk"),
                 "reference": result.get("title")}
                for result in results]
    
    def generate_response(self, query: str, context: List[Dict]) -> str:
        """Generate a response using the retrieved context"""
        context_text = "\n\n".join([
            f"Source: {doc['reference']}\nContent: {doc['text']}" 
            for doc in context
        ])

        # Get conversation history from Cosmos DB
        db_history = self.storage.get_conversation_history(self.conversation_id)
        history_text = "\n".join([
            f"User: {item['query']}\nAssistant: {item['response']}"
            for item in db_history
        ])

        prompt = f"""Use the following context and conversation history to answer the user's query.
        
        Conversation History:
        {history_text}

        Context:
        {context_text}
        
        Question: {query}

        Answer:"""
        
        response = self.chat_client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[{"role": "system", "content": "You are a helpful AI assistant. Use the provided context and conversation history to briefly answer the user's query."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def answer_question(self, query: str, conversation_id: str = None) -> str:
        """Answer a question using RAG"""
        if conversation_id:
            self.conversation_id = conversation_id

        print(f"Message Thread: {self.conversation_history}")

        # Search for relevant documents
        relevant_docs = self.search_relevant_documents(query)
        
        # Generate response using the context
        response = self.generate_response(query, relevant_docs)
        
        # Store in conversation history
        self.conversation_history.append({
            "query": query,
            "response": response
        })
        
        return response
    
    def reset_conversation(self, new_id: Optional[str] = None):
        """Start a new conversation"""
        self.conversation_id = new_id or self.storage.create_new_conversation()
        self.conversation_history.clear()