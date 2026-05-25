-- ============================================================
--  TalentSync — Database Schema (SQLite)
--  Run once to create all tables.
--  Migrate to MySQL by changing data types (INTEGER→INT, etc.)
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    email       TEXT    UNIQUE NOT NULL,
    password    TEXT    NOT NULL,
    role        TEXT    NOT NULL DEFAULT 'candidate',  -- 'candidate' | 'hr'
    skills      TEXT    DEFAULT '',
    ats_score   INTEGER DEFAULT 0,
    phone       TEXT    DEFAULT '',
    location    TEXT    DEFAULT '',
    linkedin    TEXT    DEFAULT '',
    github      TEXT    DEFAULT '',
    summary     TEXT    DEFAULT '',
    education   TEXT    DEFAULT '',
    created_at  TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS jobs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    company     TEXT    NOT NULL,
    location    TEXT    DEFAULT '',
    type        TEXT    DEFAULT 'Full-time',
    salary      TEXT    DEFAULT '',
    skills      TEXT    DEFAULT '',
    description TEXT    DEFAULT '',
    status      TEXT    DEFAULT 'Active',
    created_at  TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS applications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    job_id      INTEGER NOT NULL,
    match_score INTEGER DEFAULT 0,
    status      TEXT    DEFAULT 'Reviewing',  -- Reviewing|Shortlisted|Pending|Rejected
    applied_at  TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(job_id)  REFERENCES jobs(id)  ON DELETE CASCADE,
    UNIQUE(user_id, job_id)
);

CREATE TABLE IF NOT EXISTS notifications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    title       TEXT    NOT NULL,
    message     TEXT    DEFAULT '',
    type        TEXT    DEFAULT 'info',  -- 'info'|'success'|'error'|'warning'
    is_read     INTEGER DEFAULT 0,
    created_at  TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
