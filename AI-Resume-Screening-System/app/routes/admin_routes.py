# ============================================================
#  TalentSync — Admin Routes  (Blueprint: /api/admin)
# ============================================================

from flask import Blueprint, request, jsonify
from app.database.connection import get_db
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/stats')
def admin_stats():
    """GET /api/admin/stats — Dashboard KPIs and chart data."""
    with get_db() as conn:
        # Only count applications that have a REAL matching user (excludes old seeded fake data)
        total       = conn.execute("""
            SELECT COUNT(*) FROM applications a
            INNER JOIN users u ON a.user_id = u.id
            WHERE u.role = 'candidate'
        """).fetchone()[0]
        shortlisted = conn.execute("""
            SELECT COUNT(*) FROM applications a
            INNER JOIN users u ON a.user_id = u.id
            WHERE u.role = 'candidate' AND a.status='Shortlisted'
        """).fetchone()[0]
        reviewing   = conn.execute("""
            SELECT COUNT(*) FROM applications a
            INNER JOIN users u ON a.user_id = u.id
            WHERE u.role = 'candidate' AND a.status='Reviewing'
        """).fetchone()[0]
        pending     = conn.execute("""
            SELECT COUNT(*) FROM applications a
            INNER JOIN users u ON a.user_id = u.id
            WHERE u.role = 'candidate' AND a.status='Pending'
        """).fetchone()[0]
        rejected    = conn.execute("""
            SELECT COUNT(*) FROM applications a
            INNER JOIN users u ON a.user_id = u.id
            WHERE u.role = 'candidate' AND a.status='Rejected'
        """).fetchone()[0]
        active_jobs = conn.execute("SELECT COUNT(*) FROM jobs WHERE status='Active'").fetchone()[0]
        total_jobs  = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        total_cands = conn.execute("SELECT COUNT(*) FROM users WHERE role='candidate'").fetchone()[0]
        avg_row     = conn.execute("SELECT AVG(ats_score) FROM users WHERE role='candidate' AND ats_score>0").fetchone()[0]
        avg_ats     = round(avg_row, 1) if avg_row else 0
        analyzed    = conn.execute("SELECT COUNT(*) FROM users WHERE role='candidate' AND ats_score>0").fetchone()[0]

        # Skills distribution
        skills_raw   = conn.execute("SELECT skills FROM users WHERE role='candidate' AND skills != ''").fetchall()
        skill_counts: dict[str, int] = {}
        for row in skills_raw:
            for s in row[0].split(','):
                s = s.strip()
                if s:
                    skill_counts[s] = skill_counts.get(s, 0) + 1
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:8]

        # Applications by job role (only real users)
        role_data = conn.execute('''
            SELECT j.title, COUNT(*) as cnt FROM applications a
            INNER JOIN users u ON a.user_id = u.id
            JOIN jobs j ON a.job_id = j.id
            WHERE u.role = 'candidate'
            GROUP BY j.title ORDER BY cnt DESC LIMIT 6
        ''').fetchall()

        # ATS Distribution
        # 0-20, 21-40, 41-60, 61-70, 71-80, 81-90, 91-100
        ats_ranges = {'0-20':0, '21-40':0, '41-60':0, '61-70':0, '71-80':0, '81-90':0, '91-100':0}
        all_ats = conn.execute("SELECT ats_score FROM users WHERE role='candidate'").fetchall()
        for row in all_ats:
            s = row[0] or 0
            if s <= 20: ats_ranges['0-20'] += 1
            elif s <= 40: ats_ranges['21-40'] += 1
            elif s <= 60: ats_ranges['41-60'] += 1
            elif s <= 70: ats_ranges['61-70'] += 1
            elif s <= 80: ats_ranges['71-80'] += 1
            elif s <= 90: ats_ranges['81-90'] += 1
            else: ats_ranges['91-100'] += 1
            
        # Applications over time (only real users)
        import datetime
        now = datetime.datetime.now()
        months = [(now.month - i - 1) % 12 + 1 for i in range(5, -1, -1)]
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        app_time_labels = [month_names[m-1] for m in months]
        app_time_total = [0] * 6
        app_time_shortlisted = [0] * 6
        
        apps_date = conn.execute("""
            SELECT a.applied_at, a.status FROM applications a
            INNER JOIN users u ON a.user_id = u.id
            WHERE u.role = 'candidate'
        """).fetchall()
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

    return jsonify({
        'total_applicants':  total,
        'shortlisted':       shortlisted,
        'reviewing':         reviewing,
        'pending':           pending,
        'rejected':          rejected,
        'active_jobs':       active_jobs,
        'total_jobs':        total_jobs,
        'total_candidates':  total_cands,
        'avg_ats_score':     avg_ats,
        'resumes_analyzed':  analyzed,
        'top_skills':        [{'skill': s, 'count': c} for s, c in top_skills],
        'top_skill_demanded': top_skills[0][0] if top_skills else 'Python',
        'acceptance_rate':   round((shortlisted / total * 100), 1) if total > 0 else 0,
        'status_breakdown':  {'Shortlisted': shortlisted, 'Reviewing': reviewing, 'Pending': pending, 'Rejected': rejected},
        'apps_by_role':      [{'role': r[0], 'count': r[1]} for r in role_data],
        'ats_distribution':  list(ats_ranges.values()),
        'app_time': {
            'labels': app_time_labels,
            'total': app_time_total,
            'shortlisted': app_time_shortlisted
        }
    })


