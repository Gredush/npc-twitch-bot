import sqlite3


class InterestManager:

    INTEREST_KEYWORDS = {

        "wow": [
            "wow",
            "world",
            "warcraft",
            "raid",
            "guild",
            "mythic"
        ],

        "rust": [
            "rust",
            "base",
            "raid",
            "heli"
        ],

        "tarkov": [
            "tarkov",
            "eft",
            "labs"
        ],

        "hardware": [
            "cpu",
            "gpu",
            "amd",
            "intel",
            "nvidia",
            "ram"
        ]
    }

    def __init__(self):

        self.ensure_table()

    def ensure_table(self):

        conn = sqlite3.connect(
            "memory.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS interests (
            username TEXT,
            interest TEXT,
            score INTEGER DEFAULT 0,
            PRIMARY KEY (
                username,
                interest
            )
        )
        """)

        conn.commit()
        conn.close()

    def process_message(
        self,
        username,
        message
    ):

        text = message.lower()

        conn = sqlite3.connect(
            "memory.db"
        )

        cursor = conn.cursor()

        for interest, keywords in (
            self.INTEREST_KEYWORDS.items()
        ):

            found = False

            for keyword in keywords:

                if keyword in text:

                    found = True
                    break

            if not found:
                continue

            cursor.execute("""
            INSERT OR IGNORE INTO interests
            (
                username,
                interest,
                score
            )
            VALUES (?, ?, 0)
            """, (
                username,
                interest
            ))

            cursor.execute("""
            UPDATE interests
            SET score = score + 1
            WHERE username = ?
            AND interest = ?
            """, (
                username,
                interest
            ))

        conn.commit()
        conn.close()

    def get_top_interests(
        self,
        username,
        limit=3
    ):

        conn = sqlite3.connect(
            "memory.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            interest,
            score
        FROM interests
        WHERE username = ?
        ORDER BY score DESC
        LIMIT ?
        """, (
            username,
            limit
        ))

        rows = cursor.fetchall()

        conn.close()

        return rows