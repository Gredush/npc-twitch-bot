import sqlite3


class ConversationMemory:

    def get_recent_conversation(self, limit=15):

        conn = sqlite3.connect("memory.db")
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

    def build_conversation_block(self):

        messages = self.get_recent_conversation()

        text = []

        for username, message in messages:

            text.append(
                f"{username}: {message}"
            )

        return "\n".join(text)