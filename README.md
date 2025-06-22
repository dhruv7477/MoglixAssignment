# RAG-Based Question-Answering Chatbot

A containerized Python application that implements a Retrieval-Augmented Generation (RAG) system for document-based question answering.

## Features
- Document ingestion (PDF, TXT, CSV)
- Semantic search using ChromaDB vector database
- Answer generation using T5-small language model
- REST API with FastAPI
- Docker containerization

## Quick Start

1. Build the Docker image:
```bash
docker build -t rag-chatbot .
```

2. Run the container:
```bash
docker run -p 8000:8000 rag-chatbot
```

3. Test the API:
```bash
# Upload a document
curl -X POST -F "file=@sample.pdf" http://localhost:8000/api/v1/upload

# Ask a question
curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the main topic?"}' http://localhost:8000/api/v1/query
```

## API Endpoints
- `POST /api/v1/upload` - Upload a document
- `POST /api/v1/query` - Ask a question
- `GET /health` - Health check

## Development
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run locally:
```bash
uvicorn src.main:app --reload
```

## Configuration
Environment variables:
- `CHROMA_DB_PATH` - Path to persist ChromaDB data (default: `.chromadb`)
- `MODEL_NAME` - HuggingFace model name (default: `t5-small`)