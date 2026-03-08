"""
Search Service — finds real AI courses via Vertex AI Search + YouTube.

Like Adiyogi's Grounded Gen that retrieves reference content from
Vertex AI Search datastores, this service searches our indexed
AI course database for the most relevant courses.

Fallback chain:
1. Vertex AI Search (indexed course catalog)
2. YouTube Data API (live search)
3. Curated demo results
"""

import json
from google import genai
from google.genai import types
from app.config import settings
from app.models import IndexedCourse, LearnerProfile

# Vertex AI Search engine path (to be created via setup script)
EDUCATION_ENGINE = (
    f"projects/{settings.GCP_PROJECT_ID}/locations/global"
    f"/collections/default_collection/engines/ai_education_engine"
)


def _get_client():
    if settings.GOOGLE_API_KEY:
        return genai.Client(api_key=settings.GOOGLE_API_KEY)
    return genai.Client(vertexai=True)


async def search_courses(
    query: str,
    profile: LearnerProfile,
    max_results: int = 10,
) -> list[IndexedCourse]:
    """
    Search for AI courses matching the learner's needs.
    Tries Vertex AI Search → YouTube → curated fallback.
    """
    # Build search query enriched with profile context
    enriched_query = _build_search_query(query, profile)

    # Try Vertex AI Search first
    courses = await _vertex_search(enriched_query, profile, max_results)
    if courses:
        return courses

    # Fallback to YouTube
    courses = await _youtube_search(enriched_query, max_results)
    if courses:
        return courses

    # Final fallback — curated AI courses
    return _curated_ai_courses(profile)


def _build_search_query(query: str, profile: LearnerProfile) -> str:
    """Enrich query with profile context for better search."""
    parts = [query]
    if profile.level:
        parts.append(f"{profile.level} level")
    if profile.preferred_language != "en-IN":
        lang_map = {"hi-IN": "Hindi", "ta-IN": "Tamil", "te-IN": "Telugu"}
        lang = lang_map.get(profile.preferred_language, "")
        if lang:
            parts.append(lang)
    if "hands-on" in profile.learning_style:
        parts.append("with projects")
    return " ".join(parts)


async def _vertex_search(
    query: str,
    profile: LearnerProfile,
    max_results: int,
) -> list[IndexedCourse]:
    """Search indexed courses via Vertex AI Search with grounded generation."""
    try:
        client = _get_client()

        grounding_tool = types.Tool(
            retrieval=types.Retrieval(
                vertexAiSearch=types.VertexAISearch(engine=EDUCATION_ENGINE)
            )
        )

        prompt = f"""Find the {max_results} most relevant free AI/ML courses for this learner:
Goal: {profile.goal or query}
Level: {profile.level}
Prior knowledge: {', '.join(profile.prior_knowledge) if profile.prior_knowledge else 'none specified'}

Return ONLY a JSON array of courses found in the knowledge base:
[{{"title": "...", "provider": "...", "platform": "...", "url": "...", "thumbnail": "...", "description": "...", "duration": "...", "level": "...", "language": "...", "topics": [...], "free": true}}]"""

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[grounding_tool],
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )

        courses_data = json.loads(response.text)
        if isinstance(courses_data, list):
            return [IndexedCourse(**c) for c in courses_data[:max_results]]
        return []

    except Exception as e:
        print(f"[SEARCH] Vertex AI Search failed: {e}")
        return []


async def _youtube_search(query: str, max_results: int) -> list[IndexedCourse]:
    """Search YouTube for free AI courses."""
    if not settings.YOUTUBE_API_KEY:
        return []

    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "q": f"{query} free course tutorial AI",
                    "type": "video",
                    "maxResults": max_results,
                    "key": settings.YOUTUBE_API_KEY,
                    "relevanceLanguage": "en",
                    "videoDuration": "long",
                },
            )
            data = response.json()
            courses = []
            for item in data.get("items", []):
                vid = item["id"]["videoId"]
                snippet = item["snippet"]
                courses.append(IndexedCourse(
                    id=vid,
                    title=snippet["title"],
                    provider=snippet["channelTitle"],
                    platform="youtube",
                    url=f"https://www.youtube.com/watch?v={vid}",
                    thumbnail=snippet["thumbnails"]["medium"]["url"],
                    description=snippet["description"][:200],
                    language="English",
                    topics=[query.split()[0] if query else "AI"],
                    free=True,
                ))
            return courses
    except Exception as e:
        print(f"[SEARCH] YouTube search failed: {e}")
        return []


