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

# Allowed roles on registration
ALLOWED_ROLES = {'candidate', 'hr'}


def login_user(email: str, password: str) -> dict:
    """Authenticate a user. Returns user dict on success."""
    if not email or not password:
        return {'success': False, 'message': 'Email and password are required.'}

    with get_db() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email.strip().lower(),)
        ).fetchone()

    # Generic message — do not reveal whether the email exists
    if not user:
        return {
            'success': False,
            'message': 'Invalid email or password.'
        }

    # Always use hashed comparison — plain-text passwords are no longer supported
    try:
        is_valid = check_password_hash(user['password'], password)
    except Exception:
        is_valid = False

    if not is_valid:
        return {
            'success': False,
            'message': 'Invalid email or password.'
        }

    logger.info(f"Login successful: {email}")

    u_dict = dict(user)
    # Never return the password hash to the caller
    u_dict.pop('password', None)
    return {'success': True, 'user': u_dict}


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

    # Whitelist roles — prevent privilege escalation via self-assigned role
    if role not in ALLOWED_ROLES:
        return {'success': False, 'message': "Invalid role. Must be 'candidate' or 'hr'."}

    hashed_password = generate_password_hash(password)

    try:
        with get_db() as conn:
            cur = conn.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name.strip(), email.strip().lower(), hashed_password, role)
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
