import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

MODEL = "gemini-3.8-flash"


def generate(prompt):

    url = (
        "https://generativelanguage.googleapis.com"
        f"/v1beta/models/{MODEL}:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url,
        json=payload,
        timeout=30
    )

    data = response.json()

    if "candidates" not in data:
        raise Exception(data)

    return (
        data["candidates"][0]
        ["content"]["parts"][0]["text"]
    )