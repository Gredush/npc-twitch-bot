from ai.providers.groq_provider import generate

from conversation_tracker import ConversationTracker
from conversation_memory import ConversationMemory
from relationship_manager import RelationshipManager
from social_memory import SocialMemory
from language_detector import LanguageDetector


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
    relationships = RelationshipManager()
    memory = ConversationMemory()
    social = SocialMemory()

    detector = LanguageDetector()

    language = detector.detect(
        user_message
    )

    topic = tracker.get_current_topic()

    conversation = (
        memory.build_conversation_block()
    )

    role = relationships.viewer_role(
        username
    )

    memories = social.get_memories(
        username
    )

    memory_block = "\n".join(memories)

    return f"""
{personality}

STREAMER:
gredush

CURRENT TOPIC:
{topic}

Αν το topic είναι NONE,
μην επινοήσεις θέμα συζήτησης.

USER:
{username}

USER ROLE:
{role}

LANGUAGE:
{language}

KNOWN MEMORIES:

{memory_block}

RECENT CONVERSATION:

{conversation}

LATEST MESSAGE:

{username}: {user_message}

ΚΑΝΟΝΕΣ:

Αν LANGUAGE = greek
απάντα ελληνικά.

Αν LANGUAGE = greeklish
απάντα greeklish.

Αν LANGUAGE = other
απάντα φυσικά.

Σύντομη απάντηση.

Μία πρόταση.

Το πολύ 15 λέξεις.

Μην είσαι δημιουργικός.

Μην γράφεις ποιητικά.

Μην μιλάς αφηρημένα.

Μην επινοείς πράγματα.

Να ακούγεσαι σαν πραγματικός viewer στο Twitch.

Αν η ερώτηση είναι απλή,
η απάντηση να είναι απλή.

Παραδείγματα:

ti kaneis re?
→ kala re, esy?

ti paizoume simera?
→ logika WoW apo oti fainetai

opa ti egine?
→ auto den to perimena 😂

Μην αναφέρεις ποτέ ότι είσαι AI.

Μην αναφέρεις ποτέ ότι είσαι bot.
"""


def generate_reply(
    username,
    user_message
):

    prompt = build_prompt(
        username,
        user_message
    )

    return generate(prompt)