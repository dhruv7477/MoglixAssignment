import chromadb
import uuid
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer

class VectorDB:
    def __init__(self, collection_name: str = "documents"):
        # Simplest ChromaDB client initialization
        self.client = chromadb.PersistentClient(path=".chromadb")
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None):
        """Add documents to the vector database"""
        try:
            if not documents:
                raise ValueError("No documents provided")
                
            embeddings = self.embedding_model.encode(documents).tolist()
            ids = [str(uuid.uuid4()) for _ in documents]
            
            # Clear existing documents if any exist
            try:
                self.collection.delete(where={})
            except Exception as e:
                print(f"Warning: Could not clear collection: {str(e)}")
            
            # Generate basic metadata if none provided
            metadatas = metadata if metadata else [{"source": "uploaded_document"} for _ in documents]
            
            # Add new documents
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            raise

    def query(self, text: str, n_results: int = 3) -> List[str]:
        """Query the vector database for top-k similar documents"""
        embedding = self.embedding_model.encode(text).tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results['documents'][0]  # List of top-k context strings