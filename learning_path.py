"""
learning_path.py
-----------------
Learning Path / Recommendations module.

Uses Google Gemini to generate a personalized, structured learning path
(beginner -> intermediate -> advanced) for any topic the learner names.
"""

import os
import traceback
import google.generativeai as genai

GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")


def get_learning_recommendations(topic: str) -> str:
    """
    Generate a structured, adaptive learning path for a given topic.

    Args:
        topic: The subject the learner wants a study plan for.

    Returns:
        A Markdown-formatted learning path as text, or an error message.
    """
    if not topic or not topic.strip():
        return "Please provide a topic to get learning recommendations."

    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.

Suggest a structured and adaptive learning path including key topics,
order of learning, estimated timelines, and useful resources (videos,
articles, or books). Include beginner, intermediate, and advanced levels.
Keep it practical and well organized with clear headings.
"""

    try:
        model = genai.GenerativeModel(model_name=GEMINI_MODEL_NAME)
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text
        elif hasattr(response, "parts") and response.parts:
            return response.parts[0].text
        else:
            return "Could not extract content from Gemini response."
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        return f"Error occurred: {e}"