# ============================================================
#  TalentSync — Input Validators
# ============================================================

import re

# Whitelisted application statuses — prevents arbitrary strings in the DB
ALLOWED_STATUSES = {'Shortlisted', 'Reviewing', 'Pending', 'Rejected'}

# Whitelisted user roles — prevents privilege escalation
ALLOWED_ROLES = {'candidate', 'hr'}


def validate_email(email: str) -> bool:
    pattern = r'^[\w\.\-]+@[\w\-]+\.[a-z]{2,}$'
    return bool(re.match(pattern, email.strip(), re.I)) if email else False


def validate_password(password: str) -> tuple:
    """Returns (is_valid, error_message)."""
    if not password:
        return False, "Password is required."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if len(password) > 128:
        return False, "Password must not exceed 128 characters."
    return True, ""


def validate_file_extension(filename: str, allowed: set = None) -> bool:
    if allowed is None:
        allowed = {'pdf', 'doc', 'docx'}
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in allowed


def validate_required_fields(data: dict, required: list) -> tuple:
    """Check that all required keys are present and non-empty."""
    for field in required:
        if not data.get(field):
            return False, f"'{field}' is required."
    return True, ""


def validate_status(status: str) -> bool:
    """Check that a status value is in the allowed whitelist."""
    return status in ALLOWED_STATUSES


def validate_role(role: str) -> bool:
    """Check that a role value is in the allowed whitelist."""
    return role in ALLOWED_ROLES


def sanitize_text(value: str, max_length: int = 1000) -> str:
    """Trim and truncate a text field to prevent oversized payloads."""
    if not value:
        return ''
    return str(value).strip()[:max_length]
