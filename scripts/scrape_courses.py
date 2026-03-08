"""
Scrape AI course metadata using Firecrawl and build a JSONL index
for Vertex AI Search ingestion.

Usage:
    pip install firecrawl-py
    export FIRECRAWL_API_KEY=fc-...
    python scripts/scrape_courses.py
"""

import json
import os
import time
from pathlib import Path

try:
    from firecrawl import FirecrawlApp
except ImportError:
    FirecrawlApp = None

OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "ai_courses.jsonl"

# Sources to scrape — YouTube playlists/channels, NPTEL, fast.ai, etc.
SCRAPE_TARGETS = [
    # YouTube channels/playlists with free AI courses
    {"url": "https://www.youtube.com/@CodeWithHarry/playlists", "provider": "CodeWithHarry", "platform": "youtube"},
    {"url": "https://www.youtube.com/@campaboraseries/playlists", "provider": "CampusX", "platform": "youtube"},
    {"url": "https://www.youtube.com/@3blue1brown/playlists", "provider": "3Blue1Brown", "platform": "youtube"},
    {"url": "https://www.youtube.com/@freaboradcamp/playlists", "provider": "freeCodeCamp", "platform": "youtube"},
    {"url": "https://www.youtube.com/@sentdex/playlists", "provider": "sentdex", "platform": "youtube"},
    # Course platforms
    {"url": "https://www.fast.ai/", "provider": "fast.ai", "platform": "fast.ai"},
    {"url": "https://nptel.ac.in/course.html?query=artificial+intelligence", "provider": "NPTEL", "platform": "nptel"},
    {"url": "https://nptel.ac.in/course.html?query=machine+learning", "provider": "NPTEL", "platform": "nptel"},
    {"url": "https://nptel.ac.in/course.html?query=deep+learning", "provider": "NPTEL", "platform": "nptel"},
]

