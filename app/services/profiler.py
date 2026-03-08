"""
Profiler Service — collects detailed learner information.

Like Adiyogi's Director service that refines project briefs,
this service chats with the learner to understand their:
- Goal, prior knowledge, weak areas
- Available time, deadline, learning style
- Education background

Returns a complete LearnerProfile.
"""

import json
from google import genai
from app.config import settings
from app.models import LearnerProfile

PROFILER_PROMPT = """You are Adiyogi AI Education's learner profiler.
Your job is to understand the learner deeply so we can design the PERFECT course for them.

You are having a conversation to collect this information:
1. **Goal**: What exactly do they want to achieve? Be specific.
2. **Prior Knowledge**: What do they already know? List specific skills/topics.
3. **Weak Areas**: What do they struggle with?
4. **Available Time**: How many hours per week can they study?
5. **Deadline**: Any time pressure? (exam date, job switch, etc.)
6. **Learning Style**: Do they prefer videos, reading, hands-on coding, or mixed?
7. **Education Background**: Their current education level and field.
8. **Language Preference**: Hindi, English, or regional?

CURRENT PROFILE STATE:
{profile_json}

CONVERSATION SO FAR:
{history}

USER'S LATEST MESSAGE:
{message}

Respond with JSON:
{{
  "reply": "Your conversational response — friendly, Hindi-English mix OK. Ask the NEXT missing piece of info.",
  "profile_update": {{
    // Only include fields that the user just provided info about
    // e.g. "goal": "become an ML engineer" if they just told you their goal
  }},
  "is_complete": false  // true ONLY when you have enough info to design a course
}}

Be conversational. Ask ONE thing at a time. Use Hinglish naturally.
If they give vague answers, probe deeper. "Python seekhna hai" → ask what level, what for."""


def _get_client():
    if settings.GOOGLE_API_KEY:
        return genai.Client(api_key=settings.GOOGLE_API_KEY)
    return genai.Client(vertexai=True)


def profile_chat(message: str, current_profile: LearnerProfile, history: list[dict]) -> dict:
    """
    Chat with learner to build their profile.
    Returns: {reply, profile_update, is_complete}
    """
    try:
        client = _get_client()

        profile_json = current_profile.model_dump_json(indent=2)
        history_text = "\n".join(
            f"{m.get('role', 'user')}: {m.get('content', '')}"
            for m in history[-10:]
        )

        prompt = PROFILER_PROMPT.format(
            profile_json=profile_json,
            history=history_text,
            message=message,
        )

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )

        result = json.loads(response.text)
        return {
            "reply": result.get("reply", "Tell me more about what you want to learn!"),
            "profile_update": result.get("profile_update", {}),
            "is_complete": result.get("is_complete", False),
        }

    except Exception as e:
        print(f"[PROFILER] Error: {e}")
        return {
            "reply": "Interesting! Tell me more — what's your main learning goal?",
            "profile_update": {},
            "is_complete": False,
        }


def merge_profile(current: LearnerProfile, update: dict) -> LearnerProfile:
    """Merge partial profile update into existing profile."""
    data = current.model_dump()
    for key, value in update.items():
        if key in data and value:
            if isinstance(data[key], list) and isinstance(value, list):
                data[key] = list(set(data[key] + value))
            else:
                data[key] = value
    return LearnerProfile(**data)
