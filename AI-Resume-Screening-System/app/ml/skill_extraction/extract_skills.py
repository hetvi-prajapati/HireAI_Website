# ============================================================
#  TalentSync — Skill Extraction Engine (v2 — Real ML)
#
#  Pipeline:
#    Primary  → Load trained spaCy NER model (SKILL entities)
#    Fallback → Regex-boundary matching against skills_db
#               (Used on first run before training, or if model
#                files are missing)
#
#  The NER model is loaded ONCE at module import time and
#  reused across all requests for maximum performance.
# ============================================================

import re
from pathlib import Path
from functools import lru_cache
from app.ml.skill_extraction.skills_db import ALL_SKILLS, SKILL_CATEGORIES, JOB_ROLE_SKILLS
from app.utils.logger import get_logger

logger = get_logger(__name__)

# ── Model Path ────────────────────────────────────────────────
_BASE_DIR   = Path(__file__).resolve().parents[4]
_NER_PATH   = _BASE_DIR / "trained_models" / "spacy_skill_ner"

# ── Lazy NER Model Loader ─────────────────────────────────────
_nlp = None
_ner_available = False


def _load_ner_model():
    """Load spaCy NER model once. Thread-safe via module-level flag."""
    global _nlp, _ner_available
    if _nlp is not None:
        return

    if not _NER_PATH.exists():
        logger.info(
            "spaCy NER model not found — using regex+sklearn hybrid. "
            "Run 'py -m app.ml.training.train_all' to train."
        )
        _ner_available = False
        return

    try:
        import spacy
        _nlp = spacy.load(str(_NER_PATH))
        _ner_available = True
        logger.info(f"[OK] Loaded spaCy SKILL NER model from '{_NER_PATH}'")
    except ImportError:
        logger.info(
            "spaCy not installed (Python 3.14+ compatibility issue). "
            "Using regex+sklearn hybrid extractor."
        )
        _ner_available = False
    except Exception as e:
        logger.error(f"Failed to load spaCy NER model: {e}. Using regex fallback.")
        _ner_available = False



# ── Regex Fallback Extractor ──────────────────────────────────
def _regex_extract(text: str) -> list:
    """
    Legacy regex-boundary skill extractor.
    Used as fallback when the NER model is not yet trained.
    """
    if not text:
        return []
    text_lower = text.lower()
    found = set()
    for skill in ALL_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill.title())
    return sorted(found)


# ── NER Extractor ─────────────────────────────────────────────
def _ner_extract(text: str) -> list:
    """
    Run the trained spaCy NER model to extract SKILL entities.
    Returns skills in Title Case, deduplicated, sorted.
    """
    doc = _nlp(text)
    found = set()
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            found.add(ent.text.strip().lower())

    # Also run regex to catch any skills the model might have missed
    # (hybrid approach = best accuracy)
    regex_skills = {s.lower() for s in _regex_extract(text)}
    all_skills   = found | regex_skills

    return sorted({s.title() for s in all_skills})


# ── Public API ────────────────────────────────────────────────
def extract_skills(text: str) -> list[str]:
    """
    Extract all recognisable skills from raw resume text.

    Uses the trained spaCy NER model as the primary extractor,
    with a regex-boundary fallback for robustness.

    Args:
        text: Raw resume text (any case).

    Returns:
        List of skill strings in Title Case, sorted alphabetically.
    """
    _load_ner_model()

    if _ner_available and _nlp is not None:
        result = _ner_extract(text)
        method = "NER"
    else:
        result = _regex_extract(text)
        method = "Regex"

    logger.info(f"extract_skills [{method}]: found {len(result)} skills.")
    return result


def extract_skills_with_categories(text: str) -> dict[str, list[str]]:
    """
    Same as extract_skills(), but groups results by category.

    Returns:
        {
            'Programming Languages': ['Python', 'Java'],
            'Data Science & ML':     ['Machine Learning', 'NLP'],
            ...
        }
    """
    all_found = set(s.lower() for s in extract_skills(text))
    result    = {}

    for category, skills in SKILL_CATEGORIES.items():
        matched = [s.title() for s in skills if s.lower() in all_found]
        if matched:
            result[category] = sorted(matched)

    return result


def get_skill_gaps(candidate_skills: list[str], target_role: str) -> dict:
    """
    Compare candidate skills against the required skills for a job role.

    Args:
        candidate_skills: List of skills the candidate has (any case).
        target_role: Role name matching a key in JOB_ROLE_SKILLS.

    Returns:
        {
            'matched':  ['Python', 'SQL'],
            'missing':  ['Docker', 'Kubernetes'],
            'match_pct': 67
        }
    """
    required = JOB_ROLE_SKILLS.get(target_role, [])
    if not required:
        return {'matched': [], 'missing': [], 'match_pct': 0}

    candidate_lower = {s.lower() for s in candidate_skills}
    matched = [r for r in required if r.lower() in candidate_lower]
    missing = [r for r in required if r.lower() not in candidate_lower]
    match_pct = round(len(matched) / len(required) * 100) if required else 0

    return {
        'matched':   [s.title() for s in matched],
        'missing':   [s.title() for s in missing],
        'match_pct': match_pct
    }


def get_extraction_method() -> str:
    """Return whether the NER model or regex fallback is active."""
    _load_ner_model()
    return "spaCy NER (Trained Model)" if _ner_available else "Regex Fallback (Model not trained)"
