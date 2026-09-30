# Requirement Analysis Phase

## Project Description
EduGenie is a lightweight AI-powered educational assistant that simplifies
learning through generative AI. It enables users to:
- Ask questions and receive smart, concise answers
- Understand complex concepts through simplified explanations
- Generate quizzes from topics or text
- Receive personalized learning recommendations
- Summarize large educational passages

Built with **FastAPI** for the backend and a simple **HTML+CSS** frontend,
EduGenie is lightweight enough to run well on devices like a Mac M1.

## Functional Requirements
| ID | Requirement |
|---|---|
| FR1 | User can ask a question and receive an AI-generated answer |
| FR2 | User can enter a topic and receive a simplified explanation |
| FR3 | User can enter a topic/passage and receive a 3-question MCQ quiz |
| FR4 | User can paste a long passage and receive a concise summary |
| FR5 | User can enter a topic and receive a structured learning path |

## Non-Functional Requirements
- Lightweight enough to run on low-resource devices
- Responsive web interface
- Clear error handling if the AI API fails or returns invalid data

## User Scenarios
**Scenario 1:** A student wants to know about oceans and rivers, and uses
EduGenie to ask "Which is the largest ocean?"

**Scenario 2:** A student wants to check her understanding of "The
Pythagoras Theorem" and clicks "Generate Quiz."

**Scenario 3:** A learner exploring SQL requests a learning path — a
structured plan with beginner-to-advanced topics, timelines, and
suggestions.

## Prerequisites
1. Python 3.10+
2. FastAPI framework
3. HTML & CSS (basic templating, used in `/templates` and `/static`)
4. Google Gemini API key (from Google AI Studio)
5. Uvicorn (ASGI server)
6. Jinja2 (HTML templating engine)