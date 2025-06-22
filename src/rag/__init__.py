from typing import List
from transformers import pipeline

class RAGGenerator:
    def __init__(self, model_name: str = "t5-small"):
        self.generator = pipeline(
            "text2text-generation",
            model=model_name,
            device="cpu"
        )

    def generate_answer(self, question: str, context: List[str]) -> str:
        """Generate answer using RAG approach with LLM"""
        context_str = "\n".join(context)
        prompt = f"question: {question} context: {context_str}"
        
        result = self.generator(
            prompt,
            max_length=200,
            num_beams=4,
            early_stopping=True
        )
        
        return result[0]['generated_text']