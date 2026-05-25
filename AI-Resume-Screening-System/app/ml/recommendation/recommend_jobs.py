# ============================================================
#  TalentSync — Job Recommendation Engine
#  Content-Based Filtering using TF-IDF + Cosine Similarity
# ============================================================

from app.ml.recommendation.tfidf_model import TFIDFVectorizer
from app.ml.recommendation.cosine_similarity import (
    cosine_similarity, skill_overlap_score, rank_by_similarity
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


def recommend_jobs(candidate_skills: list[str],
                   jobs: list[dict],
                   top_n: int = 10) -> list[dict]:
    """
    Recommend the top N jobs for a candidate using two-stage matching.

    Stage 1 — Skill Overlap Score (fast, interpretable):
        Matches candidate skills directly against job required skills.

    Stage 2 — TF-IDF Cosine Similarity (semantic):
        Vectorises resume skill text and job description together.

    Final score = 70% skill_overlap + 30% cosine_similarity

    Args:
        candidate_skills: Extracted skills from the candidate's resume.
        jobs:             List of job dicts (from DB) with 'skills', 'description'.
        top_n:            Maximum number of recommendations to return.

    Returns:
        List of job dicts with extra keys:
            - 'match_percentage' (int 0-100)
            - 'matched_skills'   (list[str])
            - 'missing_skills'   (list[str])
    """
    if not jobs:
        return []

    candidate_text = ' '.join(candidate_skills)

    # Build corpus: candidate + all job texts
    all_texts = [candidate_text] + [
        f"{j.get('title', '')} {j.get('skills', '')} {j.get('description', '')}"
        for j in jobs
    ]

    # Fit TF-IDF on the full corpus
    vectorizer = TFIDFVectorizer()
    all_vecs   = vectorizer.fit_transform(all_texts)
    cand_vec   = all_vecs[0]
    job_vecs   = [(i, all_vecs[i + 1]) for i in range(len(jobs))]

    # Rank by cosine similarity
    ranked = rank_by_similarity(cand_vec, job_vecs)

    results = []
    for job_idx, cos_score in ranked:
        job = dict(jobs[job_idx])
        job_skills = [s.strip() for s in job.get('skills', '').split(',') if s.strip()]

        # Stage 1: skill overlap
        overlap = skill_overlap_score(candidate_skills, job_skills)

        # Combined final score
        final_score = int((overlap * 0.70 + cos_score * 0.30) * 100)

        if final_score <= 0:
            continue

        # Skill breakdown
        cand_lower = {s.lower() for s in candidate_skills}
        matched = [s for s in job_skills if s.lower() in cand_lower]
        missing = [s for s in job_skills if s.lower() not in cand_lower]

        job['match_percentage'] = min(final_score, 100)
        job['matched_skills']   = matched
        job['missing_skills']   = missing
        results.append(job)

    # Sort by match % and return top N
    results.sort(key=lambda x: x['match_percentage'], reverse=True)
    logger.info(f"recommend_jobs: {len(results)} matches from {len(jobs)} jobs.")
    return results[:top_n]
