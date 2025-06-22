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
make build
```

2. Run the container:
```bash
make run
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

## Example: LLM-based /query request

### Request
```
POST /api/v1/query?top_k=3
{
  "question": "What is the main topic of the document?"
}
```

### Response
```
{
  "answer": "The main topic is ...",
  "context": [
    "First relevant chunk...",
    "Second relevant chunk...",
    "Third relevant chunk..."
  ],
  "top_k": 3
}
```

The system uses a HuggingFace LLM (e.g., T5-small) to generate the answer based on the top-k retrieved chunks.

## Example: NLU-enhanced /query request

### Request
```
POST /api/v1/query?top_k=3
{
  "question": "What is the main topic of the document?"
}
```

### Response
```
{
  "nlu": {
    "question": "What is the main topic of the document?",
    "labels": ["definition", "factoid", ...],
    "scores": [0.85, 0.10, ...],
    "top_label": "definition",
    "top_score": 0.85
  },
  "answer": "The main topic is ...",
  "context": [
    "First relevant chunk...",
    "Second relevant chunk...",
    "Third relevant chunk..."
  ],
  "top_k": 3
}
```

The system uses an NLU model to analyze the question and a HuggingFace LLM (e.g., T5-small) to generate the answer based on the top-k retrieved chunks.

## Example Input Documents

- `Dhruv Sharma.pdf`: A PDF file containing a my CV or any text document.

## Example Questions and Expected Outputs

| Example Question                                      | Example Output (answer)                |
|------------------------------------------------------|----------------------------------------|
| What companies has the candidate worked for?          | Google, Microsoft, OpenAI              |
| What programming languages does the candidate know?   | Python, Java, C++                      |
| What is the main topic of the document?               | The main topic is ...                  |
| List all certifications mentioned in the document.    | AWS Certified, PMP, Scrum Master       |
| What is the candidate's highest degree?               | Master of Science in Computer Science  |

*Note: Outputs will vary depending on the document content.*
