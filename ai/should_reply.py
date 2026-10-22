from ai.utils.context_builder import build_chat_context
from ai.providers.groq_provider import generate
from conversation_awareness import ConversationAwareness


def should_reply(username, message):

    awareness = ConversationAwareness()

    if awareness.looks_like_reply_to_npc(
        username,
        message
    ):
        return True

    chat_context = build_chat_context(15)

    prompt = f"""
Είσαι viewer σε Twitch chat.

Απάντησε ΜΟΝΟ:

YES

ή

NO

YES μόνο αν:

- συνεχίζεται συζήτηση
- υπάρχει χιούμορ
- υπάρχει ερώτηση
- αξίζει να συμμετέχεις

NO αν:

- απλό γεια
- μονόλεκτη απάντηση
- δεν έχεις κάτι να προσθέσεις

CHAT:

{chat_context}

ΝΕΟ ΜΗΝΥΜΑ:

{username}: {message}
"""

    result = generate(prompt)

    if not result:
        return False

    return "YES" in result.upper()