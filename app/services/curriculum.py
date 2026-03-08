"""
Curriculum Designer Service — designs adaptive learning paths.

Like Adiyogi's Scene Service that breaks a story into visual scenes,
this service takes search results + learner profile and DESIGNS
a structured curriculum with modules, assessments, and progression.

This is NOT suggestion — it's intelligent course DESIGN.
"""

import json
from google import genai
from app.config import settings
from app.models import LearnerProfile, IndexedCourse, CurriculumModule

CURRICULUM_PROMPT = """You are an expert AI/ML curriculum designer at Adiyogi AI Education.

TASK: Design a structured, adaptive learning curriculum for this learner using ONLY the real courses provided.

LEARNER PROFILE:
- Name: {name}
- Goal: {goal}
- Prior Knowledge: {prior_knowledge}
- Weak Areas: {weak_areas}
- Level: {level}
- Available Time: {hours_per_week} hours/week
- Deadline: {deadline}
- Learning Style: {learning_style}
- Education: {education}
- Language: {language}

AVAILABLE COURSES (from our verified index — use ONLY these):
{courses_json}

DESIGN REQUIREMENTS:
1. Create {num_modules} modules that build progressively
2. Each module must use real courses from the list above (reference by their exact title and URL)
3. Design clear learning objectives ("By end of this module, you will...")
4. Add hands-on practice for each module (coding exercises, projects)
5. Add an assessment/milestone for each module
6. Consider the learner's weak areas — add remedial content where needed
7. Respect their available time — don't overload
8. If they prefer Hindi, prioritize Hindi courses
9. Make it adaptive: if they know Python already, skip basics

Return JSON:
{{
  "title": "Course title — specific to their goal",
  "description": "What they'll achieve",
  "estimated_duration": "e.g. 6 weeks",
  "skill_level": "{level}",
  "modules": [
    {{
      "module_number": 1,
      "title": "Module title",
      "objective": "By end of this module, you will be able to...",
      "duration": "1 week",
      "topics": ["topic1", "topic2"],
      "courses": [
        // Include FULL course objects from the available list
        {{"title": "...", "provider": "...", "platform": "...", "url": "...", "thumbnail": "...", "description": "...", "duration": "...", "level": "...", "language": "...", "topics": [...], "free": true}}
      ],
      "practice": ["Exercise 1 description", "Exercise 2 description"],
      "assessment": "Build X / Complete Y / Solve Z",
      "prerequisites": []
    }}
  ],
  "tips": ["Adaptive tip based on their profile"],
  "adaptive_notes": "Why this path was designed this way for THIS specific learner"
}}"""


def _get_client():
    if settings.GOOGLE_API_KEY:
        return genai.Client(api_key=settings.GOOGLE_API_KEY)
    return genai.Client(vertexai=True)


def design_curriculum(
    profile: LearnerProfile,
    courses: list[IndexedCourse],
    topic: str = "AI and Machine Learning",
) -> dict:
    """
    Design an adaptive curriculum from search results + profile.
    Returns structured curriculum data.
    """
    try:
        client = _get_client()

        # Decide number of modules based on available time
        hours = profile.available_hours_per_week or 10
        if hours <= 5:
            num_modules = 4
        elif hours <= 10:
            num_modules = 6
        else:
            num_modules = 8

        courses_json = json.dumps(
            [c.model_dump() for c in courses],
            indent=2,
        )

        lang_map = {"hi-IN": "Hindi", "ta-IN": "Tamil", "te-IN": "Telugu", "en-IN": "English"}

        prompt = CURRICULUM_PROMPT.format(
            name=profile.name or "Learner",
            goal=profile.goal or topic,
            prior_knowledge=", ".join(profile.prior_knowledge) if profile.prior_knowledge else "None specified",
            weak_areas=", ".join(profile.weak_areas) if profile.weak_areas else "None specified",
            level=profile.level or "beginner",
            hours_per_week=hours,
            deadline=profile.deadline or "No specific deadline",
            learning_style=profile.learning_style or "visual",
            education=profile.education_background or "Not specified",
            language=lang_map.get(profile.preferred_language, "English"),
            courses_json=courses_json,
            num_modules=num_modules,
        )

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json", "temperature": 0.7},
        )

        return json.loads(response.text)

    except Exception as e:
        print(f"[CURRICULUM] Design failed: {e}")
        # Fallback: simple module-per-course design
        return _fallback_curriculum(profile, courses, topic)


def _fallback_curriculum(
    profile: LearnerProfile,
    courses: list[IndexedCourse],
    topic: str,
) -> dict:
    """Simple fallback curriculum when Gemini is unavailable."""
    modules = []
    for i, course in enumerate(courses[:6], 1):
        modules.append({
            "module_number": i,
            "title": course.title,
            "objective": f"Complete {course.title} and understand {', '.join(course.topics[:2])}",
            "duration": course.duration or "1 week",
            "topics": course.topics,
            "courses": [course.model_dump()],
            "practice": [f"Practice exercises from {course.title}"],
            "assessment": f"Complete all exercises in {course.title}",
            "prerequisites": [str(i - 1)] if i > 1 else [],
        })

    return {
        "title": f"{topic} Learning Path for {profile.name or 'You'}",
        "description": f"A structured path to learn {topic} from free resources",
        "estimated_duration": f"{len(modules)} weeks",
        "skill_level": profile.level or "beginner",
        "modules": modules,
        "tips": [
            "Study consistently — even 30 minutes daily is better than cramming",
            "Build projects alongside courses to solidify understanding",
            "Join online communities for doubt-solving",
        ],
        "adaptive_notes": "Fallback curriculum — courses ordered by difficulty",
    }
