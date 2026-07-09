# ============================================================
#  TalentSync — Application Factory  (app/__init__.py)
#  Creates and configures the Flask app, registers Blueprints,
#  initialises the database, and creates upload directories.
# ============================================================

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template

from app.config.settings import ActiveConfig


def create_app(config=None) -> Flask:
    """
    Flask Application Factory.
    Call this function to create a configured Flask instance.
    """
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )

    # ── Load configuration
    app.config.from_object(config or ActiveConfig)
    app.secret_key = ActiveConfig.SECRET_KEY

    # ── Ensure upload directories exist
    os.makedirs(ActiveConfig.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(ActiveConfig.TEMP_FOLDER,   exist_ok=True)

    # ── Register Blueprints
    from app.routes.auth_routes   import auth_bp
    from app.routes.resume_routes import resume_bp
    from app.routes.user_routes   import user_bp
    from app.routes.admin_routes  import admin_bp
    from app.routes.ml_routes     import ml_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(ml_bp)

    # ── Landing page route
    @app.route('/')
    def index():
        return render_template('index.html')

    # ── Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/404.html'), 500

    # ── Initialise database on first run
    _init_db(ActiveConfig.DB_FILE)

    return app


# ── Database bootstrap ─────────────────────────────────────

def _init_db(db_file: str):
    """Create all tables and seed demo data if the DB is empty."""
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')

    with sqlite3.connect(db_file) as conn:
        # Create tables from schema file
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
        else:
            _create_tables_inline(conn)

        _seed_demo_data(conn)
        conn.commit()


def _create_tables_inline(conn):
    """Fallback: create tables without the schema.sql file."""
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT UNIQUE, password TEXT, role TEXT,
            skills TEXT DEFAULT '', ats_score INTEGER DEFAULT 0,
            phone TEXT DEFAULT '', location TEXT DEFAULT '',
            linkedin TEXT DEFAULT '', github TEXT DEFAULT '',
            summary TEXT DEFAULT '', education TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, company TEXT, location TEXT, type TEXT, salary TEXT,
            skills TEXT, description TEXT, status TEXT DEFAULT 'Active',
            created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, job_id INTEGER,
            match_score INTEGER DEFAULT 0, status TEXT DEFAULT 'Reviewing',
            applied_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(job_id)  REFERENCES jobs(id),
            UNIQUE(user_id, job_id)
        );
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, title TEXT, message TEXT, type TEXT,
            is_read INTEGER DEFAULT 0, created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')


