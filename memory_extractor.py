class MemoryExtractor:

    TRIGGERS = [

        "παίζω",
        "δουλεύω",
        "εργάζομαι",
        "σπουδάζω",
        "μένω",
        "είμαι",
        "μου αρέσει",
        "λατρεύω",
        "πήρα",
        "αγόρασα",
        "έχω"
    ]

    QUESTION_MARKERS = [

        "?",
        "ποιος",
        "ποια",
        "ποιο",
        "τι",
        "πώς",
        "πως",
        "γιατί",
        "που",
        "πού",
        "πότε",
        "με ξέρεις",
        "ξέρεις",
        "γνωρίζεις"
    ]

    def extract(
        self,
        username,
        message
    ):

        text = (
            message
            .lower()
            .strip()
        )

        if text.startswith("!"):
            return None

        if len(text.split()) < 4:
            return None

        for marker in self.QUESTION_MARKERS:

            if marker in text:
                return None

        for trigger in self.TRIGGERS:

            if trigger in text:

                return message.strip()

        return None