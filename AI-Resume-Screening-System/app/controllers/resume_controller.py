# ============================================================
#  TalentSync — Resume Controller
#  Orchestrates: file upload → parse → ATS score → DB save
# ============================================================

import os
from datetime import datetime
from werkzeug.utils import secure_filename
from app.ml.parsers.resume_parser import parse_resume
from app.ml.ats.ats_checker import compute_ats_score
from app.database.connection import get_db
from app.utils.validators import validate_file_extension
from app.utils.logger import get_logger
from app.config.settings import ActiveConfig

logger = get_logger(__name__)


def process_resume_upload(file, user_id: int | None = None) -> dict:
    """
    Full resume processing pipeline:
      1. Validate file
      2. Parse text + extract structured data
      3. Compute ATS score
      4. Update user record in DB (if user_id provided)

    Returns:
        {
            'success':    bool,
            'message':    str,
            'data': {
                'skills':       list[str],
                'ats_score':    int,
                'ats_grade':    str,
                'suggestions':  list[str],
                'breakdown':    dict,
                'email':        str,
                'phone':        str,
                'linkedin':     str,
                'github':       str,
            }
        }
    """
    if file is None or file.filename == '':
        return {'success': False, 'message': 'No file selected.'}

    filename = secure_filename(file.filename)

    if not validate_file_extension(filename):
        return {'success': False, 'message': 'Only PDF, DOC, and DOCX files are allowed.'}

    # ── Parse resume
    parsed = parse_resume(file, filename)

    if not parsed['raw_text']:
        return {
            'success': False,
            'message': 'Could not extract text. Make sure the PDF is text-based (not a scanned image).'
        }

    # ── ATS scoring
    ats_result = compute_ats_score(parsed['raw_text'])
    ats_score  = ats_result['score']

    # ── Save to DB
    if user_id:
        skills_str = ','.join(parsed['skills'])
        with get_db() as conn:
            conn.execute(
                "UPDATE users SET skills=?, ats_score=? WHERE id=?",
                (skills_str, ats_score, user_id)
            )
            conn.commit()
        logger.info(f"Resume saved for user_id={user_id}: score={ats_score}, skills={len(parsed['skills'])}")

    return {
        'success': True,
        'message': 'Resume parsed and analysed successfully.',
        'data': {
            'skills':      parsed['skills'],
            'ats_score':   ats_score,
            'ats_grade':   ats_result['grade'],
            'suggestions': ats_result['suggestions'],
            'breakdown':   ats_result['breakdown'],
            'email':       parsed['email'],
            'phone':       parsed['phone'],
            'linkedin':    parsed['linkedin'],
            'github':      parsed['github'],
            'degree':      parsed['degree'],
            'skill_categories': parsed['skill_categories'],
        }
    }
