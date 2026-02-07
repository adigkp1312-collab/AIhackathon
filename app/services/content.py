"""
Content aggregation service.

Searches free learning content from YouTube, NPTEL, and other open sources.
Uses YouTube Data API when available, falls back to curated demo results.
"""

import httpx
from app.config import settings

# Curated free learning sources for India
FREE_SOURCES = {
    "youtube_hindi": [
        {"channel": "CodeWithHarry", "topics": ["python", "web", "dsa", "programming"]},
        {"channel": "Apna College", "topics": ["web", "dsa", "java", "programming"]},
        {"channel": "CampusX", "topics": ["machine learning", "data science", "python"]},
        {"channel": "Chai aur Code", "topics": ["javascript", "react", "web", "backend"]},
        {"channel": "Telusko", "topics": ["python", "java", "spring", "programming"]},
        {"channel": "Love Babbar", "topics": ["dsa", "competitive programming", "cpp"]},
        {"channel": "Striver (take U forward)", "topics": ["dsa", "competitive programming"]},
        {"channel": "Gate Smashers", "topics": ["gate", "os", "dbms", "networking"]},
        {"channel": "5 Minutes Engineering", "topics": ["gate", "engineering", "theory"]},
        {"channel": "Physics Wallah", "topics": ["physics", "chemistry", "maths", "jee", "neet"]},
    ],
    "nptel": {
        "base_url": "https://nptel.ac.in",
        "description": "Free IIT/IISc courses with certificates",
    },
    "other_free": [
        {"name": "Khan Academy", "url": "https://www.khanacademy.org", "languages": ["English", "Hindi"]},
        {"name": "freeCodeCamp", "url": "https://www.freecodecamp.org", "languages": ["English"]},
        {"name": "MIT OpenCourseWare", "url": "https://ocw.mit.edu", "languages": ["English"]},
        {"name": "Coursera (Audit)", "url": "https://www.coursera.org", "languages": ["English"]},
        {"name": "SWAYAM", "url": "https://swayam.gov.in", "languages": ["English", "Hindi"]},
        {"name": "Google Digital Garage", "url": "https://learndigital.withgoogle.com", "languages": ["English", "Hindi"]},
    ],
}


async def search_youtube(query: str, max_results: int = 5) -> list:
    """
    Search YouTube for free learning content.
    Uses YouTube Data API if configured, otherwise returns curated results.
    """
    if settings.YOUTUBE_API_KEY:
        return await _youtube_api_search(query, max_results)
    return _curated_youtube_results(query, max_results)


async def _youtube_api_search(query: str, max_results: int) -> list:
    """Search using YouTube Data API v3."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "q": f"{query} free course tutorial",
                    "type": "video",
                    "maxResults": max_results,
                    "key": settings.YOUTUBE_API_KEY,
                    "relevanceLanguage": "en",
                    "videoDuration": "long",
                },
            )
            data = response.json()
            results = []
            for item in data.get("items", []):
                results.append(
                    {
                        "title": item["snippet"]["title"],
                        "channel": item["snippet"]["channelTitle"],
                        "video_id": item["id"]["videoId"],
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                        "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                        "description": item["snippet"]["description"][:200],
                    }
                )
            return results
    except Exception as e:
        print(f"YouTube API error: {e}")
        return _curated_youtube_results(query, max_results)


def _curated_youtube_results(query: str, max_results: int) -> list:
    """Return curated results based on topic matching."""
    query_lower = query.lower()
    results = []

    topic_map = {
        "python": [
            {
                "title": "Python Tutorial for Beginners (Full Course) - CodeWithHarry",
                "channel": "CodeWithHarry",
                "video_id": "demo1",
                "url": "https://www.youtube.com/results?search_query=CodeWithHarry+Python+Tutorial+Hindi",
                "thumbnail": "",
                "description": "Complete Python course in Hindi - 12+ hours, beginner friendly",
            },
            {
                "title": "Python for Everybody - Full University Course (freeCodeCamp)",
                "channel": "freeCodeCamp",
                "video_id": "demo2",
                "url": "https://www.youtube.com/results?search_query=Python+for+Everybody+freeCodeCamp",
                "thumbnail": "",
                "description": "University of Michigan Python course - completely free",
            },
        ],
        "machine learning": [
            {
                "title": "100 Days of Machine Learning - CampusX (Hindi)",
                "channel": "CampusX",
                "video_id": "demo3",
                "url": "https://www.youtube.com/results?search_query=CampusX+100+days+machine+learning",
                "thumbnail": "",
                "description": "Comprehensive ML course in Hindi with daily videos",
            },
            {
                "title": "Machine Learning Specialization - Andrew Ng",
                "channel": "Stanford Online",
                "video_id": "demo4",
                "url": "https://www.youtube.com/results?search_query=Andrew+Ng+Machine+Learning+2024",
                "thumbnail": "",
                "description": "The gold standard ML course from Stanford, free on YouTube",
            },
        ],
        "web": [
            {
                "title": "Web Development Complete Course - Apna College (Hindi)",
                "channel": "Apna College",
                "video_id": "demo5",
                "url": "https://www.youtube.com/results?search_query=Apna+College+Web+Development+Hindi",
                "thumbnail": "",
                "description": "Full stack web dev in Hindi - HTML, CSS, JS, React, Node",
            },
        ],
        "javascript": [
            {
                "title": "JavaScript Full Course - Chai aur Code (Hindi)",
                "channel": "Chai aur Code",
                "video_id": "demo6",
                "url": "https://www.youtube.com/results?search_query=Chai+aur+Code+JavaScript+Hindi",
                "thumbnail": "",
                "description": "Complete JavaScript course in Hindi with projects",
            },
        ],
    }

    for topic, videos in topic_map.items():
        if topic in query_lower:
            results.extend(videos)

    if not results:
        results.append(
            {
                "title": f"Search YouTube for: {query}",
                "channel": "YouTube Search",
                "video_id": "search",
                "url": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}+free+course+tutorial",
                "thumbnail": "",
                "description": f"Find free courses on {query} from top YouTube educators",
            }
        )

    return results[:max_results]


def get_free_sources():
    """Return the curated list of free learning sources."""
    return FREE_SOURCES
