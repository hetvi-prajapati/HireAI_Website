# ============================================================
#  TalentSync — ML Pipeline Orchestrator
#
#  Single entry point for the full ML inference pipeline:
#    1. Parse raw resume PDF → extract text
#    2. Preprocess text (clean, tokenize)
#    3. Extract skills (spaCy NER + regex hybrid)
#    4. Compute ATS score (section-based heuristic)
#    5. Recommend matching jobs (sklearn TF-IDF + skill overlap)
#    6. Generate skill gap report for each recommended job
#
#  All components are stateless and thread-safe.
#  Models are loaded lazily on first inference call.
# ============================================================

import time
from app.ml.preprocessing.clean_text import preprocess_to_string
from app.ml.skill_extraction.extract_skills import (
    extract_skills, extract_skills_with_categories,
    get_skill_gaps, get_extraction_method
)
from app.ml.recommendation.recommend_jobs import recommend_jobs
from app.ml.recommendation.tfidf_model    import get_model_info
from app.ml.ats.ats_checker               import compute_ats_score
from app.utils.logger import get_logger

logger = get_logger(__name__)


def run_full_pipeline(resume_text: str,
                      jobs: list[dict],
                      top_n: int = 10) -> dict:
    """
    Run the complete TalentSync ML inference pipeline.

    Args:
        resume_text: Raw text extracted from the candidate's resume PDF.
        jobs:        List of job dicts from the database.
        top_n:       Maximum recommended jobs to return.

    Returns:
        {
            'skills':           list[str]        — all detected skills
            'skills_by_cat':    dict[str, list]  — skills grouped by category
            'ats':              dict             — ATS score + breakdown
            'recommendations':  list[dict]       — ranked job matches
            'pipeline_meta':    dict             — timing + model info
        }
    """
    t_start = time.time()
    logger.info("ML Pipeline: Starting full inference...")

    # ── Stage 1: Preprocess ───────────────────────────────────
    t1 = time.time()
    cleaned_text = preprocess_to_string(resume_text)
    t_preprocess = round(time.time() - t1, 4)

    # ── Stage 2: Skill Extraction ─────────────────────────────
    t2 = time.time()
    skills         = extract_skills(resume_text)          # pass raw text to NER
    skills_by_cat  = extract_skills_with_categories(resume_text)
    t_extraction   = round(time.time() - t2, 4)

    # ── Stage 3: ATS Scoring ──────────────────────────────────
    t3 = time.time()
    # Extract required skills from all jobs for keyword boost
    all_job_skills = list({
        s.strip() for j in jobs
        for s in j.get('skills', '').split(',') if s.strip()
    })
    ats_result = compute_ats_score(resume_text, job_skills=all_job_skills)
    t_ats      = round(time.time() - t3, 4)

    # ── Stage 4: Job Recommendations ─────────────────────────
    t4 = time.time()
    recommendations = recommend_jobs(
        candidate_skills=skills,
        jobs=jobs,
        top_n=top_n,
        candidate_resume_text=resume_text
    )
    t_recommend = round(time.time() - t4, 4)

    # ── Stage 5: Skill Gap Reports ────────────────────────────
    for rec in recommendations:
        role = rec.get('title', rec.get('role', ''))
        gaps = get_skill_gaps(skills, role)
        rec['skill_gap'] = gaps

    t_total = round(time.time() - t_start, 4)

    logger.info(
        f"ML Pipeline done in {t_total}s | "
        f"Skills: {len(skills)} | "
        f"ATS: {ats_result['score']}/100 | "
        f"Recommendations: {len(recommendations)}"
    )

    return {
        'skills':          skills,
        'skills_by_cat':   skills_by_cat,
        'ats':             ats_result,
        'recommendations': recommendations,
        'pipeline_meta': {
            'total_time_s':      t_total,
            'preprocess_time_s': t_preprocess,
            'extraction_time_s': t_extraction,
            'ats_time_s':        t_ats,
            'recommend_time_s':  t_recommend,
            'extraction_method': get_extraction_method(),
            'tfidf_model':       get_model_info(),
            'skills_count':      len(skills),
        }
    }


def get_pipeline_status() -> dict:
    """
    Return the current status of all ML models.

    Useful for the /api/ml/status health-check endpoint.
    """
    from pathlib import Path
    import json

    base = Path(__file__).resolve().parents[3]

    ner_path   = base / "trained_models" / "spacy_skill_ner"
    tfidf_path = base / "trained_models" / "tfidf_recommender" / "tfidf_vectorizer.pkl"
    dataset    = base / "datasets" / "metadata.json"

    ner_trained   = ner_path.exists()
    tfidf_trained = tfidf_path.exists()

    # Load training history if available
    ner_history = {}
    if (ner_path / "training_history.json").exists():
        with open(ner_path / "training_history.json") as f:
            ner_history = json.load(f)

    tfidf_meta = {}
    if (tfidf_path.parent / "metadata.json").exists():
        with open(tfidf_path.parent / "metadata.json") as f:
            tfidf_meta = json.load(f)

    dataset_meta = {}
    if dataset.exists():
        with open(dataset) as f:
            dataset_meta = json.load(f)

    return {
        "status": "ready" if (ner_trained and tfidf_trained) else "not_trained",
        "models": {
            "spacy_ner": {
                "trained":    ner_trained,
                "path":       str(ner_path),
                "best_f1":    ner_history.get("best_f1"),
                "epochs":     ner_history.get("epochs"),
            },
            "tfidf_recommender": {
                "trained":     tfidf_trained,
                "path":        str(tfidf_path),
                "vocab_size":  tfidf_meta.get("vocab_size"),
                "hit_rate":    tfidf_meta.get("evaluation"),
                "corpus_size": tfidf_meta.get("corpus_size"),
            },
        },
        "dataset": dataset_meta,
        "extraction_method": get_extraction_method(),
    }
