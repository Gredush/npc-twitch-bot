import sqlite3
from datetime import datetime


class AffinityManager:

    def __init__(self):

        self.ensure_table()

    def ensure_table(self):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS affinity (
            username TEXT PRIMARY KEY,
            score INTEGER DEFAULT 0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()

    def increase(
        self,
        username,
        amount=1
    ):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT OR IGNORE INTO affinity
        (username, score)
        VALUES (?, 0)
        """, (username,))

        cursor.execute("""
        UPDATE affinity
        SET
            score = score + ?,
            last_updated = CURRENT_TIMESTAMP
        WHERE username = ?
        """, (
            amount,
            username
        ))

        conn.commit()
        conn.close()

    def apply_decay(self):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            username,
            score,
            last_updated
        FROM affinity
        """)

        rows = cursor.fetchall()

        now = datetime.now()

        for username, score, last_updated in rows:

            try:

                last = datetime.fromisoformat(
                    last_updated
                )

                days = (
                    now - last
                ).days

                decay = days // 7

                new_score = max(
                    0,
                    score - decay
                )

                cursor.execute("""
                UPDATE affinity
                SET score = ?
                WHERE username = ?
                """, (
                    new_score,
                    username
                ))

            except Exception:
                pass

        conn.commit()
        conn.close()

    def get_score(
        self,
        username
    ):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT score
        FROM affinity
        WHERE username = ?
        """, (username,))

        row = cursor.fetchone()

        conn.close()

        if not row:
            return 0

        return row[0]