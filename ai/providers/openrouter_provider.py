import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

MODELS = [

    "nvidia/nemotron-3-ultra-550b-a55b:free",

    "nvidia/nemotron-3.5-lightning:free"
]


def try_model(
    model,
    prompt
):

    headers = {
        "Authorization": (
            f"Bearer {OPENROUTER_API_KEY}"
        ),
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 80
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    data = response.json()

    print(data)

    if "choices" not in data:
        raise Exception(data)

    reply = (
        data["choices"][0]
        ["message"]["content"]
    )

    if not reply:
        return None

    bad_prefixes = (

        "The user is asking",

        "I need to answer",

        "Looking at the memories",

        "Analyze the request",

        "Current topic",

        "User Persona"
    )

    for prefix in bad_prefixes:

        if reply.startswith(
            prefix
        ):

            print(
                f"REASONING FILTERED: {prefix}"
            )

            return None

    return reply


def generate(prompt):

    for model in MODELS:

        try:

            print(
                f"TRYING OPENROUTER MODEL: {model}"
            )

            reply = try_model(
                model,
                prompt
            )

            if reply:

                print(
                    f"OPENROUTER SUCCESS: {model}"
                )

                print(
                    f"OPENROUTER REPLY: [{reply}]"
                )

                return reply

        except Exception as e:

            print(
                f"OPENROUTER MODEL FAILED {model}: {e}"
            )

            continue

    return None