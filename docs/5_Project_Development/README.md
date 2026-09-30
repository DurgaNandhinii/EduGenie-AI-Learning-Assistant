# Project Development Phase

All source code for this phase lives in the project root directory
(not duplicated here to avoid redundancy). Key files:

| File | Purpose |
|---|---|
| `main.py` | FastAPI app, route definitions, Gemini configuration |
| `qna.py` | Q&A module using Gemini |
| `explanation_module.py` | Concept explanation module |
| `quiz_module.py` | Quiz generation + JSON parsing/validation |
| `summary_module.py` | Text summarization module |
| `learning_path.py` | Learning path recommendation module |
| `templates/index.html` | Frontend UI (tabs for all 5 features) |
| `static/style.css` | Frontend styling |

## Key Implementation Notes
- Each module wraps its Gemini API call in a `try/except` block to
  return a readable error message instead of crashing the app.
- The quiz module strips Markdown code fences from Gemini's response
  before parsing it as JSON, since the model sometimes wraps JSON in
  ` ```json ... ``` ` blocks.
- Environment variables (`GEMINI_API_KEY`, `GEMINI_MODEL`) are loaded
  once at startup in `main.py` via `python-dotenv`.

See the root `README.md` for full setup and run instructions.