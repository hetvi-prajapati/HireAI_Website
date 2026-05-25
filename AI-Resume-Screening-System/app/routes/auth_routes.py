# ============================================================
#  TalentSync — Auth Routes  (Blueprint: /api/auth)
# ============================================================

from flask import Blueprint, request, jsonify, session
from app.controllers.auth_controller import login_user, register_user
from app.database.connection import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """POST /api/auth/login  →  { email, password }"""
    data     = request.get_json(force=True) or {}
    email    = data.get('email', '').strip()
    password = data.get('password', '')
    
    result = login_user(email, password)
    if result.get('success'):
        session['user_id'] = result['user']['id']
    return jsonify(result)


@auth_bp.route('/register', methods=['POST'])
def register():
    """POST /api/auth/register  →  { name, email, password, role }"""
    data = request.get_json(force=True) or {}
    result = register_user(
        data.get('name', ''),
        data.get('email', ''),
        data.get('password', ''),
        data.get('role', 'candidate')
    )
    if result.get('success'):
        session['user_id'] = result['user']['id']
    return jsonify(result)


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """POST /api/auth/logout"""
    session.pop('user_id', None)
    return jsonify({'success': True})


@auth_bp.route('/me', methods=['GET'])
def get_me():
    """GET /api/auth/me"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Not logged in'})
        
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if user:
            u_dict = dict(user)
            # Never return password hash
            if 'password' in u_dict:
                del u_dict['password']
            return jsonify({'success': True, 'user': u_dict})
            
    return jsonify({'success': False, 'message': 'User not found'})


@auth_bp.route('/change_password', methods=['POST'])
def change_password():
    """POST /api/auth/change_password → { current_password, new_password }"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    data = request.get_json(force=True) or {}
    current_pw = data.get('current_password', '')
    new_pw     = data.get('new_password', '')

    if not current_pw or not new_pw:
        return jsonify({'success': False, 'message': 'Both passwords required'}), 400
    if len(new_pw) < 6:
        return jsonify({'success': False, 'message': 'New password must be at least 6 characters'}), 400

    from werkzeug.security import check_password_hash, generate_password_hash
    with get_db() as conn:
        user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        # Support plain-text demo passwords
        is_valid = (user['password'] == current_pw) or \
                   check_password_hash(user['password'], current_pw)
        if not is_valid:
            return jsonify({'success': False, 'message': 'Current password is incorrect'}), 403

        conn.execute('UPDATE users SET password=? WHERE id=?',
                     (generate_password_hash(new_pw), user_id))
        conn.commit()

    return jsonify({'success': True, 'message': 'Password changed successfully!'})


@auth_bp.route('/landing_stats', methods=['GET'])
def landing_stats():
    """GET /api/auth/landing_stats — real numbers for landing page."""
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
