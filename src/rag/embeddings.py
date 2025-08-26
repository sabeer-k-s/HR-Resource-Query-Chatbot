# src/rag/embeddings.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Tuple

class EmbeddingsManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.dimension = None

    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        return self.model.encode(texts)

    def build_index(self, embeddings: np.ndarray) -> None:
        """Build FAISS index from embeddings."""
        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, k: int = 3) -> Tuple[np.ndarray, np.ndarray]:
        """Search FAISS index for top k matches."""
        if self.index is None:
            raise Exception("FAISS index not initialized")
        return self.index.search(query_embedding, k)