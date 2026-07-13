# ============================================================
#  TalentSync — Application Settings
#  Centralised configuration for all environments
# ============================================================

import os
import secrets
from dotenv import load_dotenv

# Load .env file (only used in development; ignored in production)
load_dotenv()


def _require_secret_key() -> str:
    """
    Returns SECRET_KEY from the environment.
    Generates a secure random key in development but raises an error
    in production if SECRET_KEY is not explicitly set.
    """
    key = os.getenv("SECRET_KEY")
    env = os.getenv("FLASK_ENV", "development").lower()
    if not key:
        if env == "production":
            raise RuntimeError(
                "CRITICAL: SECRET_KEY environment variable is not set. "
                "Set a strong, random SECRET_KEY before running in production."
            )
        # Development: auto-generate a per-process key (sessions reset on restart — acceptable for dev)
        return secrets.token_hex(32)
    return key


class Config:
    """Base configuration — shared by all environments."""

    # ── Application
    APP_NAME    = os.getenv("APP_NAME", "TalentSync")
    APP_VERSION = os.getenv("APP_VERSION", "2.0")
    SECRET_KEY  = _require_secret_key()

    # ── Database (SQLite for now — swap URL for MySQL/PostgreSQL later)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///talentsync.db")
    DB_FILE      = "talentsync.db"

    # ── File Upload
    UPLOAD_FOLDER      = os.getenv("UPLOAD_FOLDER", "app/static/uploads/resumes")
    TEMP_FOLDER        = "app/static/uploads/temp"
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))  # 5 MB
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

    # ── Flask
    DEBUG   = os.getenv("FLASK_ENV", "development") == "development"
    TESTING = False
    PORT    = int(os.getenv("PORT", 5000))

    # ── Session / Cookie Security (OWASP hardening)
    SESSION_COOKIE_HTTPONLY = True    # JS cannot access the session cookie
    SESSION_COOKIE_SAMESITE = "Lax"  # CSRF mitigation
    # NOTE: Set SESSION_COOKIE_SECURE=True in production (requires HTTPS)
    SESSION_COOKIE_SECURE   = os.getenv("FLASK_ENV", "development") == "production"
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours (in seconds)

    # ── ML / NLP
    TFIDF_VECTORIZER_PATH = "trained_models/tfidf_vectorizer.pkl"
    RECOMMENDATION_MODEL  = "trained_models/recommendation_model.pkl"
    CLASSIFIER_MODEL      = "trained_models/classifier.pkl"


class DevelopmentConfig(Config):
    DEBUG   = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG   = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


# Export the active config based on the environment variable
_env = os.getenv("FLASK_ENV", "development").lower()
ActiveConfig = ProductionConfig if _env == "production" else DevelopmentConfig
