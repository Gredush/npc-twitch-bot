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

    def extract(self, username, message):

        text = message.lower()

        if len(text.split()) < 4:
            return None

        for trigger in self.TRIGGERS:

            if trigger in text:

                return message.strip()

        return None