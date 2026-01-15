import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
def call_model(prompt: str, max_tokens=4000, temperature=0.1) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response.choices[0].message.content


def judge_story(story: str) -> dict:
    """
    Uses the LLM as a judge to evaluate story quality and safety.
    Returns a structured JSON-like dictionary.
    """

    judge_prompt = f"""
You are a careful evaluator of children's bedtime stories for ages 5 to 10.

Evaluate the story below using these criteria:
1. Age appropriateness (vocabulary and concepts)
2. Emotional safety (no fear, violence, or distress)
3. Clear story structure:
   - The story has 7 paragraphs
   - Each paragraph serves a distinct role:
     setup, normal routine, problem, first attempt, learning moment, resolution, lesson
4. Clear positive lesson or moral
5. Simple, easy-to-follow language

Story:
\"\"\"{story}\"\"\"

Respond ONLY in valid JSON with the following keys:
- age_appropriateness: "pass" or "fail"
- emotional_safety: "pass" or "fail"
- story_structure: "pass" or "fail"
- lesson_clarity: "pass" or "fail"
- language_simplicity: "pass" or "fail"
- narrative_engagement: "pass" or "fail"
- suggestions: a short list of concrete improvements
"""

    response = call_model(judge_prompt, max_tokens=500, temperature=0.0)

    try:
        import json
        return json.loads(response)
    except Exception:
        # Fallback in case the model returns malformed JSON
        return {
            "age_appropriateness": "fail",
            "emotional_safety": "fail",
            "story_structure": "fail",
            "lesson_clarity": "fail",
            "language_simplicity": "fail",
            "narrative_engagement": "fail",
            "suggestions": ["Judge response was not valid JSON."]
        }

def revise_story(original_story: str, judge_feedback: dict) -> str:
    """
    Revises the story based on judge feedback.
    Only one revision pass is performed.
    """

    revision_prompt = f"""
You are improving a bedtime story for a child aged 5 to 10.

Here is the original story:
\"\"\"{original_story}\"\"\"

Here is feedback from a story evaluator:
{judge_feedback}

Revise the story to address the feedback.
Guidelines:
- Keep the story gentle and emotionally safe
- Use simple words and short sentences
- Ensure a clear beginning, middle, and end
- End with a positive lesson

Return ONLY the revised story.
"""

    return call_model(revision_prompt, max_tokens=4000, temperature=0.3)

def build_story_prompt(user_request: str) -> str:
    return f"""
You are a gentle and creative storyteller for children aged 5 to 10.

Your task is to write a bedtime story based on the user's request.

CRITICAL SAFETY RULES:
- The story MUST be emotionally safe.
- No violence, hitting, bullying, or harm.
- Unsafe requests must be reinterpreted safely.

STORY STRUCTURE REQUIREMENTS:
- The story MUST have 7 short paragraphs:
  1. Setup: introduce characters and setting
  2. Normal routine: show everyday life
  3. Problem: a gentle challenge appears
  4. First attempt: an idea that does not fully work
  5. Learning moment: characters adjust their approach
  6. Resolution: the problem is solved positively
  7. Lesson: reflect and end calmly
- Each paragraph should have 3–5 simple sentences.
- The story should feel calm and unhurried.


STYLE REQUIREMENTS:
- Tone: warm, calm, and positive
- Language: simple words, short sentences
- Length: 7 short paragraphs
- End with a clear, positive lesson

User request:
\"\"\"{user_request}\"\"\"

Only return the story.
"""



def main():
    user_input = input("What kind of story do you want to hear?\n ")

    # First pass story
    story_prompt = build_story_prompt(user_input)
    story = call_model(story_prompt)

    # Judge the story
    feedback = judge_story(story)

    print("\n--- Judge Feedback ---")
    print(feedback)

    # Check if any category failed
    needs_revision = any(
        feedback[key] == "fail"
        for key in [
            "age_appropriateness",
            "emotional_safety",
            "story_structure",
            "lesson_clarity",
            "language_simplicity",
            "narrative_engagement",
        ]
    )

    if needs_revision:
        story = revise_story(story, feedback)

    print("\n--- Final Story ---")
    print(story)



if __name__ == "__main__":
    main()
