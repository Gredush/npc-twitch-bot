import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODELS = [
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b"
]


def try_model(model_name, prompt):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
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
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    data = response.json()

    if "choices" not in data:
        raise Exception(data)

    return data["choices"][0]["message"]["content"]


def generate(prompt):

    for model in MODELS:

        try:

            reply = try_model(
                model,
                prompt
            )

            if reply:
                return reply

        except Exception:
            continue

    return None