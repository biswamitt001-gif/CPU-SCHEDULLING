"""
SQLite database helper for the CPU Scheduling Simulator.
Stores run history: algorithm name, avg TAT, avg WT.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "scheduler.db")


def init_db():
    """Create the results table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm TEXT    NOT NULL,
            avg_tat   REAL    NOT NULL,
            avg_wt    REAL    NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_result(algorithm: str, avg_tat: float, avg_wt: float):
    """Persist a scheduling run result."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO results (algorithm, avg_tat, avg_wt) VALUES (?, ?, ?)",
        (algorithm, avg_tat, avg_wt),
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 20):
    """Return the last `limit` results from the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT id, algorithm, avg_tat, avg_wt, created_at FROM results ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
