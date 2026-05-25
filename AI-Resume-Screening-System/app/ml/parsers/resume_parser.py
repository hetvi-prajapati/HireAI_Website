# ============================================================
#  TalentSync — Resume Parser (Orchestrator)
#  Decides which parser to use based on file extension,
#  then extracts structured data (skills, email, name, etc.)
#  from the raw text.
# ============================================================

import re
from app.ml.parsers.pdf_parser import extract_text_from_pdf
from app.ml.skill_extraction.extract_skills import extract_skills, extract_skills_with_categories
from app.ml.preprocessing.clean_text import clean_text
from app.utils.logger import get_logger

logger = get_logger(__name__)


# ── Regex patterns for personal info extraction ──────────────

_EMAIL_RE    = re.compile(r'[\w\.\-]+@[\w\-]+\.[a-z]{2,}', re.I)
_PHONE_RE    = re.compile(r'(?:\+91[\-\s]?)?[6-9]\d{9}|(?:\(\d{3}\)\s*|\d{3}[\-\.])\d{3}[\-\.]\d{4}')
_LINKEDIN_RE = re.compile(r'linkedin\.com/in/[\w\-]+', re.I)
_GITHUB_RE   = re.compile(r'github\.com/[\w\-]+', re.I)
_CGPA_RE     = re.compile(r'(?:cgpa|gpa|grade)[:\s]*([0-9]\.[0-9]{1,2})', re.I)

# Education keywords
_DEGREE_KEYWORDS = [
    'b.tech', 'b.e.', 'b.sc', 'bca', 'm.tech', 'm.e.', 'm.sc', 'mca',
    'mba', 'phd', 'bachelor', 'master', 'diploma', 'b.com', 'm.com'
]

# Experience keywords
_EXP_KEYWORDS = ['intern', 'engineer', 'analyst', 'developer', 'scientist', 'manager', 'associate']


def parse_resume(file, filename: str) -> dict:
    """
    Main entry point.
    Accepts a file object and filename, returns a structured dict.

    Returns:
        {
            'raw_text': str,
            'email': str,
            'phone': str,
            'linkedin': str,
            'github': str,
            'cgpa': str,
            'degree': str,
            'skills': list[str],
            'skill_categories': dict,
            'experience_lines': list[str],
        }
    """
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

    # ── Step 1: Extract raw text
    if ext == 'pdf':
        raw_text = extract_text_from_pdf(file)
    else:
        logger.warning(f"Unsupported file type: {ext}. Returning empty parse.")
        return _empty_result()

    if not raw_text.strip():
        logger.warning("Parser returned empty text — file may be image-based.")
        return _empty_result()

    # ── Step 2: Extract structured fields
    result = {
        'raw_text':          raw_text,
        'email':             _extract_email(raw_text),
        'phone':             _extract_phone(raw_text),
        'linkedin':          _extract_linkedin(raw_text),
        'github':            _extract_github(raw_text),
        'cgpa':              _extract_cgpa(raw_text),
        'degree':            _extract_degree(raw_text),
        'skills':            extract_skills(raw_text),
        'skill_categories':  extract_skills_with_categories(raw_text),
        'experience_lines':  _extract_experience(raw_text),
    }

    logger.info(f"Resume parsed: {len(result['skills'])} skills, email={result['email']}")
    return result


# ── Private helper functions ──────────────────────────────────

def _extract_email(text: str) -> str:
    match = _EMAIL_RE.search(text)
    return match.group() if match else ''


def _extract_phone(text: str) -> str:
    match = _PHONE_RE.search(text)
    return match.group() if match else ''


def _extract_linkedin(text: str) -> str:
    match = _LINKEDIN_RE.search(text)
    return match.group() if match else ''


def _extract_github(text: str) -> str:
    match = _GITHUB_RE.search(text)
    return match.group() if match else ''


def _extract_cgpa(text: str) -> str:
    match = _CGPA_RE.search(text)
    return match.group(1) if match else ''


def _extract_degree(text: str) -> str:
    text_lower = text.lower()
    for degree in _DEGREE_KEYWORDS:
        if degree in text_lower:
            return degree.upper()
    return ''


def _extract_experience(text: str) -> list[str]:
    """Return lines that likely describe work experience."""
    lines = text.split('\n')
    exp_lines = []
    for line in lines:
        line = line.strip()
        if any(kw in line.lower() for kw in _EXP_KEYWORDS) and len(line) > 15:
            exp_lines.append(line)
    return exp_lines[:10]   # Return top 10 relevant lines


def _empty_result() -> dict:
    return {
        'raw_text': '', 'email': '', 'phone': '', 'linkedin': '',
        'github': '', 'cgpa': '', 'degree': '', 'skills': [],
        'skill_categories': {}, 'experience_lines': []
    }
