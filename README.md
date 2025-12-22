# AI – Bedtime Story Generator

This project is a Python-based bedtime story generator that creates safe, engaging stories for children aged 5–10.  
It uses an LLM storyteller guided by explicit safety and narrative constraints, along with an LLM-based judge to evaluate and improve story quality.

The goal of this assignment is to demonstrate prompt design, agent-style evaluation, and safe content generation in an open-ended setting.

---

## Key Features

- **Age-appropriate storytelling (5–10 years)**  
  Stories use simple language, gentle themes, and a calm tone.

- **Explicit narrative structure**  
  Stories follow a fixed multi-paragraph arc (setup, problem, attempts, resolution, lesson) to ensure a meaningful plot.

- **Safety-first prompting**  
  User requests are treated as intent. Unsafe elements (e.g., violence) are safely reinterpreted rather than followed.

- **LLM Judge for Quality Control**  
  A separate LLM evaluates stories for:
  - Age appropriateness
  - Emotional safety
  - Narrative structure
  - Lesson clarity
  - Language simplicity

- **Single-pass revision loop**  
  If the judge detects issues, the story is revised once using structured feedback.

---

## How It Works (High Level)

1. The user provides a simple story idea.
2. The system builds a structured storyteller prompt with safety and narrative constraints.
3. The LLM generates a story.
4. A second LLM acts as a judge and evaluates the story.
5. If needed, the story is revised once and returned as the final output.

---

## Setup Instructions

### 1. Create and activate a virtual environment
### 2. Add your OpenAI api key to .env file
### 3. Install dependencies:
   **pip install -r requirements.txt**
### 4. Run python main.py
   **Example input : Story with a cat and a mouse.**

