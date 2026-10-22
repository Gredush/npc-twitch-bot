from collections import Counter
import sqlite3


class TopicManager:

    def get_recent_messages(self, limit=50):

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

    def detect_topic(self):

        messages = self.get_recent_messages()

        ignored_words = {
            "και",
            "να",
            "στο",
            "στον",
            "την",
            "τον",
            "το",
            "ta",
            "kai",
            "nai",
            "oxi",
            "lol",
            "xaxa",
            "χαχα",
            "χαχαχα",
            "re",
            "ρε"
        }

        words = []

        for message in messages:

            for word in message.lower().split():

                word = word.strip(".,!?()[]{}")

                if len(word) < 4:
                    continue

                if word in ignored_words:
                    continue

                words.append(word)

        if not words:
            return None, 0

        counter = Counter(words)

        topic, count = counter.most_common(1)[0]

        return topic, count