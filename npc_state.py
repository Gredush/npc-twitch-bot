from datetime import datetime, timedelta


# ============================================================
# ADAPTIVE COOLDOWN
# ============================================================
ADAPTIVE_COOLDOWN = True
BASE_COOLDOWN_SEC = 90      # ήσυχο chat
MIN_COOLDOWN_SEC = 15       # ζεστό chat
MIN_MESSAGES_BETWEEN = 2    # τουλάχιστον 2 μηνύματα από την τελευταία απάντηση
IMPORTANT_COOLDOWN_SEC = 5  # bypass: max 1 απάντηση / 5s

ALWAYS_ALLOW_PATTERNS = [
    "i was here", "imoun edw", "ήμουν εδώ",
]

def _is_important_message(message):
    """Μηνύματα που αξίζουν απάντηση ανεξαρτήτως cooldown."""
    if not message:
        return False
    m = message.lower()
    if "?" in message or ";" in message:
        return True
    if "@jokersmiles" in m or "joker" in m:
        return True
    if len(message) > 40:
        return True
    for p in ALWAYS_ALLOW_PATTERNS:
        if p in m:
            return True
    return False


class NPCState:

    def __init__(self):
        self.last_reply_time = None
        self.messages_since_reply = 0
        self._chat_times = []  # timestamps τελευταίων μηνυμάτων

    def register_message(self):
        self.messages_since_reply += 1
        now = datetime.now()
        self._chat_times.append(now)
        # κράτα μόνο τα τελευταία 60s
        cutoff = now - timedelta(seconds=60)
        self._chat_times = [t for t in self._chat_times if t > cutoff]

    def _chat_rate_per_minute(self):
        return len(self._chat_times)

    def _compute_cooldown_sec(self):
        if not ADAPTIVE_COOLDOWN:
            return BASE_COOLDOWN_SEC
        rate = self._chat_rate_per_minute()
        if rate <= 0:
            return BASE_COOLDOWN_SEC
        if rate >= 60:
            return MIN_COOLDOWN_SEC
        # γραμμική παρεμβολή
        return BASE_COOLDOWN_SEC - (BASE_COOLDOWN_SEC - MIN_COOLDOWN_SEC) * (rate / 60.0)

    def can_reply(self, message=None):
        # ελάχιστα μηνύματα από την τελευταία απάντηση
        if self.messages_since_reply < MIN_MESSAGES_BETWEEN:
            return False

        # πρώτη φορά
        if self.last_reply_time is None:
            return True

        elapsed = (datetime.now() - self.last_reply_time).total_seconds()

        # bypass για σημαντικά μηνύματα
        if message and _is_important_message(message):
            return elapsed >= IMPORTANT_COOLDOWN_SEC

        cooldown = self._compute_cooldown_sec()
        return elapsed >= cooldown

    def force_reply(self):
        """Επιτρέπει απάντηση αμέσως (π.χ. όταν γίνεται mention)."""
        return True

    def register_reply(self):
        self.last_reply_time = datetime.now()
        self.messages_since_reply = 0
