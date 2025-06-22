from transformers import pipeline
from typing import Dict, List

class NLUAnalyzer:
    def __init__(self, candidate_labels=None):
        if candidate_labels is None:
            # Example question types; customize as needed
            candidate_labels = [
                "factoid",
                "definition",
                "list",
                "yes/no",
                "reasoning",
                "other"
            ]
        self.candidate_labels = candidate_labels
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

    def analyze(self, question: str) -> Dict:
        result = self.classifier(question, self.candidate_labels)
        return {
            "question": question,
            "labels": result["labels"],
            "scores": result["scores"],
            "top_label": result["labels"][0],
            "top_score": result["scores"][0]
        }

    def extract_entities(self, context: str) -> List[Dict]:
        """Extract named entities from context using NER"""
        return self.ner(context)

    def filter_entities(self, entities: List[Dict], entity_types: List[str]) -> List[str]:
        """Filter entities by type (e.g., ORG for organizations)"""
        return [e['word'] for e in entities if e['entity_group'] in entity_types]
