from datetime import datetime, timedelta


class NPCState:

    def __init__(self):

        self.last_reply_time = None
        self.messages_since_reply = 0

    def register_message(self):

        self.messages_since_reply += 1

    def can_reply(self):

        # Τουλάχιστον 10 μηνύματα από τότε που μίλησε

        if self.messages_since_reply < 4:
            return False

        # Πρώτη φορά

        if self.last_reply_time is None:
            return True

        # Cooldown 3 λεπτών

        cooldown = timedelta(minutes=1)

        if datetime.now() - self.last_reply_time < cooldown:
            return False

        return True


    def force_reply(self):
        """Επιτρέπει απάντηση αμέσως (π.χ. όταν γίνεται mention)."""
        return True

    def register_reply(self):

        self.last_reply_time = datetime.now()
        self.messages_since_reply = 0