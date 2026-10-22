import sqlite3


class AffinityManager:

    def __init__(self):

        self.ensure_table()

    def ensure_table(self):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS affinity (
                username TEXT PRIMARY KEY,
                score INTEGER DEFAULT 0
            )
            """
        )

        conn.commit()
        conn.close()

    def increase(
        self,
        username,
        amount=1
    ):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO affinity
            (username, score)
            VALUES (?, 0)
            """,
            (username,)
        )

        cursor.execute(
            """
            UPDATE affinity
            SET score = score + ?
            WHERE username = ?
            """,
            (
                amount,
                username
            )
        )

        conn.commit()
        conn.close()

    def get_score(
        self,
        username
    ):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT score
            FROM affinity
            WHERE username = ?
            """,
            (username,)
        )

        row = cursor.fetchone()

        conn.close()

        if not row:
            return 0

        return row[0]