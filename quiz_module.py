"""
quiz_module.py
--------------
Quiz generation module.

Generates 3 multiple-choice questions (4 options each) from a given
topic or passage of text, using Google Gemini. Output is normalized
into a Python list of dicts:

    [
        {"question": "...", "options": ["A", "B", "C", "D"], "answer": "A"},
        ...
    ]
"""

import os
import re
import json
import google.generativeai as genai

GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")


def clean_json_block(text: str) -> str:
    """Strip Markdown ```json ... ``` code fences if Gemini adds them."""
    return re.sub(r"```(?:json)?\n?(.*?)```", r"\1", text, flags=re.DOTALL).strip()


def generate_quiz(text: str) -> list:
    """
    Generate a 3-question multiple-choice quiz from a topic or passage.

    Args:
        text: A topic name (e.g. "Pythagoras theorem") or a longer passage.

    Returns:
        A list of question dicts, or a list containing a single dict with
        an "error" key if generation/parsing fails.
    """
    if not text or not text.strip():
        return [{"error": "Please provide text or a topic for the quiz."}]

    try:
        model = genai.GenerativeModel(model_name=GEMINI_MODEL_NAME)

        prompt = f"""You are a quiz generator.

From the following passage or topic, create exactly 3 multiple-choice
questions. Each question should include:
- A "question"
- A list of 4 "options"
- A "answer" that must exactly match one of the options.

Respond with ONLY valid JSON, no markdown, no commentary, in this exact
shape:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage/topic:
{text}
"""

        response = model.generate_content(prompt)
        quiz_text = (response.text or "").strip()
        cleaned_text = clean_json_block(quiz_text)

        quiz = json.loads(cleaned_text)

        # Basic shape validation so a malformed model response doesn't
        # break the frontend.
        if not isinstance(quiz, list):
            raise ValueError("Model response was not a JSON list.")
        for q in quiz:
            if not all(k in q for k in ("question", "options", "answer")):
                raise ValueError("A quiz question is missing required fields.")

        return quiz

    except json.JSONDecodeError as e:
        return [{"error": f"Could not parse quiz JSON: {e}"}]
    except Exception as e:  # noqa: BLE001
        return [{"error": f"Error generating quiz: {e}"}]