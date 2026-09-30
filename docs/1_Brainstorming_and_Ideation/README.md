# Brainstorming & Ideation Phase

## Problem Identified
Students across academic levels struggle with:
- Fragmented learning tools (separate apps for Q&A, quizzes, summaries, study plans)
- Complex concepts explained in overly technical language
- Lack of personalized, structured guidance on how to learn a new topic
- Limited access to affordable, on-demand tutoring support

## Idea
Build **EduGenie** — a single, lightweight AI-powered educational assistant
that combines five core learning needs into one tool:
1. Ask questions and get smart, concise answers
2. Understand complex concepts through simplified explanations
3. Generate quizzes from any topic or text
4. Receive personalized, structured learning recommendations
5. Summarize long educational passages

## Why Google Gemini
- Advanced reasoning and strong instruction-following
- Structured JSON output support (needed for quiz generation)
- Reliable cloud inference, removing the need for expensive local hardware
- Free-tier access suitable for a student project

## Target Users
- Self-learners and students of all academic levels
- Educational institutions and content platforms
- Learners with minimal technical background or hardware resources

## Why This Approach
A single web interface (FastAPI + HTML/CSS) keeps the tool lightweight,
runs well on modest hardware (e.g. Mac M1), and can be accessed from any
device with a browser — no installation required for end users.