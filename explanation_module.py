"""
explanation_module.py
----------------------
Concept explanation module.

The project documentation describes this module as using a local,
lightweight instruction-tuned model (LaMini-Flan-T5-783M) so explanations
can run without a network call. That model works well but requires
installing `transformers` + `torch` (a multi-GB download) and is slow on
CPU-only machines.

To keep this project easy to install and run out of the box, this module
defaults to using the Gemini API (EXPLAIN_MODE=gemini in .env) for
explanations too. If you want the original local-model behavior, set
EXPLAIN_MODE=local in your .env file and uncomment the transformers/torch
lines in requirements.txt, then reinstall dependencies.
"""

import os
import google.generativeai as genai

GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
EXPLAIN_MODE = os.getenv("EXPLAIN_MODE", "gemini").lower()

# Lazily-initialized local model globals (only used if EXPLAIN_MODE=local)
_explain_tokenizer = None
_explain_model = None


def _load_local_model():
    """Load LaMini-Flan-T5-783M the first time it's needed."""
    global _explain_tokenizer, _explain_model
    if _explain_model is not None:
        return

    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    _explain_tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
    _explain_model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")


def _explain_topic_local(topic: str) -> str:
    """Generate an explanation using the local LaMini-Flan-T5-783M model."""
    _load_local_model()

    input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
    inputs = _explain_tokenizer(input_text, return_tensors="pt")

    outputs = _explain_model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        do_sample=True,
    )

    return _explain_tokenizer.decode(outputs[0], skip_special_tokens=True)


def _explain_topic_gemini(topic: str) -> str:
    """Generate an explanation using the Gemini API."""
    model = genai.GenerativeModel(model_name=GEMINI_MODEL_NAME)
    prompt = (
        f"Explain the concept of '{topic}' in a simple and clear way for a "
        "school student. Keep it concise (a short paragraph), avoid jargon "
        "where possible, and use an example if it helps understanding."
    )
    response = model.generate_content(prompt)
    text = getattr(response, "text", None)
    return text.strip() if text else "Could not generate an explanation."


def explain_topic(topic: str) -> str:
    """
    Produce a simplified, student-friendly explanation of a topic.

    Routes to either the local model or Gemini depending on the
    EXPLAIN_MODE environment variable.

    Args:
        topic: The concept the learner wants explained.

    Returns:
        A plain-text explanation, or a readable error message.
    """
    if not topic or not topic.strip():
        return "Please provide a topic to explain."

    try:
        if EXPLAIN_MODE == "local":
            return _explain_topic_local(topic)
        return _explain_topic_gemini(topic)
    except Exception as e:  # noqa: BLE001
        return f"Error in Explanation: {e}"