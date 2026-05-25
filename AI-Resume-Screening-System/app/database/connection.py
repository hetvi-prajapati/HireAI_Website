# ============================================================
#  TalentSync — Database Connection Manager
#  Provides get_db() helper — returns a SQLite connection
#  with Row factory so columns are accessible by name.
# ============================================================

import sqlite3
import os
from app.config.settings import ActiveConfig


def get_db() -> sqlite3.Connection:
    """
    Open and return a fresh SQLite connection.
    Uses row_factory = sqlite3.Row so results act like dicts.
    Always close the connection after use (use as context manager).
    """
    conn = sqlite3.connect(ActiveConfig.DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query: str, params: tuple = ()) -> list[dict]:
    """
    Utility: run a SELECT query and return list of dicts.
    Use for simple read-only queries.
    """
    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]


def execute_write(query: str, params: tuple = ()) -> int:
    """
    Utility: run an INSERT / UPDATE / DELETE.
    Returns the lastrowid (useful for INSERT).
    """
    with get_db() as conn:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.lastrowid
