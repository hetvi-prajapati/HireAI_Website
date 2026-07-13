# ============================================================
#  TalentSync — Auth Routes  (Blueprint: /api/auth)
# ============================================================

from flask import Blueprint, request, jsonify, session
from app.controllers.auth_controller import login_user, register_user
from app.database.connection import get_db
from app.utils.security import login_required
from app import limiter

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """POST /api/auth/login  →  { email, password }"""
    data     = request.get_json(silent=True) or {}
    email    = data.get('email', '').strip()
    password = data.get('password', '')

    result = login_user(email, password)
    if result.get('success'):
        session.clear()  # Regenerate session on login (session fixation prevention)
        session['user_id'] = result['user']['id']
    return jsonify(result)


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """POST /api/auth/register  →  { name, email, password, role }"""
    data = request.get_json(silent=True) or {}
    result = register_user(
        data.get('name', ''),
        data.get('email', ''),
        data.get('password', ''),
        data.get('role', 'candidate')
    )
    if result.get('success'):
        session.clear()
        session['user_id'] = result['user']['id']
    return jsonify(result)


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """POST /api/auth/logout"""
    session.clear()  # Clear entire session, not just user_id
    return jsonify({'success': True})


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_me():
    """GET /api/auth/me"""
    user_id = session.get('user_id')
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if user:
            u_dict = dict(user)
            u_dict.pop('password', None)  # Never return password hash
            return jsonify({'success': True, 'user': u_dict})
    return jsonify({'success': False, 'message': 'User not found'}), 404


@auth_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """POST /api/auth/change_password → { current_password, new_password }"""
    user_id = session.get('user_id')

    data       = request.get_json(silent=True) or {}
    current_pw = data.get('current_password', '')
    new_pw     = data.get('new_password', '')

    if not current_pw or not new_pw:
        return jsonify({'success': False, 'message': 'Both passwords required'}), 400
    if len(new_pw) < 8:
        return jsonify({'success': False, 'message': 'New password must be at least 8 characters'}), 400
    if len(new_pw) > 128:
        return jsonify({'success': False, 'message': 'Password must not exceed 128 characters'}), 400

    from werkzeug.security import check_password_hash, generate_password_hash
    with get_db() as conn:
        user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        # Only hash-based comparison — no plaintext fallback
        try:
            is_valid = check_password_hash(user['password'], current_pw)
        except Exception:
            is_valid = False

        if not is_valid:
            return jsonify({'success': False, 'message': 'Current password is incorrect'}), 403

        conn.execute('UPDATE users SET password=? WHERE id=?',
                     (generate_password_hash(new_pw), user_id))
        conn.commit()

    # Invalidate session after password change — force re-login
    session.clear()
    return jsonify({'success': True, 'message': 'Password changed successfully! Please log in again.'})


@auth_bp.route('/landing_stats', methods=['GET'])
def landing_stats():
    """GET /api/auth/landing_stats — public stats for the landing page (no auth needed)."""
    with get_db() as conn:
        total_candidates = conn.execute("SELECT COUNT(*) FROM users WHERE role='candidate'").fetchone()[0]
        total_jobs       = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        total_apps       = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        avg_row          = conn.execute("SELECT AVG(ats_score) FROM users WHERE role='candidate' AND ats_score>0").fetchone()[0]
        avg_ats          = round(avg_row, 0) if avg_row else 0
    return jsonify({
        'resumes_analyzed': total_candidates,
        'jobs_matched':     total_jobs,
        'applications':     total_apps,
        'avg_ats':          int(avg_ats)
    })


@auth_bp.route('/forgot_password', methods=['POST'])
@limiter.limit("3 per minute")
def forgot_password():
    """
    POST /api/auth/forgot_password  →  { email }
    Always returns the same response to prevent email enumeration.
    """
    data  = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'success': False, 'message': 'Email address is required.'}), 400

    # Check DB but return identical response whether email exists or not
    # This prevents attackers from enumerating valid email addresses
    with get_db() as conn:
        conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()

    # In production: send a real password reset email here via SMTP / SendGrid etc.
    return jsonify({
        'success': True,
        'message': 'If an account with that email exists, a reset link has been sent.'
    })
