# ============================================================
#  TalentSync — Cosine Similarity
#  cos(θ) = (A · B) / (‖A‖ · ‖B‖)
#  Used to measure text similarity between resume and job.
# ============================================================

import math


def cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """
    Compute cosine similarity between two TF-IDF sparse vectors.

    Both vectors are represented as {term: weight} dicts.

    Returns:
        float in [0, 1] — 1 means identical, 0 means no overlap.
    """
    if not vec_a or not vec_b:
        return 0.0

    # Dot product: sum of (a[word] * b[word]) for words in common
    common_terms = set(vec_a.keys()) & set(vec_b.keys())
    dot_product  = sum(vec_a[t] * vec_b[t] for t in common_terms)

    # Magnitudes
    mag_a = math.sqrt(sum(v * v for v in vec_a.values()))
    mag_b = math.sqrt(sum(v * v for v in vec_b.values()))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot_product / (mag_a * mag_b)


def skill_overlap_score(candidate_skills: list[str], job_skills: list[str]) -> float:
    """
    Simple set-intersection skill match score (fallback when no TF-IDF).

    Formula: |candidate ∩ job| / |job|

    Returns:
        float in [0, 1]
    """
    if not job_skills:
        return 0.0

    cand_lower = {s.lower() for s in candidate_skills}
    job_lower  = {s.lower() for s in job_skills}

    intersection = cand_lower & job_lower
    return len(intersection) / len(job_lower)


def rank_by_similarity(query_vec: dict[str, float],
                        document_vecs: list[tuple[int, dict[str, float]]]) -> list[tuple[int, float]]:
    """
    Rank a list of documents by cosine similarity to a query.

    Args:
        query_vec:     TF-IDF vector for the resume / query.
        document_vecs: List of (doc_id, tfidf_vector) tuples.

    Returns:
        List of (doc_id, similarity_score) sorted descending.
    """
    scores = [
        (doc_id, cosine_similarity(query_vec, doc_vec))
        for doc_id, doc_vec in document_vecs
    ]
    return sorted(scores, key=lambda x: x[1], reverse=True)