def _seed_demo_data(conn):
    """Insert demo users, jobs and applications if tables are empty."""
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        return   # Already seeded

    demo_users = [
        ('Rahul Sharma',  'rahul@demo.com',   'demo123', 'candidate', 'Python,SQL,Machine Learning,Pandas,Tableau,Flask,Git', 78),
        ('Priya Mehta',   'priya@demo.com',   'demo123', 'hr',        '', 0),
        ('Preethi Nair',  'preethi@demo.com', 'demo123', 'candidate', 'Python,TensorFlow,Machine Learning,NLP,Keras,NumPy,Git', 91),
        ('Aakash Patel',  'aakash@demo.com',  'demo123', 'candidate', 'Excel,SQL,Power BI,Tableau', 62),
        ('Sneha Reddy',   'sneha@demo.com',   'demo123', 'candidate', 'Python,Machine Learning,Pandas,Scikit-Learn,Data Science', 88),
        ('Manav Joshi',   'manav@demo.com',   'demo123', 'candidate', 'Java,C++,Docker,Kubernetes', 45),
        ('Ananya Singh',  'ananya@demo.com',  'demo123', 'candidate', 'Python,Keras,NLP,Deep Learning,TensorFlow,PyTorch', 84),
        ('Rohan Kapoor',  'rohan@demo.com',   'demo123', 'candidate', 'Python,Machine Learning,R,SQL,Pandas', 71),
        ('Divya Menon',   'divya@demo.com',   'demo123', 'candidate', 'SQL,Tableau,Excel,Power BI,Data Science', 79),
        ('Kiran Desai',   'kiran@demo.com',   'demo123', 'candidate', 'Python,AWS,Docker,Flask,PostgreSQL', 82),
        ('Meera Iyer',    'meera@demo.com',   'demo123', 'candidate', 'React,JavaScript,Node.js,MongoDB,HTML,CSS', 76),
        ('Arjun Verma',   'arjun@demo.com',   'demo123', 'candidate', 'Python,Spark,Hadoop,SQL,AWS,Machine Learning', 85),
    ]
    conn.executemany(
        "INSERT INTO users (name,email,password,role,skills,ats_score) VALUES (?,?,?,?,?,?)",
        demo_users
    )

    now = datetime.now().strftime('%Y-%m-%d')
    seed_jobs = [
        ('Data Scientist',   'TechCorp India',  'Bangalore', 'Full-time', '12-18 LPA',  'Python,Machine Learning,Pandas,SQL,Tableau',       'Senior DS role for AI team.',      'Active',  now),
        ('ML Engineer',      'AI Nexus',        'Mumbai',    'Full-time', '15-22 LPA',  'Python,TensorFlow,PyTorch,Docker,Deep Learning',   'Build ML pipelines at scale.',     'Active',  now),
        ('Data Analyst',     'FinPulse',        'Remote',    'Contract',  '8-12 LPA',   'SQL,Excel,Tableau,Power BI,Data Science',          'Analyze financial data.',          'Active',  now),
        ('Python Developer', 'CloudSoft',       'Ahmedabad', 'Full-time', '6-10 LPA',   'Python,Django,Flask,PostgreSQL,Git',               'Backend Python developer needed.', 'Active',  now),
        ('AI Researcher',    'DeepThink Labs',  'Hyderabad', 'Full-time', '20-30 LPA',  'Python,Machine Learning,NLP,Deep Learning,PyTorch','Research in NLP/CV.',              'Active',  now),
        ('Business Analyst', 'AnalytIQ',        'Chennai',   'Full-time', '7-12 LPA',   'SQL,Excel,Power BI,Tableau,Data Science',          'Drive data-driven decisions.',     'Active',  now),
        ('Data Engineer',    'DataBridge',      'Pune',      'Full-time', '10-16 LPA',  'Python,SQL,Spark,Hadoop,AWS,Docker',               'Build robust data pipelines.',     'Active',  now),
        ('Cloud Architect',  'SkyScale',        'Bangalore', 'Full-time', '25-35 LPA',  'AWS,Azure,Docker,Kubernetes,Python,Terraform',     'Design cloud infrastructure.',     'Active',  now),
        ('NLP Engineer',     'LangAI',          'Remote',    'Full-time', '18-26 LPA',  'Python,NLP,TensorFlow,PyTorch,Deep Learning',      'Work on language models.',         'Active',  now),
        ('Frontend Dev',     'UIWorks',         'Delhi',     'Full-time', '6-11 LPA',   'React,JavaScript,HTML,CSS,Node.js',                'Build stunning UIs.',              'Closing', now),
    ]
    conn.executemany(
        "INSERT INTO jobs (title,company,location,type,salary,skills,description,status,created_at) VALUES (?,?,?,?,?,?,?,?,?)",
        seed_jobs
    )

    apps = [
        (1,1,82,'Reviewing','2026-05-18 10:00'), (1,2,68,'Reviewing','2026-05-17 09:30'),
        (3,2,95,'Shortlisted','2026-05-18 08:00'), (3,5,88,'Shortlisted','2026-05-17 11:00'),
        (4,3,65,'Pending','2026-05-16 14:00'),   (4,6,58,'Pending','2026-05-15 13:00'),
        (5,1,91,'Shortlisted','2026-05-18 07:00'), (5,2,84,'Reviewing','2026-05-17 10:30'),
        (6,4,41,'Rejected','2026-05-14 09:00'),  (7,2,87,'Shortlisted','2026-05-18 06:30'),
        (7,5,79,'Reviewing','2026-05-17 08:00'), (8,1,76,'Reviewing','2026-05-16 10:00'),
        (9,3,80,'Reviewing','2026-05-18 05:00'), (9,6,75,'Shortlisted','2026-05-17 07:00'),
        (10,7,83,'Shortlisted','2026-05-18 04:00'), (11,10,76,'Reviewing','2026-05-16 08:00'),
        (12,1,85,'Shortlisted','2026-05-18 03:00'), (12,7,88,'Reviewing','2026-05-17 05:00'),
    ]
    conn.executemany(
        "INSERT INTO applications (user_id,job_id,match_score,status,applied_at) VALUES (?,?,?,?,?)",
        apps
    )
