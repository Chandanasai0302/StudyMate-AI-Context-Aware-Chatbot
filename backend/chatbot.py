
import os
import asyncio
from typing import Dict, List

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your root .env file."
    )

client = genai.Client(api_key=API_KEY)

# Separate history for every conversation.
conversations: Dict[str, List[dict]] = {}

MAX_HISTORY_MESSAGES = 10

SYSTEM_PROMPT = """
You are StudyMate AI, a friendly AI study companion.

Help students understand Python, DSA, AI, machine learning,
and software development.

Explain difficult concepts in simple language.
Use examples where helpful.
Remember relevant information from earlier messages.
Be encouraging, clear, and beginner-friendly.
"""


def get_conversation(conversation_id: str) -> List[dict]:
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    return conversations[conversation_id]


def trim_history(history: List[dict]) -> List[dict]:
    return history[-MAX_HISTORY_MESSAGES:]


async def generate_response(
    conversation_id: str,
    user_message: str
) -> str:

    history = get_conversation(conversation_id)

    # Include the new message when building the context.
    updated_history = history + [
        {
            "role": "user",
            "parts": [{"text": user_message}]
        }
    ]

    limited_history = trim_history(updated_history)

    try:
        response = await asyncio.wait_for(
            client.aio.models.generate_content(
                model=MODEL_NAME,
                contents=limited_history,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=1024
                )
            ),
            timeout=45
        )

        answer = response.text

        if not answer:
            raise ValueError("The AI returned an empty response.")

        # Save messages only after a successful API response.
        history.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        history.append({
            "role": "model",
            "parts": [{"text": answer}]
        })

        conversations[conversation_id] = trim_history(history)

        return answer

 
    except asyncio.TimeoutError:
        raise RuntimeError(
            "The AI response timed out. Please try again."
        )

    except Exception as error:
        print("Gemini API error type:", type(error).__name__)
        print("Gemini API error details:", str(error))

        if "503" in str(error) or "UNAVAILABLE" in str(error):
            raise RuntimeError(
                "Gemini is temporarily busy. Please wait a few minutes and try again."
            )

        raise RuntimeError(
            "Gemini request failed. Check the API configuration and terminal error."
        )
  