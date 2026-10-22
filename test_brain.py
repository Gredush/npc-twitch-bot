from ai.brain import build_prompt
from ai.providers.groq_provider import try_model

prompt = build_prompt(
    "gredush",
    "ti paizoume simera?"
)

response = try_model(
    "openai/gpt-oss-20b",
    prompt
)

print(response)