def _curated_ai_courses(profile: LearnerProfile) -> list[IndexedCourse]:
    """Curated AI course catalog — always available as fallback."""
    level = profile.level or "beginner"

    ALL_COURSES = [
        # Beginner
        IndexedCourse(id="cwh-ml", title="Machine Learning in Hindi - Full Course", provider="CodeWithHarry", platform="youtube", url="https://www.youtube.com/watch?v=7uwa9aPbBRU", thumbnail="https://i.ytimg.com/vi/7uwa9aPbBRU/mqdefault.jpg", description="Complete ML course in Hindi covering all fundamentals with Python examples", duration="12 hours", level="beginner", language="Hindi", topics=["machine learning", "python", "scikit-learn"], free=True),
        IndexedCourse(id="cwh-python", title="Python Tutorial for Beginners (Full Course)", provider="CodeWithHarry", platform="youtube", url="https://www.youtube.com/watch?v=7wnove7K-ZQ", thumbnail="https://i.ytimg.com/vi/7wnove7K-ZQ/mqdefault.jpg", description="Complete Python course in Hindi — beginner to advanced", duration="14 hours", level="beginner", language="Hindi", topics=["python", "programming"], free=True),
        IndexedCourse(id="3b1b-nn", title="Neural Networks (3Blue1Brown)", provider="3Blue1Brown", platform="youtube", url="https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi", thumbnail="https://i.ytimg.com/vi/aircAruvnKk/mqdefault.jpg", description="Beautiful visual explanations of how neural networks learn", duration="4 hours", level="beginner", language="English", topics=["neural networks", "deep learning", "math"], free=True),
        IndexedCourse(id="fcc-ml", title="Machine Learning for Everybody", provider="freeCodeCamp", platform="youtube", url="https://www.youtube.com/watch?v=i_LwzRVP7bg", thumbnail="https://i.ytimg.com/vi/i_LwzRVP7bg/mqdefault.jpg", description="Full university-level ML course — no math prerequisites", duration="10 hours", level="beginner", language="English", topics=["machine learning", "python"], free=True),
        IndexedCourse(id="campusx-100", title="100 Days of Machine Learning", provider="CampusX", platform="youtube", url="https://www.youtube.com/playlist?list=PLKnIA16OIAGMGda7kJ2GyiQ1cHSv0cYEo", thumbnail="https://i.ytimg.com/vi/7uwa9aPbBRU/mqdefault.jpg", description="Comprehensive Hindi ML bootcamp — 100 daily videos", duration="100 hours", level="beginner", language="Hindi", topics=["machine learning", "data science", "python"], free=True),
        # Intermediate
        IndexedCourse(id="stanford-cs229", title="Stanford CS229: Machine Learning", provider="Stanford Online", platform="youtube", url="https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU", thumbnail="https://i.ytimg.com/vi/jGwO_UgTS7I/mqdefault.jpg", description="Andrew Ng's legendary Stanford ML course — full lectures", duration="20 hours", level="intermediate", language="English", topics=["machine learning", "statistics", "optimization"], free=True),
        IndexedCourse(id="fast-ai", title="Practical Deep Learning for Coders", provider="fast.ai", platform="youtube", url="https://www.youtube.com/playlist?list=PLfYUBJiXbdtSvpQjSnJJ_PmDQB_VyT5iU", thumbnail="https://i.ytimg.com/vi/8SF_h3xF3cE/mqdefault.jpg", description="Top-down approach to deep learning — build first, theory later", duration="30 hours", level="intermediate", language="English", topics=["deep learning", "pytorch", "computer vision", "nlp"], free=True),
        IndexedCourse(id="nptel-dl", title="Deep Learning - NPTEL (IIT Madras)", provider="NPTEL", platform="nptel", url="https://nptel.ac.in/courses/106106213", thumbnail="", description="IIT Madras deep learning course with certificate option", duration="12 weeks", level="intermediate", language="English", topics=["deep learning", "neural networks", "cnn", "rnn"], free=True),
        # Advanced
        IndexedCourse(id="stanford-cs231n", title="Stanford CS231n: CNNs for Visual Recognition", provider="Stanford Online", platform="youtube", url="https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv", thumbnail="https://i.ytimg.com/vi/vT1JzLTH4G4/mqdefault.jpg", description="Deep dive into convolutional neural networks — Andrej Karpathy", duration="20 hours", level="advanced", language="English", topics=["computer vision", "cnn", "deep learning"], free=True),
        IndexedCourse(id="huggingface-nlp", title="HuggingFace NLP Course", provider="HuggingFace", platform="youtube", url="https://huggingface.co/learn/nlp-course", thumbnail="", description="Learn transformers, fine-tuning, and modern NLP from HuggingFace", duration="15 hours", level="advanced", language="English", topics=["nlp", "transformers", "huggingface", "llm"], free=True),
    ]

    # Filter by level — include current + one above
    level_order = {"beginner": 0, "intermediate": 1, "advanced": 2}
    learner_level = level_order.get(level, 0)
    return [
        c for c in ALL_COURSES
        if level_order.get(c.level, 0) <= learner_level + 1
    ]
