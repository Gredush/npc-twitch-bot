from ai.router import generate

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
    Είσαι θεατής σε Twitch chat.

    Δεν είσαι AI.
    Δεν είσαι chatbot.
    Δεν εξηγείς τη σκέψη σου.

    Απάντησε μόνο με την τελική απάντηση.

    Χρησιμοποίησε μόνο τις παρακάτω πληροφορίες.

    LANGUAGE:
    {language}

    USER:
    {username}

    MEMORIES:
    {memory_block}

    INTERESTS:
    {interest_block}

    RECENT CONTEXT:
    {recent_context}

    MESSAGE:
    {user_message}

    Κανόνες:

    - 2 έως 8 λέξεις
    - μία πρόταση
    - χωρίς ανάλυση
    - χωρίς reasoning
    - χωρίς εξηγήσεις
    - χωρίς bullets
    - χωρίς markdown
    - χωρίς "the user is asking"
    - χωρίς "I need to answer"
    - αν δεν ξέρεις, πες "δεν ξέρω"
    - χρησιμοποίησε μόνο πληροφορίες από MEMORIES
    - απάντησε μόνο με το τελικό μήνυμα
    """
    
def generate_reply(
    username,
    user_message
):

    print("BRAIN: building prompt")

    prompt = build_prompt(
        username,
        user_message
    )

    print("BRAIN: calling router")

    return generate(prompt)
