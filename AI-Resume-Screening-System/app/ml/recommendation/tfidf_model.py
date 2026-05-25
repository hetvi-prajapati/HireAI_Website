# ============================================================
#  TalentSync — TF-IDF Vectorizer
#  Converts text into numerical vectors for similarity search.
#  Pure-Python implementation (no sklearn required).
#  Swap with sklearn TfidfVectorizer for larger datasets.
# ============================================================

import math
import re
from collections import Counter
from app.ml.preprocessing.clean_text import preprocess_to_string
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TFIDFVectorizer:
    """
    Lightweight TF-IDF vectorizer.
    Fit on a corpus of documents, then transform any text to a vector.
    """

    def __init__(self):
        self.vocabulary: dict[str, int] = {}
        self.idf: dict[str, float] = {}
        self._fitted = False

    def fit(self, documents: list[str]) -> 'TFIDFVectorizer':
        """
        Build vocabulary and compute IDF scores from a corpus.

        Args:
            documents: List of raw text strings.
        """
        processed = [preprocess_to_string(d) for d in documents]
        all_tokens = set()
        doc_freq: dict[str, int] = {}

        for doc in processed:
            tokens = set(doc.split())
            all_tokens.update(tokens)
            for t in tokens:
                doc_freq[t] = doc_freq.get(t, 0) + 1

        # Build vocabulary index
        self.vocabulary = {word: idx for idx, word in enumerate(sorted(all_tokens))}

        # Compute IDF: log((N + 1) / (df + 1)) + 1  (smooth IDF)
        N = len(processed)
        self.idf = {
            word: math.log((N + 1) / (doc_freq.get(word, 0) + 1)) + 1
            for word in self.vocabulary
        }
        self._fitted = True
        logger.info(f"TFIDFVectorizer fitted: {len(self.vocabulary)} terms, {N} documents.")
        return self

    def transform(self, text: str) -> dict[str, float]:
        """
        Convert a single text document into a TF-IDF weighted dict.

        Args:
            text: Raw text string.

        Returns:
            dict mapping vocabulary_word → tfidf_score
        """
        if not self._fitted:
            raise RuntimeError("Call fit() before transform().")

        processed = preprocess_to_string(text)
        tokens    = processed.split()
        tf        = Counter(tokens)
        total     = len(tokens) if tokens else 1

        vector = {}
        for word, idx in self.vocabulary.items():
            if word in tf:
                tfidf = (tf[word] / total) * self.idf.get(word, 1.0)
                vector[word] = tfidf

        return vector

    def fit_transform(self, documents: list[str]) -> list[dict[str, float]]:
        """Convenience: fit then transform all documents."""
        self.fit(documents)
        return [self.transform(d) for d in documents]


# Module-level singleton (re-used across the recommendation engine)
_vectorizer = TFIDFVectorizer()


def get_vectorizer() -> TFIDFVectorizer:
    """Return the shared vectorizer instance."""
    return _vectorizer