# Curated courses — always included even without Firecrawl
CURATED_COURSES = [
    {"id": "cwh-ml", "title": "Machine Learning in Hindi - Full Course", "provider": "CodeWithHarry", "platform": "youtube", "url": "https://www.youtube.com/watch?v=7uwa9aPbBRU", "thumbnail": "https://i.ytimg.com/vi/7uwa9aPbBRU/mqdefault.jpg", "description": "Complete ML course in Hindi covering all fundamentals with Python examples", "duration": "12 hours", "level": "beginner", "language": "Hindi", "topics": ["machine learning", "python", "scikit-learn"], "free": True},
    {"id": "cwh-python", "title": "Python Tutorial for Beginners (Full Course)", "provider": "CodeWithHarry", "platform": "youtube", "url": "https://www.youtube.com/watch?v=7wnove7K-ZQ", "thumbnail": "https://i.ytimg.com/vi/7wnove7K-ZQ/mqdefault.jpg", "description": "Complete Python course in Hindi — beginner to advanced", "duration": "14 hours", "level": "beginner", "language": "Hindi", "topics": ["python", "programming"], "free": True},
    {"id": "3b1b-nn", "title": "Neural Networks (3Blue1Brown)", "provider": "3Blue1Brown", "platform": "youtube", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi", "thumbnail": "https://i.ytimg.com/vi/aircAruvnKk/mqdefault.jpg", "description": "Beautiful visual explanations of how neural networks learn", "duration": "4 hours", "level": "beginner", "language": "English", "topics": ["neural networks", "deep learning", "math"], "free": True},
    {"id": "fcc-ml", "title": "Machine Learning for Everybody", "provider": "freeCodeCamp", "platform": "youtube", "url": "https://www.youtube.com/watch?v=i_LwzRVP7bg", "thumbnail": "https://i.ytimg.com/vi/i_LwzRVP7bg/mqdefault.jpg", "description": "Full university-level ML course — no math prerequisites", "duration": "10 hours", "level": "beginner", "language": "English", "topics": ["machine learning", "python"], "free": True},
    {"id": "campusx-100", "title": "100 Days of Machine Learning", "provider": "CampusX", "platform": "youtube", "url": "https://www.youtube.com/playlist?list=PLKnIA16OIAGMGda7kJ2GyiQ1cHSv0cYEo", "thumbnail": "https://i.ytimg.com/vi/7uwa9aPbBRU/mqdefault.jpg", "description": "Comprehensive Hindi ML bootcamp — 100 daily videos", "duration": "100 hours", "level": "beginner", "language": "Hindi", "topics": ["machine learning", "data science", "python"], "free": True},
    {"id": "stanford-cs229", "title": "Stanford CS229: Machine Learning", "provider": "Stanford Online", "platform": "youtube", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU", "thumbnail": "https://i.ytimg.com/vi/jGwO_UgTS7I/mqdefault.jpg", "description": "Andrew Ng's legendary Stanford ML course — full lectures", "duration": "20 hours", "level": "intermediate", "language": "English", "topics": ["machine learning", "statistics", "optimization"], "free": True},
    {"id": "fast-ai", "title": "Practical Deep Learning for Coders", "provider": "fast.ai", "platform": "youtube", "url": "https://www.youtube.com/playlist?list=PLfYUBJiXbdtSvpQjSnJJ_PmDQB_VyT5iU", "thumbnail": "https://i.ytimg.com/vi/8SF_h3xF3cE/mqdefault.jpg", "description": "Top-down approach to deep learning — build first, theory later", "duration": "30 hours", "level": "intermediate", "language": "English", "topics": ["deep learning", "pytorch", "computer vision", "nlp"], "free": True},
    {"id": "nptel-dl", "title": "Deep Learning - NPTEL (IIT Madras)", "provider": "NPTEL", "platform": "nptel", "url": "https://nptel.ac.in/courses/106106213", "thumbnail": "", "description": "IIT Madras deep learning course with certificate option", "duration": "12 weeks", "level": "intermediate", "language": "English", "topics": ["deep learning", "neural networks", "cnn", "rnn"], "free": True},
    {"id": "stanford-cs231n", "title": "Stanford CS231n: CNNs for Visual Recognition", "provider": "Stanford Online", "platform": "youtube", "url": "https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv", "thumbnail": "https://i.ytimg.com/vi/vT1JzLTH4G4/mqdefault.jpg", "description": "Deep dive into convolutional neural networks — Andrej Karpathy", "duration": "20 hours", "level": "advanced", "language": "English", "topics": ["computer vision", "cnn", "deep learning"], "free": True},
    {"id": "huggingface-nlp", "title": "HuggingFace NLP Course", "provider": "HuggingFace", "platform": "huggingface", "url": "https://huggingface.co/learn/nlp-course", "thumbnail": "", "description": "Learn transformers, fine-tuning, and modern NLP from HuggingFace", "duration": "15 hours", "level": "advanced", "language": "English", "topics": ["nlp", "transformers", "huggingface", "llm"], "free": True},
    {"id": "mit-intro-ml", "title": "MIT 6.036: Introduction to Machine Learning", "provider": "MIT OpenCourseWare", "platform": "mit_ocw", "url": "https://openlearninglibrary.mit.edu/courses/course-v1:MITx+6.036+1T2019/about", "thumbnail": "", "description": "MIT's introductory ML course with problem sets and exams", "duration": "15 weeks", "level": "intermediate", "language": "English", "topics": ["machine learning", "math", "algorithms"], "free": True},
    {"id": "deeplearning-ai-genai", "title": "Generative AI for Everyone", "provider": "DeepLearning.AI", "platform": "coursera_audit", "url": "https://www.coursera.org/learn/generative-ai-for-everyone", "thumbnail": "", "description": "Andrew Ng explains generative AI — what it is and how to use it", "duration": "5 hours", "level": "beginner", "language": "English", "topics": ["generative ai", "llm", "prompt engineering"], "free": True},
    {"id": "google-ml-crash", "title": "Google Machine Learning Crash Course", "provider": "Google", "platform": "google", "url": "https://developers.google.com/machine-learning/crash-course", "thumbnail": "", "description": "Google's fast-paced ML course with TensorFlow exercises", "duration": "15 hours", "level": "beginner", "language": "English", "topics": ["machine learning", "tensorflow", "google"], "free": True},
    {"id": "karpathy-nn-zero", "title": "Neural Networks: Zero to Hero", "provider": "Andrej Karpathy", "platform": "youtube", "url": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ", "thumbnail": "https://i.ytimg.com/vi/VMj-3S1tku0/mqdefault.jpg", "description": "Build neural networks from scratch — backprop, GPT, tokenizers", "duration": "20 hours", "level": "intermediate", "language": "English", "topics": ["neural networks", "gpt", "transformers", "backpropagation"], "free": True},
    {"id": "statquest-ml", "title": "StatQuest Machine Learning", "provider": "StatQuest", "platform": "youtube", "url": "https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF", "thumbnail": "https://i.ytimg.com/vi/Gv9_4yMHFhI/mqdefault.jpg", "description": "Statistics and ML explained with fun visual animations", "duration": "25 hours", "level": "beginner", "language": "English", "topics": ["machine learning", "statistics", "data science"], "free": True},
]


def scrape_with_firecrawl(target: dict) -> list[dict]:
    """Scrape a URL with Firecrawl and extract course metadata."""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key or not FirecrawlApp:
        return []

    app = FirecrawlApp(api_key=api_key)
    try:
        result = app.scrape(
            target["url"],
            formats=["markdown", "links"],
        )
        # Parse the scraped content for course-like entries
        # This is a simplified extraction — real implementation would use
        # Gemini to parse the markdown into structured course objects
        print(f"[SCRAPE] Got {len(result.get('markdown', ''))} chars from {target['url']}")
        return []  # Parsing would happen here with Gemini
    except Exception as e:
        print(f"[SCRAPE] Failed for {target['url']}: {e}")
        return []


def build_index():
    """Build the JSONL course index."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_courses = list(CURATED_COURSES)

    # Try Firecrawl scraping for each target
    for target in SCRAPE_TARGETS:
        scraped = scrape_with_firecrawl(target)
        all_courses.extend(scraped)
        time.sleep(1)  # Rate limiting

    # Deduplicate by URL
    seen_urls = set()
    unique_courses = []
    for course in all_courses:
        if course["url"] not in seen_urls:
            seen_urls.add(course["url"])
            unique_courses.append(course)

    # Write JSONL for Vertex AI Search import
    with open(OUTPUT_FILE, "w") as f:
        for course in unique_courses:
            f.write(json.dumps(course) + "\n")

    print(f"[INDEX] Wrote {len(unique_courses)} courses to {OUTPUT_FILE}")

    # Also write a JSON version for easy viewing
    json_file = OUTPUT_DIR / "ai_courses.json"
    with open(json_file, "w") as f:
        json.dump(unique_courses, f, indent=2)

    print(f"[INDEX] Also wrote JSON to {json_file}")
    return unique_courses


if __name__ == "__main__":
    build_index()
