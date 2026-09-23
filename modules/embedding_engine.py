import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


class EmbeddingEngine:

    def __init__(self):

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        self.index = None

    def create_embeddings(self, texts):

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return embeddings.astype(
            "float32"
        )

    def build_index(self, embeddings):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(embeddings)

    def search(self, query, k=8):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = self.index.search(
            query_embedding.astype("float32"),
            k
        )

        return scores[0], indices[0]