@admin_bp.route('/candidates')
def get_candidates():
    """GET /api/admin/candidates — All applicants with match scores."""
    with get_db() as conn:
        rows = conn.execute('''
            SELECT a.id as app_id, u.name, u.email, u.skills, u.ats_score,
                   j.title as job, a.match_score, a.status, a.applied_at
            FROM applications a
            JOIN users u ON a.user_id = u.id
            JOIN jobs j  ON a.job_id  = j.id
            ORDER BY a.match_score DESC
        ''').fetchall()
    return jsonify([dict(r) for r in rows])


@admin_bp.route('/update_status', methods=['POST'])
def update_status():
    """POST /api/admin/update_status  →  { user_id, status }"""
    data    = request.get_json(force=True) or {}
    app_id  = data.get('app_id')
    status  = data.get('status')

    if not app_id or not status:
        return jsonify({'success': False, 'message': 'app_id and status required'}), 400

    with get_db() as conn:
        # Get the user_id from the application
        app_row = conn.execute('SELECT user_id FROM applications WHERE id=?', (app_id,)).fetchone()
        if not app_row:
            return jsonify({'success': False, 'message': 'Application not found'}), 404
        user_id = app_row['user_id']

        conn.execute('UPDATE applications SET status=? WHERE id=?', (status, app_id))
        msg   = f'Your application status has been updated to: {status}'
        ntype = 'success' if status == 'Shortlisted' else ('error' if status == 'Rejected' else 'info')
        conn.execute(
            'INSERT INTO notifications (user_id, title, message, type, created_at) VALUES (?, ?, ?, ?, ?)',
            (user_id, 'Application Status Updated', msg, ntype, datetime.now().strftime('%Y-%m-%d %H:%M'))
        )
        conn.commit()
    return jsonify({'success': True})


@admin_bp.route('/delete_job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """DELETE /api/admin/delete_job/<job_id>"""
    with get_db() as conn:
        conn.execute("DELETE FROM jobs WHERE id=?", (job_id,))
        conn.commit()
    return jsonify({'success': True})


# ── Jobs CRUD ─────────────────────────────────────────────
@admin_bp.route('/jobs', methods=['GET', 'POST'])
def jobs_api():
    if request.method == 'GET':
        with get_db() as conn:
            jobs = conn.execute('SELECT * FROM jobs ORDER BY id DESC').fetchall()
        return jsonify([dict(j) for j in jobs])

    data = request.get_json(force=True) or {}
    with get_db() as conn:
        conn.execute(
            'INSERT INTO jobs (title, company, location, type, salary, skills, description, status, created_at) VALUES (?,?,?,?,?,?,?,?,?)',
            (data.get('title'), data.get('company'), data.get('location'), data.get('type','Full-time'),
             data.get('salary'), data.get('skills'), data.get('description'), 'Active', datetime.now().strftime('%Y-%m-%d'))
        )
        conn.commit()
    return jsonify({'success': True})


@admin_bp.route('/jobs/<int:job_id>', methods=['PUT', 'GET'])
def job_detail(job_id):
    if request.method == 'GET':
        with get_db() as conn:
            job = conn.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
        return jsonify(dict(job)) if job else (jsonify({'error': 'Not found'}), 404)

    data = request.get_json(force=True) or {}
    with get_db() as conn:
        conn.execute(
            'UPDATE jobs SET title=?, company=?, location=?, type=?, salary=?, skills=?, description=? WHERE id=?',
            (data.get('title'), data.get('company'), data.get('location'), data.get('type'),
             data.get('salary'), data.get('skills'), data.get('description'), job_id)
        )
        conn.commit()
    return jsonify({'success': True})
