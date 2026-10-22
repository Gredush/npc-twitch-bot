from ai.utils.memory_loader import get_recent_messages


def build_chat_context(limit=20):

    messages = get_recent_messages(limit)

    context = []

    for username, message in messages:
        context.append(
            f"{username}: {message}"
        )

    return "\n".join(context)