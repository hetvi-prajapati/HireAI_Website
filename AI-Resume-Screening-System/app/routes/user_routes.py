# ============================================================
#  TalentSync — User Routes  (Blueprint: /api)
# ============================================================

from flask import Blueprint, request, jsonify
from app.database.connection import get_db

user_bp = Blueprint('user', __name__, url_prefix='/api')


@user_bp.route('/candidate/stats/<int:user_id>')
def candidate_stats(user_id):
    """GET /api/candidate/stats/<user_id>"""
    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        u    = dict(user)
        apps = conn.execute("SELECT COUNT(*) FROM applications WHERE user_id=?", (user_id,)).fetchone()[0]
        shortlisted = conn.execute(
            "SELECT COUNT(*) FROM applications WHERE user_id=? AND status='Shortlisted'", (user_id,)
        ).fetchone()[0]
        total_jobs = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        skills = [s.strip() for s in (u.get('skills') or '').split(',') if s.strip()]

        # Calculate pseudo-proficiency for skills radar
        # We need top 6 skills for radar chart
        radar_skills = skills[:6]
        if len(radar_skills) < 6:
            radar_skills += ['Problem Solving', 'Communication', 'Teamwork', 'Agile', 'Adaptability', 'Leadership'][:6-len(radar_skills)]
        
        base_score = u.get('ats_score', 0)
        import random
        # deterministic random based on user id and skill string length
        radar_levels = []
        radar_required = []
        for s in radar_skills:
            seed = user_id + len(s)
            random.seed(seed)
            level = min(100, max(40, base_score + random.randint(-15, 15)))
            req = min(100, max(60, base_score + random.randint(5, 20)))
            radar_levels.append(level)
            radar_required.append(req)
            
        # Market trends (ATS dist, Top skills bar, App time)
        # Using similar logic to admin for market overview
        ats_ranges = {'0-20':0, '21-40':0, '41-60':0, '61-70':0, '71-80':0, '81-90':0, '91-100':0}
        all_ats = conn.execute("SELECT ats_score FROM users WHERE role='candidate'").fetchall()
        for row in all_ats:
            s_val = row[0] or 0
            if s_val <= 20: ats_ranges['0-20'] += 1
            elif s_val <= 40: ats_ranges['21-40'] += 1
            elif s_val <= 60: ats_ranges['41-60'] += 1
            elif s_val <= 70: ats_ranges['61-70'] += 1
            elif s_val <= 80: ats_ranges['71-80'] += 1
            elif s_val <= 90: ats_ranges['81-90'] += 1
            else: ats_ranges['91-100'] += 1
            
        # Top skills
        skills_raw = conn.execute("SELECT skills FROM users WHERE role='candidate' AND skills != ''").fetchall()
        skill_counts = {}
        for row in skills_raw:
            for s_val in row[0].split(','):
                s_val = s_val.strip()
                if s_val:
                    skill_counts[s_val] = skill_counts.get(s_val, 0) + 1
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:8]

        import datetime
        now = datetime.datetime.now()
        months = [(now.month - i - 1) % 12 + 1 for i in range(5, -1, -1)]
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        app_time_labels = [month_names[m-1] for m in months]
        app_time_total = [0] * 6
        app_time_shortlisted = [0] * 6
        
        apps_date = conn.execute("SELECT applied_at, status FROM applications").fetchall()
        for row in apps_date:
            date_str, status = row
            try:
                m = int(date_str.split('-')[1])
                if m in months:
                    idx = months.index(m)
                    app_time_total[idx] += 1
                    if status == 'Shortlisted':
                        app_time_shortlisted[idx] += 1
            except:
                pass

        import random
        # deterministic profile views based on ats score
        random.seed(user_id)
        views = max(12, int(base_score * 0.45) + random.randint(-10, 15))
        views_weekly = max(0, int(views * 0.2) + random.randint(-5, 5))

        # calculate missing skills (top skills in market not in candidate's skills)
        candidate_skills_lower = [s.lower() for s in skills]
        missing = []
        for s, _ in top_skills:
            if s.lower() not in candidate_skills_lower:
                missing.append(s)

    return jsonify({
        'ats_score':    u.get('ats_score', 0),
        'skills_count': len(skills),
        'skills':       skills,
        'missing_skills': missing[:4],
        'profile_views': views,
        'profile_views_weekly': views_weekly,
        'skills_count': len(skills),
        'skills':       skills,
        'applications': apps,
        'shortlisted':  shortlisted,
        'job_matches':  total_jobs,
        'radar': {
            'labels': radar_skills,
            'levels': radar_levels,
            'required': radar_required
        },
        'market_trends': {
            'ats_distribution': list(ats_ranges.values()),
            'top_skills': [{'skill': s, 'count': c} for s, c in top_skills],
            'app_time': {
                'labels': app_time_labels,
                'total': app_time_total,
                'shortlisted': app_time_shortlisted
            }
        }
    })


@user_bp.route('/users/<int:user_id>/profile', methods=['GET', 'PUT'])
def user_profile(user_id):
    """GET/PUT /api/users/<user_id>/profile"""
    if request.method == 'GET':
        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        return jsonify(dict(user)) if user else (jsonify({'error': 'Not found'}), 404)

    data = request.get_json(force=True) or {}
    with get_db() as conn:
        conn.execute(
            '''UPDATE users SET name=?, email=?, phone=?, location=?,
               linkedin=?, github=?, summary=?, education=? WHERE id=?''',
            (data.get('name'), data.get('email'), data.get('phone'),
             data.get('location'), data.get('linkedin'), data.get('github'),
             data.get('summary'), data.get('education'), user_id)
        )
        conn.commit()
    return jsonify({'success': True})


@user_bp.route('/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    """GET /api/notifications/<user_id>"""
    with get_db() as conn:
        nots = conn.execute(
            "SELECT * FROM notifications WHERE user_id=? ORDER BY id DESC", (user_id,)
        ).fetchall()
    return jsonify([dict(n) for n in nots])


@user_bp.route('/notifications/<int:user_id>/read', methods=['POST'])
def read_notifications(user_id):
    """POST /api/notifications/<user_id>/read"""
    with get_db() as conn:
        conn.execute("UPDATE notifications SET is_read=1 WHERE user_id=?", (user_id,))
        conn.commit()
    return jsonify({'success': True})
