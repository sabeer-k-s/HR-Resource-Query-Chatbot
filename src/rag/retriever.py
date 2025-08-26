# src/rag/retriever.py
from typing import List, Dict
from .embeddings import EmbeddingsManager
import numpy as np

class Retriever:
    def __init__(self, employees: List[Dict], embeddings_manager: EmbeddingsManager):
        self.employees = employees
        self.embeddings_manager = embeddings_manager
        # Create text representations for embeddings
        self.employee_texts = [
            f"{emp['name']} has {emp['experience_years']} years of experience, "
            f"skills: {', '.join(emp['skills'])}, "
            f"projects: {', '.join(emp['projects'])}, "
            f"availability: {emp['availability']}"
            for emp in employees
        ]
        # Build FAISS index
        embeddings = self.embeddings_manager.create_embeddings(self.employee_texts)
        self.embeddings_manager.build_index(embeddings)

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        """Retrieve top k employees matching the query."""
        query_embedding = self.embeddings_manager.create_embeddings([query])[0]
        distances, indices = self.embeddings_manager.search(np.array([query_embedding]), k)
        return [self.employees[i] for i in indices[0]]