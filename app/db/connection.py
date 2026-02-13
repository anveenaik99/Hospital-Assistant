"""Database connection management."""
import sqlite3
import os
from contextlib import contextmanager
from typing import Generator


DB_PATH = os.getenv("DB_PATH", "data/app.db")


def get_connection() -> sqlite3.Connection:
    """Get a database connection with row factory enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_cursor() -> Generator[sqlite3.Cursor, None, None]:
    """Context manager for database operations."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
