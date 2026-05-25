# ============================================================
#  TalentSync — Application Settings
#  Centralised configuration for all environments
# ============================================================

import os
from dotenv import load_dotenv

# Load .env file (only used in development; ignored in production)
load_dotenv()


class Config:
    """Base configuration — shared by all environments."""

    # ── Application
    APP_NAME       = os.getenv("APP_NAME", "TalentSync")
    APP_VERSION    = os.getenv("APP_VERSION", "2.0")
    SECRET_KEY     = os.getenv("SECRET_KEY", "dev-secret-change-in-prod")

    # ── Database (SQLite for now — swap URL for MySQL/PostgreSQL later)
    DATABASE_URL   = os.getenv("DATABASE_URL", "sqlite:///talentsync.db")
    DB_FILE        = "talentsync.db"

    # ── File Upload
    UPLOAD_FOLDER      = os.getenv("UPLOAD_FOLDER", "app/static/uploads/resumes")
    TEMP_FOLDER        = "app/static/uploads/temp"
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))  # 5 MB
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

    # ── Flask
    DEBUG              = os.getenv("FLASK_ENV", "development") == "development"
    TESTING            = False
    PORT               = int(os.getenv("PORT", 5000))

    # ── ML / NLP
    TFIDF_VECTORIZER_PATH   = "trained_models/tfidf_vectorizer.pkl"
    RECOMMENDATION_MODEL    = "trained_models/recommendation_model.pkl"
    CLASSIFIER_MODEL        = "trained_models/classifier.pkl"


class DevelopmentConfig(Config):
    DEBUG   = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG   = False
    TESTING = False


# Export the active config based on the environment variable
_env = os.getenv("FLASK_ENV", "development").lower()
ActiveConfig = ProductionConfig if _env == "production" else DevelopmentConfig
