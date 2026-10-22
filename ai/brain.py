from ai.utils.context_builder import build_chat_context
from ai.providers.groq_provider import generate
from conversation_tracker import ConversationTracker
from relationship_manager import RelationshipManager


def load_personality():

    with open(
        "ai/prompts/personality.txt",
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def build_prompt(username, user_message):

    personality = load_personality()

    tracker = ConversationTracker()

    relationship_manager = RelationshipManager()

    role = relationship_manager.viewer_role(
        username
    )

    topic = tracker.get_current_topic()

    context = build_chat_context(25)

    return f"""
{personality}

Πληροφορίες:

Τρέχον θέμα:
{topic}

Ο χρήστης που μίλησε:
{username}

Ρόλος:
{role}

Ο streamer λέγεται:
gredush

Αν μιλά ο gredush:
να του απαντάς φυσικά.

Αν κάποιος τρολάρει τον gredush:
συνήθως τον υπερασπίζεσαι με χιούμορ.

Δεν γλείφεις.

Δεν κάνεις moderation.

Δεν λες σε ανθρώπους τι να κάνουν.

____________

Chat:

{context}

____________

Νέο μήνυμα:

{username}: {user_message}

Απάντησε σαν παλιός viewer.

Μία σύντομη πρόταση.

Όχι παραγράφους.

Όχι ότι είσαι AI.

Όχι ότι είσαι bot.
"""


def generate_reply(username, user_message):

    prompt = build_prompt(
        username,
        user_message
    )

    return generate(prompt)