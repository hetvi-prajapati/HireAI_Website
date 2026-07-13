# ============================================================
#  TalentSync — Resume Routes  (Blueprint: /api)
# ============================================================

from flask import Blueprint, request, jsonify, session
from app.controllers.resume_controller import process_resume_upload
from app.database.connection import get_db
from app.ml.recommendation.recommend_jobs import recommend_jobs
from app.utils.security import login_required
from datetime import datetime

resume_bp = Blueprint('resume', __name__, url_prefix='/api')


@resume_bp.route('/upload_resume', methods=['POST'])
@login_required
def upload_resume():
    """
    POST /api/upload_resume
    Form data: file=<resume>
    user_id is taken from the session — not the request body (prevents IDOR).
    """
    file    = request.files.get('resume')
    # Always use the session user_id — never trust client-supplied user_id
    user_id = session.get('user_id')
    result  = process_resume_upload(file, user_id)
    status  = 200 if result['success'] else 400
    return jsonify(result), status


@resume_bp.route('/match_jobs', methods=['POST'])
@login_required
def match_jobs():
    """
    POST /api/match_jobs
    JSON: { skills: ['Python', 'SQL', ...] }
    """
    data   = request.get_json(silent=True) or {}
    skills = data.get('skills', [])

    # Validate skills is a list
    if not isinstance(skills, list):
        return jsonify({'success': False, 'message': 'skills must be a list'}), 400

    with get_db() as conn:
        jobs = [dict(j) for j in conn.execute("SELECT * FROM jobs ORDER BY id").fetchall()]

    matched = recommend_jobs(skills, jobs)
    return jsonify({'success': True, 'jobs': matched})


@resume_bp.route('/apply', methods=['POST'])
@login_required
def apply_job():
    """POST /api/apply  →  { job_id, match_score }
    user_id is taken from the session — not the request body.
    """
    data    = request.get_json(silent=True) or {}
    # Always use the session user_id — never trust client-supplied user_id
    user_id = session.get('user_id')
    job_id  = data.get('job_id')

    if not job_id:
        return jsonify({'success': False, 'message': 'job_id is required'}), 400

    with get_db() as conn:
        # Verify the job actually exists
        job = conn.execute("SELECT id FROM jobs WHERE id=?", (job_id,)).fetchone()
        if not job:
            return jsonify({'success': False, 'message': 'Job not found'}), 404

        exists = conn.execute(
            "SELECT id FROM applications WHERE user_id=? AND job_id=?",
            (user_id, job_id)
        ).fetchone()
        if exists:
            return jsonify({'success': False, 'message': 'Already applied!'})

        match_score = int(data.get('match_score', 0))
        conn.execute(
            "INSERT INTO applications (user_id, job_id, match_score, applied_at) VALUES (?, ?, ?, ?)",
            (user_id, job_id, match_score, datetime.now().strftime('%Y-%m-%d %H:%M'))
        )
        conn.commit()

    return jsonify({'success': True})
