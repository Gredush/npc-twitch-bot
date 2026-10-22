from ai.providers.groq_provider import generate


class MemoryExtractor:

    def extract(self, username, message):

        prompt = f"""
Χρήστης:

{username}

Μήνυμα:

{message}

Πρέπει να αποφασίσεις αν υπάρχει προσωπική πληροφορία που αξίζει να θυμάται ένας φίλος.

Παραδείγματα:

"παίζω Rust"
-> ΠΑΙΖΕΙ_RUST

"δουλεύω οδηγός"
-> ΔΟΥΛΕΥΕΙ_ΟΔΗΓΟΣ

"πήρα μηχανή"
-> ΕΧΕΙ_ΜΗΧΑΝΗ

"ωραίο stream"
-> NONE

Απάντησε ΜΟΝΟ με:

NONE

ή

μία σύντομη μνήμη.
"""

        result = generate(prompt)

        if not result:
            return None

        result = result.strip()

        if result.upper() == "NONE":
            return None

        return result