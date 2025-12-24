# db/faiss_store.py

import faiss
import numpy as np
import os

class FAISSStore:
    def __init__(self, dim=384, index_path="faiss.index"):
        self.dim = dim
        self.index_path = index_path

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatL2(dim)

    def add_embeddings(self, embeddings: np.ndarray):
        self.index.add(embeddings)
        faiss.write_index(self.index, self.index_path)

    def search(self, query_embedding: np.ndarray, k=5):
        distances, indices = self.index.search(query_embedding, k)
        return distances, indices


# Global FAISS instance
faiss_store = FAISSStore()