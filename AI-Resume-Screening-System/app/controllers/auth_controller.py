# ============================================================
#  TalentSync — Auth Controller
#  Business logic for login, register, and notifications.
# ============================================================

import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.connection import get_db
from app.utils.validators import validate_email, validate_password, validate_required_fields
from app.utils.logger import get_logger

logger = get_logger(__name__)


def login_user(email: str, password: str) -> dict:
    """Authenticate a user. Returns user dict on success."""
    if not email or not password:
        return {'success': False, 'message': 'Email and password are required.'}

    with get_db() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email.strip().lower(),)
        ).fetchone()

    if not user:
        return {
            'success': False,
            'message': 'No account found with that email. Demo: hetsony143@gmail.com / priya@demo.com (pass: demo123)'
        }

    # Support backward compatibility with plain text demo passwords
    is_valid = False
    if user['password'] == password:
        is_valid = True
    elif check_password_hash(user['password'], password):
        is_valid = True

    if not is_valid:
        return {
            'success': False,
            'message': 'Incorrect password. Demo: hetsony143@gmail.com / priya@demo.com (pass: demo123)'
        }

    logger.info(f"Login successful: {email}")
    return {'success': True, 'user': dict(user)}


def register_user(name: str, email: str, password: str, role: str) -> dict:
    """Create a new user account."""
    valid, msg = validate_required_fields(
        {'name': name, 'email': email, 'password': password, 'role': role},
        ['name', 'email', 'password', 'role']
    )
    if not valid:
        return {'success': False, 'message': msg}

    if not validate_email(email):
        return {'success': False, 'message': 'Invalid email address.'}

    ok, err = validate_password(password)
    if not ok:
        return {'success': False, 'message': err}

    hashed_password = generate_password_hash(password)

    try:
        with get_db() as conn:
            cur = conn.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email.strip().lower(), hashed_password, role)
            )
            user_id = cur.lastrowid

            # Welcome notification
            conn.execute(
                "INSERT INTO notifications (user_id, title, message, type, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, 'Welcome to TalentSync! 🎉',
                 'Your account is ready. Upload your resume to get started.',
                 'success', datetime.now().strftime('%Y-%m-%d %H:%M'))
            )
            conn.commit()

        logger.info(f"New user registered: {email} ({role})")
        return {
            'success': True,
            'user': {'id': user_id, 'name': name, 'email': email, 'role': role, 'ats_score': 0, 'skills': ''}
        }
    except sqlite3.IntegrityError:
        return {'success': False, 'message': 'Email already registered.'}

