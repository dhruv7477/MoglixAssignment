# UI Enhancement Tasks

## Frontend Changes (app.py)
1. Remove health check API button and related code
2. Combine document upload and question sections into single form
3. Add prominent "Send" button that triggers processing
4. Modify API call to send both file and question:
   ```python
   response = requests.post(
       f"{API_URL}/process",
       files={"file": (uploaded_file.name, file_data)},
       data={"question": question}
   )
   ```
5. Add loading spinner during processing
6. Display results in organized sections:
   - Answer
   - Single most relevant supporting context
   - Processing status

## Backend Changes (routes.py)
1. Create new `/process` endpoint that:
   - Accepts multipart form with both file and question
   - Processes document immediately
   - Generates answer using the uploaded content
   - Returns only the most relevant context
2. Update response format:
   ```python
   return {
       "status": "success",
       "answer": answer,
       "context": most_relevant_context,  # Single context string
       "document_processed": True
   }
   ```
3. Modify vector DB query to return only 1 most relevant result:
   ```python
   results = self.collection.query(
       query_embeddings=[embedding],
       n_results=1  # Only get most relevant context
   )
   ```
4. Add validation for:
   - File presence and type
   - Question length and content
   - Processing errors

# Backend Enhancement Tasks for RAG LLM Integration

## LLM-based Answer Generation
1. Ensure the backend retrieves top-k relevant chunks from the vector database for each user question.
2. Concatenate or format these chunks as context for the LLM.
3. Pass the combined context and question to a HuggingFace LLM (e.g., T5-small) for answer generation.
4. Return the generated answer from the LLM in the API response.

## API Changes
1. Update the `/query` endpoint to:
   - Accept a `top_k` parameter (optional, default to 3).
   - Retrieve top-k relevant chunks from the vector DB.
   - Pass all chunks to the LLM for answer generation.
   - Return both the answer and the context used.
2. Update OpenAPI docs to reflect the new parameter and response structure.

## Code Refactoring
1. Refactor the vector DB query method to support `n_results` (top-k retrieval).
2. Refactor the RAG pipeline to use the LLM for final answer generation, not just context return.
3. Add or update unit tests to verify LLM-based answer generation with multiple context chunks.

## Documentation
1. Update README.md to clarify that the system uses an LLM for answer generation, not just retrieval.
2. Add example API requests/responses showing LLM-generated answers.

## Testing
1. Test with various questions and document sets to ensure the LLM is used and answers are relevant.
2. Validate that the context passed to the LLM includes all top-k chunks.
3. Ensure performance is acceptable with the LLM in the loop.

## Testing Requirements
1. Test scenarios:
   - Valid file + question
   - Missing file
   - Missing question  
   - Large files
   - Various file types (PDF, TXT, CSV)
2. Verify:
   - Only single context is returned
   - Response times
   - Error messages
   - UI state changes

## Deployment Checklist
1. Update API documentation
2. Test in containerized environment
3. Verify no breaking changes for existing clients

# NLU Integration for RAG Pipeline

## NLU Model Integration
1. Integrate an open-source NLU model (e.g., transformers pipeline for zero-shot-classification or question type detection) to analyze the user's question before retrieval.
2. Use the NLU output to:
   - Optionally reformulate or classify the question.
   - Adjust retrieval or answer generation logic if needed (e.g., different prompt templates, retrieval strategies, or answer formats).
3. Pass the processed question to the RAG retrieval and LLM answer generation pipeline.
4. Return both the NLU analysis and the final answer in the API response for transparency.

## Code Changes
1. Add an NLU module/class (e.g., NLUAnalyzer) using HuggingFace transformers or similar.
2. Update the `/query` endpoint to:
   - Run the NLU model on the user's question.
   - Use the NLU output to inform the RAG process.
   - Return NLU results in the API response.
3. Add or update unit tests for NLU integration and its effect on RAG answers.

## Documentation
1. Update README.md to describe the NLU step and its role in the pipeline.
2. Add example API requests/responses showing NLU output and LLM-generated answers.

## Testing
1. Test with various question types to ensure NLU is working and improves answer quality.
2. Validate that the NLU output is meaningful and used in the pipeline.