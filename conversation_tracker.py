import sqlite3
from collections import Counter


class ConversationTracker:

    def get_recent_messages(self, limit=30):

        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT message
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        conn.close()

        return [row[0] for row in rows]

    def get_current_topic(self):

        messages = self.get_recent_messages()

        words = []

        ignored = {
            "και",
            "το",
            "να",
            "που",
            "τι",
            "σε",
            "για",
            "με",
            "θα",
            "στο",
            "της",
            "της",
            "την",
            "τον",
            "ένα",
            "μια",
            "nice",
            "lol",
            "lmao",
            "xdd",
            "χαχα",
            "χαχαχα"
        }

        for message in messages:

            for word in message.lower().split():

                word = word.strip(".,!?()[]{}")

                if len(word) < 4:
                    continue

                if word in ignored:
                    continue

                words.append(word)

        if not words:
            return None

        counter = Counter(words)

        topic, count = counter.most_common(1)[0]

        if count < 3:
            return None

        return topic