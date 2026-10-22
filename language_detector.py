import re


class LanguageDetector:

    def is_greek(self, text):

        return bool(
            re.search(
                r"[α-ωΑ-Ω]",
                text
            )
        )

    def is_greeklish(self, text):

        if self.is_greek(text):
            return False

        greeklish_words = [
            "ti",
            "kala",
            "re",
            "ela",
            "pame",
            "giati",
            "pos",
            "eimai",
            "eisai",
            "opa",
            "nai",
            "oxi",
            "kati",
            "paizei",
            "paizoume",
            "simera",
            "malaka",
            "ontws",
            "xaxa",
            "lol"
        ]

        text = text.lower()

        score = 0

        for word in greeklish_words:

            if word in text:
                score += 1

        return score >= 1

    def detect(self, text):

        if self.is_greek(text):
            return "greek"

        if self.is_greeklish(text):
            return "greeklish"

        return "other"