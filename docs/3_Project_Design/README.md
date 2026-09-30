# Project Design Phase

## Architectural Flow

Start (User opens EduGenie)
        |
        v
Frontend: User Input
        |
        v
FastAPI Backend: routes request to correct endpoint
        |
        v
  -------------------------------------------------------------
  |          |               |               |                |
Explanation  Q&A          Quiz Generation  Summarization   Learning Path
Module       Module       Module           Module          Module
(/explain)   (/qa)        (/quiz)          (/summarize)    (/learn/recommendations)
  -------------------------------------------------------------
        |
        v
Frontend: Display Results
        |
        v
End (Results shown, user interacts again)

## Folder Architecture

EduGenie/
- main.py                  -> FastAPI app & routes
- explanation_module.py    -> Concept explanation logic
- qna.py                   -> Question answering
- quiz_module.py           -> Quiz generation
- summary_module.py        -> Summarization
- learning_path.py         -> Learning recommendations
- templates/index.html     -> HTML frontend
- static/style.css         -> Styling
- requirements.txt         -> Python dependencies

## Design Decisions

- Modular structure: each AI feature lives in its own Python file so
  it can be tested, debugged, or swapped independently.
- Single-page frontend: all 5 features are accessible via tabs on one
  HTML page rather than separate pages, keeping navigation simple.
- REST API design: each module is exposed through a dedicated FastAPI
  endpoint, following standard REST conventions (GET for reads, POST for
  actions that submit data).