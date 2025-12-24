# utils/embedding.py

from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def get_embedding(self, text: str):
        return np.array(self.model.encode([text], convert_to_numpy=True))

    def get_embeddings(self, texts: list):
        return np.array(self.model.encode(texts, convert_to_numpy=True))


# Create global embedding model instance
embedder = EmbeddingModel()