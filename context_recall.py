import sqlite3


class ContextRecall:

    def get_recent_context(
        self,
        limit=20
    ):

        conn = sqlite3.connect(
            "memory.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT username, message
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        conn.close()

        rows.reverse()

        return rows

    def build_context_summary(
        self,
        limit=20
    ):

        rows = self.get_recent_context(
            limit
        )

        return "\n".join(
            [
                f"{user}: {msg}"
                for user, msg in rows
            ]
        )