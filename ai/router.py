from ai.providers.groq_provider import (
    generate as groq_generate
)

from ai.providers.openrouter_provider import (
    generate as openrouter_generate
)

from ai.providers.gemini_provider import (
    generate as gemini_generate
)


def generate(prompt):

    print(
        "ROUTER: trying GROQ"
    )

    try:

        reply = groq_generate(
            prompt
        )

        print(
            f"GROQ REPLY: [{reply}]"
        )

        if reply:

            print(
                "ROUTER: returning GROQ reply"
            )

            return reply

    except Exception as e:

        print(
            f"GROQ FAILED: {e}"
        )

    print(
        "ROUTER: trying OPENROUTER"
    )

    try:

        reply = openrouter_generate(
            prompt
        )

        print(
            f"OPENROUTER REPLY: [{reply}]"
        )

        if reply:

            print(
                "ROUTER: returning OPENROUTER reply"
            )

            return reply

    except Exception as e:

        print(
            f"OPENROUTER FAILED: {e}"
        )

    print(
        "ROUTER: trying GEMINI"
    )

    try:

        reply = gemini_generate(
            prompt
        )

        print(
            f"GEMINI REPLY: [{reply}]"
        )

        if reply:

            print(
                "ROUTER: returning GEMINI reply"
            )

            return reply

    except Exception as e:

        print(
            f"GEMINI FAILED: {e}"
        )

    print(
        "ROUTER: local fallback"
    )

    return "den ksero re 😄"