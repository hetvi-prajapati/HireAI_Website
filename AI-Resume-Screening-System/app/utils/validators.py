# ============================================================
#  TalentSync — Input Validators
# ============================================================

import re


def validate_email(email: str) -> bool:
    pattern = r'^[\w\.\-]+@[\w\-]+\.[a-z]{2,}$'
    return bool(re.match(pattern, email.strip(), re.I)) if email else False


def validate_password(password: str) -> tuple[bool, str]:
    """Returns (is_valid, error_message)."""
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters."
    return True, ""


def validate_file_extension(filename: str, allowed: set = None) -> bool:
    if allowed is None:
        allowed = {'pdf', 'doc', 'docx'}
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in allowed


def validate_required_fields(data: dict, required: list[str]) -> tuple[bool, str]:
    """Check that all required keys are present and non-empty."""
    for field in required:
        if not data.get(field):
            return False, f"'{field}' is required."
    return True, ""
