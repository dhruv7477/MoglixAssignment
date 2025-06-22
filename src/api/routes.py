from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import logging

logger = logging.getLogger(__name__)
from typing import List
import os
import uuid
from pydantic import BaseModel
from ..document_processor import DocumentProcessor
from ..vector_db import VectorDB
from ..rag import RAGGenerator
from ..nlu import NLUAnalyzer

router = APIRouter()
vector_db = VectorDB()
rag = RAGGenerator()
nlu = NLUAnalyzer()

class QueryRequest(BaseModel):
    question: str

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    file_ext = os.path.splitext(file.filename)[1]
    temp_path = f"temp_{uuid.uuid4()}{file_ext}"
    
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    try:
        logger.info(f"Processing document: {file.filename}")
        texts = DocumentProcessor.process_document(temp_path)
        logger.info(f"Processed {len(texts)} text chunks")
        
        if not vector_db.add_documents(texts):
            logger.error("Failed to add documents to vector database")
            raise HTTPException(
                status_code=500,
                detail="Failed to add documents to vector database"
            )
        logger.info("Successfully added documents to vector database")
        return {"message": "Document processed successfully"}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/process")
async def process_document(
    file: UploadFile = File(None),
    question: str = Form(None)
):
    """Process document and answer question in one request"""
    if not file or not question:
        raise HTTPException(
            status_code=400,
            detail="Both file and question are required"
        )

    # Process document
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    try:
        texts = DocumentProcessor.process_document(temp_path)
        vector_db.add_documents(texts)
        
        # Generate answer
        context = vector_db.query(question)
        answer = rag.generate_answer(question, context)
        
        return {
            "status": "success",
            "answer": answer,
            "context": context[0] if context else "",  # Return only first/most relevant context
            "document_processed": True
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/query")
async def query_api(request: QueryRequest, top_k: int = 3):
    """Answer a question using NLU, top-k relevant chunks, and LLM"""
    nlu_result = nlu.analyze(request.question)
    # Optionally, you could use nlu_result["top_label"] to adjust retrieval or prompt
    context_chunks = vector_db.query(request.question, n_results=top_k)
    answer = rag.generate_answer(request.question, context_chunks)
    return {
        "nlu": nlu_result,
        "answer": answer,
        "context": context_chunks,
        "top_k": top_k
    }