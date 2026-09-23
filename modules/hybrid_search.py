import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import (
    SEMANTIC_WEIGHT,
    TFIDF_WEIGHT
)


class HybridSearch:

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=10000
        )

        self.tfidf_matrix = None

    def build_tfidf(self, texts):

        self.tfidf_matrix = (
            self.vectorizer.fit_transform(
                texts
            )
        )

    def search_tfidf(self, query):

        query_vector = (
            self.vectorizer.transform(
                [query]
            )
        )

        scores = cosine_similarity(
            query_vector,
            self.tfidf_matrix
        )[0]

        return scores

    def combine_scores(
        self,
        semantic_scores,
        tfidf_scores
    ):

        semantic_scores = np.array(
            semantic_scores
        )

        tfidf_scores = np.array(
            tfidf_scores
        )

        if semantic_scores.max() > 0:

            semantic_scores = (
                semantic_scores /
                semantic_scores.max()
            )

        if tfidf_scores.max() > 0:

            tfidf_scores = (
                tfidf_scores /
                tfidf_scores.max()
            )

        return (
            SEMANTIC_WEIGHT *
            semantic_scores
            +
            TFIDF_WEIGHT *
            tfidf_scores
        )