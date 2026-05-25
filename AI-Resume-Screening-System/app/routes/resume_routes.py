# ============================================================
#  TalentSync — Resume Routes  (Blueprint: /api)
# ============================================================

from flask import Blueprint, request, jsonify
from app.controllers.resume_controller import process_resume_upload
from app.database.connection import get_db
from app.ml.recommendation.recommend_jobs import recommend_jobs
from datetime import datetime

resume_bp = Blueprint('resume', __name__, url_prefix='/api')


@resume_bp.route('/upload_resume', methods=['POST'])
def upload_resume():
    """
    POST /api/upload_resume
    Form data: file=<resume>, user_id=<int>
    """
    file    = request.files.get('resume')
    user_id = request.form.get('user_id', type=int)
    result  = process_resume_upload(file, user_id)
    status  = 200 if result['success'] else 400
    return jsonify(result), status


@resume_bp.route('/match_jobs', methods=['POST'])
def match_jobs():
    """
    POST /api/match_jobs
    JSON: { skills: ['Python', 'SQL', ...] }
    """
    data   = request.get_json(force=True) or {}
    skills = data.get('skills', [])

    with get_db() as conn:
        jobs = [dict(j) for j in conn.execute("SELECT * FROM jobs ORDER BY id").fetchall()]

    matched = recommend_jobs(skills, jobs)
    return jsonify({'success': True, 'jobs': matched})


@resume_bp.route('/apply', methods=['POST'])
def apply_job():
    """POST /api/apply  →  { user_id, job_id, match_score }"""
    data    = request.get_json(force=True) or {}
    user_id = data.get('user_id')
    job_id  = data.get('job_id')

    with get_db() as conn:
        exists = conn.execute(
            "SELECT id FROM applications WHERE user_id=? AND job_id=?",
            (user_id, job_id)
        ).fetchone()
        if exists:
            return jsonify({'success': False, 'message': 'Already applied!'})

        conn.execute(
            "INSERT INTO applications (user_id, job_id, match_score, applied_at) VALUES (?, ?, ?, ?)",
            (user_id, job_id, data.get('match_score', 0), datetime.now().strftime('%Y-%m-%d %H:%M'))
        )
        conn.commit()

    return jsonify({'success': True})
