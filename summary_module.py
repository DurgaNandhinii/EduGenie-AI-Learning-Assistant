"""
summary_module.py
------------------
Summarization module.

Leverages Gemini's generative capabilities to summarize long educational
passages into concise, easy-to-understand versions.
"""

import os
import google.generativeai as genai

GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")


def summarize_text(text: str) -> str:
    """
    Summarize a long passage into a shorter, simplified version.

    Args:
        text: The passage to summarize.

    Returns:
        A concise summary, or a readable error message on failure.
    """
    if not text or not text.strip():
        return "Please provide text to summarize."

    try:
        model = genai.GenerativeModel(model_name=GEMINI_MODEL_NAME)
        prompt = (
            "Summarize the following text in simple, easy-to-understand "
            "language. Keep the core information and remove redundancy. "
            "Aim for roughly 3-6 sentences unless the passage is very short.\n\n"
            f"{text}"
        )
        response = model.generate_content(prompt)
        text_out = getattr(response, "text", None)
        if text_out:
            return text_out.strip()
        return "Could not extract a summary from Gemini."
    except Exception as e:  # noqa: BLE001
        return f"Error in Summary: {e}"