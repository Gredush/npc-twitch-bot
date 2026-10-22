from reply_memory_instance import reply_memory


class ConversationAwareness:

    def looks_like_reply_to_npc(
        self,
        username,
        message
    ):

        recent = reply_memory.recent_npc_message()

        if recent is None:
            return False

        text = message.lower()

        triggers = [
            "εσύ",
            "esy",
            "τι λες",
            "λες",
            "καλά",
            "kala",
            "όντως",
            "ontws",
            "γιατί",
            "giati",
            "χαχα",
            "xaxa",
            "αυτό",
            "auto"
        ]

        for trigger in triggers:

            if trigger in text:
                return True

        return False