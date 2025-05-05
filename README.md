# RAG Chatbot API

A RAG (Retrieval-Augmented Generation) based chatbot API using Azure AI Search and Cosmos DB.

## Features

- RAG-based question answering using Azure AI Search
- Conversation history storage in Azure Cosmos DB
- RESTful API with FastAPI
- Vector search for semantic similarity
- Conversation management

## Prerequisites

- Python 3.8+
- Azure OpenAI Service
- Azure AI Search Service
- Azure Cosmos DB Account

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd AIsearch-RAG
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Azure credentials:
```env
# Azure OpenAI Settings
AZURE_OPENAI_API_KEY=your_openai_api_key
AZURE_OPENAI_ENDPOINT=your_openai_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_EMBEDDING_MODEL=your_embedding_model

# Azure AI Search Settings
AZURE_SEARCH_SERVICE_ENDPOINT=your_search_service_endpoint
AZURE_SEARCH_API_KEY=your_search_api_key
AZURE_SEARCH_INDEX_NAME=your_index_name

# Azure Cosmos DB Settings
COSMOS_ENDPOINT=your_cosmos_endpoint
COSMOS_KEY=your_cosmos_key
COSMOS_DATABASE=your_database_name
COSMOS_CONTAINER=your_container_name
```

## Running the API

Start the server:
```bash
cd app
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Chat
- `POST /api/v1/chat`
  - Send a message to the chatbot
  - Request body: `{"query": "your question", "conversation_id": "optional_id"}`

### Conversation Management
- `POST /api/v1/conversation/new`
  - Start a new conversation
- `GET /api/v1/conversation/{conversation_id}`
  - Get conversation history

## Project Structure

```
AIsearch-RAG/
├── app/
│   ├── api/                 # API routes and schemas
│   ├── core/               # Core configuration and security
│   ├── models/             # Data models
│   ├── services/           # Business logic services
│   └── main.py            # FastAPI application
├── tests/                 # Unit tests
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 