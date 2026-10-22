import sqlite3


class ConversationAwareness:

    def get_last_npc_message(self):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT message
            FROM messages
            WHERE username = 'KynigaoBot'
            ORDER BY id DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        conn.close()

        if not row:
            return None

        return row[0]

    def looks_like_reply_to_npc(
        self,
        username,
        message
    ):

        text = message.lower()

        triggers = [
            "εσύ",
            "esy",
            "λες",
            "λες;",
            "τι λες",
            "re",
            "ρε",
            "σοβαρά",
            "όντως",
            "ontws",
            "χαχα",
            "xaxa",
            "καλά",
            "kala"
        ]

        for trigger in triggers:

            if trigger in text:
                return True

        return False
