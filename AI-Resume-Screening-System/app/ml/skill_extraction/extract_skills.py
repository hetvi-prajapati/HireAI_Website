# ============================================================
#  TalentSync — Skill Extraction Engine
#  Uses regex boundary matching against the skills database.
#  Extensible: swap for spaCy NER when available.
# ============================================================

import re
from app.ml.skill_extraction.skills_db import ALL_SKILLS, SKILL_CATEGORIES, JOB_ROLE_SKILLS
from app.utils.logger import get_logger

logger = get_logger(__name__)


def extract_skills(text: str) -> list[str]:
    """
    Extract all recognisable skills from raw resume text.

    Algorithm:
      For each skill in the master list, use word-boundary regex
      to avoid partial matches (e.g. 'r' inside 'or').

    Args:
        text: Raw (lowercased) resume text.

    Returns:
        List of skill strings in Title Case, sorted alphabetically.
    """
    if not text:
        return []

    text_lower = text.lower()
    found = set()

    for skill in ALL_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill.title())

    result = sorted(found)
    logger.info(f"extract_skills: found {len(result)} skills.")
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
    text_lower = text.lower()
    result = {}

    for category, skills in SKILL_CATEGORIES.items():
        matched = []
        for skill in skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                matched.append(skill.title())
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
