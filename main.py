"""
main.py
-------
EduGenie: Google Gemini Powered Learning Assistant.

FastAPI backend that serves the frontend and exposes REST endpoints for:
    GET  /qa                     - Ask a question
    POST /explain/                - Get a simplified explanation of a topic
    POST /summarize/               - Summarize a passage
    POST /quiz                    - Generate a 3-question MCQ quiz
    GET  /learn/recommendations   - Get a personalized learning path
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env BEFORE importing modules that read
# them at import time (they read GEMINI_MODEL / EXPLAIN_MODE at import).
load_dotenv()

import google.generativeai as genai
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

# ---------------------------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print(
        "WARNING: GEMINI_API_KEY is not set. Copy .env.example to .env and "
        "add your API key, otherwise AI features will fail."
    )

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(title="EduGenie", description="Google Gemini Powered Learning Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    """Serve the main HTML frontend."""
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------------------------------------------------------------
# Q&A - GET API using Gemini
# ---------------------------------------------------------------------------
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}


# ---------------------------------------------------------------------------
# Explanation - POST API
# ---------------------------------------------------------------------------
@app.post("/explain/")
async def explain_api(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}


# ---------------------------------------------------------------------------
# Summarization - POST API
# ---------------------------------------------------------------------------
@app.post("/summarize/")
async def summarize_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}


# ---------------------------------------------------------------------------
# Quiz Generation - POST API
# ---------------------------------------------------------------------------
@app.post("/quiz")
async def quiz_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    return JSONResponse(content={"quiz": quiz})


# ---------------------------------------------------------------------------
# Learning Recommendations - GET API
# ---------------------------------------------------------------------------
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)