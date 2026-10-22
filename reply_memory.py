from datetime import datetime, timedelta


class ReplyMemory:

    def __init__(self):

        self.last_npc_message = None
        self.last_npc_time = None

    def register_npc_message(
        self,
        message
    ):

        self.last_npc_message = message
        self.last_npc_time = datetime.now()

    def recent_npc_message(self):

        if self.last_npc_time is None:
            return None

        if datetime.now() - self.last_npc_time > timedelta(minutes=5):
            return None

        return self.last_npc_message