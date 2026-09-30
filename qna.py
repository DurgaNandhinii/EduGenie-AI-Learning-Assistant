"""
qna.py
------
Question & Answer module.

Uses Google Gemini to answer general knowledge / academic questions with
precision and contextual understanding.
"""

import os
import google.generativeai as genai

GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")


def answer_question_with_gemini(question: str) -> str:
    """
    Send a user's question to Gemini and return a concise answer.

    Args:
        question: The natural-language question asked by the student.

    Returns:
        The model's answer as plain text, or a readable error message
        if something goes wrong.
    """
    if not question or not question.strip():
        return "Please provide a question."

    try:
        model = genai.GenerativeModel(model_name=GEMINI_MODEL_NAME)
        prompt = (
            "You are EduGenie, a friendly and knowledgeable AI tutor. "
            "Answer the student's question clearly, accurately, and concisely. "
            "Prefer a few sentences over a long essay unless the question needs "
            "more detail.\n\n"
            f"Question: {question}"
        )
        response = model.generate_content(prompt)
        text = getattr(response, "text", None)
        if text:
            return text.strip()
        return "Could not extract a response from Gemini."
    except Exception as e:  # noqa: BLE001 - surface a readable error to the UI
        return f"Error in QnA: {e}"