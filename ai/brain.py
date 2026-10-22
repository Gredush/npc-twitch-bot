from ai.providers.groq_provider import generate

from conversation_tracker import ConversationTracker
from social_memory import SocialMemory
from language_detector import LanguageDetector
from context_recall import ContextRecall
from interest_manager import InterestManager


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
    social = SocialMemory()
    detector = LanguageDetector()
    recall = ContextRecall()

    language = detector.detect(
        user_message
    )

    topic = tracker.get_current_topic()

    recent_context = (
        recall.build_context_summary(
            15
        )
    )

    interests = (
        InterestManager()
        .get_top_interests(
            username
        )
    )

    interest_block = "\n".join(
        [
            interest
            for interest, score in interests
        ]
    )

    memories = social.get_relevant_memories(
        username,
        user_message
    )

    memory_block = "\n".join(
        memories
    )

    return f"""
{personality}

CURRENT TOPIC:
{topic}

LANGUAGE:
{language}

USER:
{username}

INTERESTS:
{interest_block}

MEMORIES:
{memory_block}

RECENT CONTEXT:
{recent_context}

LATEST MESSAGE:
{username}: {user_message}

ΚΑΝΟΝΕΣ:

Απάντησε σαν viewer σε Twitch chat.

Μία πρόταση.

Μέχρι 8 λέξεις.

Αν LANGUAGE είναι greeklish,
απάντα greeklish.

Αν LANGUAGE είναι greek,
απάντα ελληνικά.

Αν δεν ξέρεις κάτι,
πες ότι δεν ξέρεις.

Μην επινοείς πληροφορίες.

Μην γράφεις ποιητικά.

Μην γράφεις αφηρημένες φράσεις.

Μην προσπαθείς να είσαι έξυπνος.

Μην χρησιμοποιείς περίεργες εκφράσεις.

Να ακούγεσαι φυσικός.

ΠΟΛΥ ΣΗΜΑΝΤΙΚΟ:

Αν αναφέρεις στοιχεία που ξέρεις για τον χρήστη,
χρησιμοποίησε ΜΟΝΟ πληροφορίες που υπάρχουν στις μνήμες.

Μην αλλάζεις αριθμούς.

Μην μαντεύεις.

Μην συμπληρώνεις πληροφορίες.

Αν δεν ξέρεις, πες ότι δεν ξέρεις.

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
