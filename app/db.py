import sqlite3
from pathlib import Path

DB_PATH = Path("app.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
        """
    )
    # Ensure default admin exists
    cursor.execute(
        "INSERT OR IGNORE INTO users (email, password, is_admin) VALUES (?, ?, ?)",
        ("admin@reflex.com", "password123", 1),
    )
    conn.commit()
    conn.close()

