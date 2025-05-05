import os
from azure.cosmos import CosmosClient
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class CosmosDB:
    def __init__(self):
        # Initialize Cosmos DB client
        self.client = CosmosClient(
            os.getenv("COSMOS_ENDPOINT"),
            os.getenv("COSMOS_KEY")
        )
        
        # Get database and container
        self.database = self.client.get_database_client(os.getenv("COSMOS_DATABASE"))
        self.container = self.database.get_container_client(os.getenv("COSMOS_CONTAINER"))

    def store_conversation(self, conversation_id: str, query: str, response: str) -> None:
        """Store a conversation turn in Cosmos DB"""
        item = {
            "id": f"{conversation_id}_{datetime.now().isoformat()}",
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response
        }
        
        self.container.create_item(body=item)

    def get_conversation_history(self, conversation_id: str, limit: int = 5) -> List[Dict]:
        """Retrieve conversation history from Cosmos DB"""
        query = f"SELECT * FROM c WHERE c.conversation_id = @conversation_id ORDER BY c.timestamp DESC OFFSET 0 LIMIT @limit"
        parameters = [
            {"name": "@conversation_id", "value": conversation_id},
            {"name": "@limit", "value": limit}
        ]
        
        items = list(self.container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        # Sort by timestamp ascending for chronological order
        return sorted(items, key=lambda x: x["timestamp"])

    def create_new_conversation(self) -> str:
        """Create a new conversation and return its ID"""
        # Generate a unique conversation ID
        conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return conversation_id
