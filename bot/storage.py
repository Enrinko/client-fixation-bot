"""SQLite-backed lead storage.

Duplicate protection lives in the database itself: a UNIQUE constraint on
client_phone makes the check-and-insert atomic, so a race between two updates
cannot create two leads for the same client.
"""

import sqlite3
from pathlib import Path


class DuplicateClientError(Exception):
    """The client phone is already registered."""


class LeadStorage:
    def __init__(self, db_path: str | Path) -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_phone TEXT NOT NULL UNIQUE,
                realtor_phone TEXT NOT NULL,
                client_name TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        self._conn.commit()

    def add_lead(self, client_phone: str, realtor_phone: str, client_name: str) -> int:
        try:
            cursor = self._conn.execute(
                "INSERT INTO leads (client_phone, realtor_phone, client_name) VALUES (?, ?, ?)",
                (client_phone, realtor_phone, client_name),
            )
        except sqlite3.IntegrityError as exc:
            raise DuplicateClientError(client_phone) from exc
        self._conn.commit()
        return cursor.lastrowid

    def close(self) -> None:
        self._conn.close()
