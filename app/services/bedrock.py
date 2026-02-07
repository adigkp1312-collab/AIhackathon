"""
AI Course Planner powered by Amazon Bedrock.

Takes a user's learning goal and generates a structured course plan
with modules, topics, and links to free resources.
"""

import json
import boto3
from app.config import settings

SYSTEM_PROMPT = """You are SeekhoFree AI, an expert learning advisor for Indian students and professionals.
Your job is to create structured, free learning plans from publicly available resources.

When a user says what they want to learn, you must:
1. Understand their goal and skill level
2. Break it down into a structured course plan with modules
3. For each module, suggest specific free resources (YouTube channels/playlists, NPTEL courses, MIT OCW, Khan Academy, university lectures, etc.)
4. Prioritize Hindi/regional language content where available, then English
5. Keep it practical and achievable

IMPORTANT: Always respond in valid JSON with this structure:
{
  "title": "Course plan title",
  "description": "Brief description of what the learner will achieve",
  "estimated_duration": "e.g. 4 weeks",
  "skill_level": "beginner/intermediate/advanced",
  "modules": [
    {
      "module_number": 1,
      "title": "Module title",
      "description": "What this module covers",
      "duration": "e.g. 1 week",
      "topics": ["topic1", "topic2"],
      "resources": [
        {
          "title": "Resource title",
          "type": "youtube_video|youtube_playlist|nptel_course|mit_ocw|khan_academy|other",
          "url_hint": "search query or channel name to find this",
          "language": "Hindi|English|Tamil|etc",
          "description": "Why this resource is good"
        }
      ]
    }
  ],
  "tips": ["Practical tip 1", "Practical tip 2"]
}

If the user's message is conversational (greeting, question, etc.), respond with:
{
  "type": "conversation",
  "message": "Your helpful response here"
}
"""


def get_bedrock_client():
    kwargs = {"region_name": settings.AWS_REGION}
    if settings.AWS_ACCESS_KEY_ID:
        kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
    return boto3.client("bedrock-runtime", **kwargs)


def generate_course_plan(user_message: str, conversation_history: list = None) -> dict:
    """
    Use Amazon Bedrock to generate a structured learning plan.
    Falls back to a demo response if Bedrock is not configured.
    """
    messages = []
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    # Try Bedrock first
    if settings.AWS_ACCESS_KEY_ID:
        try:
            client = get_bedrock_client()
            body = json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4096,
                    "system": SYSTEM_PROMPT,
                    "messages": messages,
                }
            )
            response = client.invoke_model(
                modelId=settings.BEDROCK_MODEL_ID,
                contentType="application/json",
                accept="application/json",
                body=body,
            )
            result = json.loads(response["body"].read())
            text = result["content"][0]["text"]
            return json.loads(text)
        except Exception as e:
            print(f"Bedrock error (falling back to demo): {e}")

    # Demo fallback when Bedrock is not configured
    return _demo_course_plan(user_message)


def _demo_course_plan(user_message: str) -> dict:
    """Generate a demo course plan for prototype demonstration."""
    msg = user_message.lower()

    # Simple keyword matching for demo
    if any(word in msg for word in ["hi", "hello", "hey", "namaste"]):
        return {
            "type": "conversation",
            "message": (
                "Namaste! I'm SeekhoFree AI. Tell me what you want to learn "
                "and I'll create a free course plan for you from the best "
                "YouTube, NPTEL, and university resources. For example, try: "
                "'I want to learn Python programming' or "
                "'mujhe machine learning seekhna hai'"
            ),
        }

    if any(word in msg for word in ["python", "programming", "coding"]):
        return _demo_python_plan()
    elif any(word in msg for word in ["machine learning", "ml", "ai", "artificial"]):
        return _demo_ml_plan()
    elif any(word in msg for word in ["web", "html", "css", "javascript", "frontend"]):
        return _demo_web_plan()
    else:
        return _demo_generic_plan(user_message)


def _demo_python_plan():
    return {
        "title": "Python Programming - Zero to Hero",
        "description": "Complete Python course using the best free resources available in Hindi and English",
        "estimated_duration": "6 weeks",
        "skill_level": "beginner",
        "modules": [
            {
                "module_number": 1,
                "title": "Python Basics",
                "description": "Variables, data types, operators, and basic I/O",
                "duration": "1 week",
                "topics": ["Variables", "Data Types", "Operators", "Input/Output", "Strings"],
                "resources": [
                    {
                        "title": "Python Tutorial in Hindi - CodeWithHarry",
                        "type": "youtube_playlist",
                        "url_hint": "CodeWithHarry Python Tutorial Hindi",
                        "language": "Hindi",
                        "description": "Most popular Hindi Python tutorial with 10M+ views",
                    },
                    {
                        "title": "Python for Everybody - Dr. Chuck (University of Michigan)",
                        "type": "youtube_playlist",
                        "url_hint": "Python for Everybody freeCodeCamp",
                        "language": "English",
                        "description": "University-level Python course, completely free on YouTube",
                    },
                ],
            },
            {
                "module_number": 2,
                "title": "Control Flow & Functions",
                "description": "If-else, loops, functions, and modules",
                "duration": "1 week",
                "topics": ["If-Else", "For Loops", "While Loops", "Functions", "Modules"],
                "resources": [
                    {
                        "title": "NPTEL - Programming in Python",
                        "type": "nptel_course",
                        "url_hint": "NPTEL Programming Python IIT",
                        "language": "English",
                        "description": "IIT professor-taught course, free on NPTEL/YouTube",
                    },
                ],
            },
            {
                "module_number": 3,
                "title": "Data Structures in Python",
                "description": "Lists, tuples, dictionaries, sets, and comprehensions",
                "duration": "1 week",
                "topics": ["Lists", "Tuples", "Dictionaries", "Sets", "List Comprehensions"],
                "resources": [
                    {
                        "title": "Python Data Structures - Apna College",
                        "type": "youtube_playlist",
                        "url_hint": "Apna College Python Data Structures",
                        "language": "Hindi",
                        "description": "Clear Hindi explanations with coding practice",
                    },
                ],
            },
            {
                "module_number": 4,
                "title": "OOP & File Handling",
                "description": "Classes, objects, inheritance, and file operations",
                "duration": "1 week",
                "topics": ["Classes", "Objects", "Inheritance", "File I/O", "Exception Handling"],
                "resources": [
                    {
                        "title": "OOP in Python - Telusko",
                        "type": "youtube_playlist",
                        "url_hint": "Telusko Python OOP",
                        "language": "English",
                        "description": "Practical OOP tutorial by Telusko (Indian educator)",
                    },
                ],
            },
            {
                "module_number": 5,
                "title": "Projects & Practice",
                "description": "Build real projects to solidify your learning",
                "duration": "2 weeks",
                "topics": ["Web Scraping", "API Projects", "Automation", "Mini Projects"],
                "resources": [
                    {
                        "title": "12 Python Projects for Beginners - freeCodeCamp",
                        "type": "youtube_video",
                        "url_hint": "freeCodeCamp 12 Python projects beginners",
                        "language": "English",
                        "description": "Hands-on project-based learning, completely free",
                    },
                    {
                        "title": "Python Projects in Hindi - CodeWithHarry",
                        "type": "youtube_playlist",
                        "url_hint": "CodeWithHarry Python projects Hindi",
                        "language": "Hindi",
                        "description": "Build real projects with Hindi explanations",
                    },
                ],
            },
        ],
        "tips": [
            "Practice daily for at least 1 hour - consistency beats intensity",
            "Type every code example yourself, don't just watch",
            "Join the r/learnpython subreddit or Discord for free help",
            "Use Google Colab (free) if you don't have a powerful computer",
        ],
    }


def _demo_ml_plan():
    return {
        "title": "Machine Learning - Beginner to Practitioner",
        "description": "Learn ML from scratch using free courses from IITs, Stanford, and top YouTube educators",
        "estimated_duration": "8 weeks",
        "skill_level": "beginner",
        "modules": [
            {
                "module_number": 1,
                "title": "Math Foundations for ML",
                "description": "Linear algebra, probability, and statistics essentials",
                "duration": "2 weeks",
                "topics": ["Linear Algebra", "Probability", "Statistics", "Calculus Basics"],
                "resources": [
                    {
                        "title": "Mathematics for Machine Learning - 3Blue1Brown",
                        "type": "youtube_playlist",
                        "url_hint": "3Blue1Brown Essence of Linear Algebra",
                        "language": "English",
                        "description": "Beautiful visual explanations of linear algebra",
                    },
                    {
                        "title": "NPTEL - Probability and Statistics (IIT Kharagpur)",
                        "type": "nptel_course",
                        "url_hint": "NPTEL Probability Statistics IIT",
                        "language": "English",
                        "description": "Rigorous IIT course available free on NPTEL",
                    },
                ],
            },
            {
                "module_number": 2,
                "title": "Python for Data Science",
                "description": "NumPy, Pandas, Matplotlib for data handling",
                "duration": "1 week",
                "topics": ["NumPy", "Pandas", "Matplotlib", "Data Cleaning"],
                "resources": [
                    {
                        "title": "Data Science with Python - CampusX (Hindi)",
                        "type": "youtube_playlist",
                        "url_hint": "CampusX Python Data Science Hindi",
                        "language": "Hindi",
                        "description": "Complete Hindi data science course by CampusX",
                    },
                ],
            },
            {
                "module_number": 3,
                "title": "Core Machine Learning",
                "description": "Supervised learning, regression, classification, and evaluation",
                "duration": "3 weeks",
                "topics": [
                    "Linear Regression",
                    "Logistic Regression",
                    "Decision Trees",
                    "SVM",
                    "Model Evaluation",
                ],
                "resources": [
                    {
                        "title": "Machine Learning Specialization - Andrew Ng (Stanford)",
                        "type": "youtube_playlist",
                        "url_hint": "Andrew Ng Machine Learning Coursera free",
                        "language": "English",
                        "description": "The gold standard ML course, available free on YouTube",
                    },
                    {
                        "title": "ML in Hindi - CampusX 100 Days of ML",
                        "type": "youtube_playlist",
                        "url_hint": "CampusX 100 days machine learning Hindi",
                        "language": "Hindi",
                        "description": "Comprehensive Hindi ML course with daily videos",
                    },
                ],
            },
            {
                "module_number": 4,
                "title": "Projects & Kaggle",
                "description": "Apply ML to real datasets and competitions",
                "duration": "2 weeks",
                "topics": ["Kaggle Competitions", "End-to-End Projects", "Model Deployment"],
                "resources": [
                    {
                        "title": "Kaggle Learn - Free ML Micro-Courses",
                        "type": "other",
                        "url_hint": "Kaggle Learn machine learning",
                        "language": "English",
                        "description": "Free hands-on ML courses with real datasets",
                    },
                ],
            },
        ],
        "tips": [
            "Don't skip the math - it makes everything else easier",
            "Use Google Colab for free GPU access",
            "Start with Kaggle's Titanic dataset for your first project",
            "Join AI/ML communities on Discord and Reddit for support",
        ],
    }


def _demo_web_plan():
    return {
        "title": "Web Development - Full Stack Basics",
        "description": "Learn to build websites from scratch with HTML, CSS, JavaScript and React",
        "estimated_duration": "8 weeks",
        "skill_level": "beginner",
        "modules": [
            {
                "module_number": 1,
                "title": "HTML & CSS Fundamentals",
                "description": "Structure and style web pages",
                "duration": "2 weeks",
                "topics": ["HTML5", "CSS3", "Flexbox", "Grid", "Responsive Design"],
                "resources": [
                    {
                        "title": "HTML CSS in Hindi - Shradha Khapra (Apna College)",
                        "type": "youtube_playlist",
                        "url_hint": "Apna College HTML CSS Hindi",
                        "language": "Hindi",
                        "description": "Beginner-friendly web dev course in Hindi",
                    },
                    {
                        "title": "freeCodeCamp Responsive Web Design",
                        "type": "other",
                        "url_hint": "freeCodeCamp responsive web design certification",
                        "language": "English",
                        "description": "Interactive free curriculum with certification",
                    },
                ],
            },
            {
                "module_number": 2,
                "title": "JavaScript",
                "description": "Programming the web - DOM, events, async",
                "duration": "3 weeks",
                "topics": ["JS Basics", "DOM Manipulation", "Events", "Fetch API", "ES6+"],
                "resources": [
                    {
                        "title": "JavaScript in Hindi - Chai aur Code",
                        "type": "youtube_playlist",
                        "url_hint": "Chai aur Code JavaScript Hindi",
                        "language": "Hindi",
                        "description": "Popular Hindi JS series with practical examples",
                    },
                ],
            },
            {
                "module_number": 3,
                "title": "React & Full Stack",
                "description": "Build modern web apps with React",
                "duration": "3 weeks",
                "topics": ["React Basics", "Components", "State", "API Integration", "Deployment"],
                "resources": [
                    {
                        "title": "React in Hindi - Chai aur Code",
                        "type": "youtube_playlist",
                        "url_hint": "Chai aur Code React Hindi",
                        "language": "Hindi",
                        "description": "Complete React course in Hindi",
                    },
                ],
            },
        ],
        "tips": [
            "Build a portfolio website as your first project",
            "Deploy free on Vercel or Netlify",
            "Practice on Frontend Mentor for real design challenges",
        ],
    }


def _demo_generic_plan(topic: str):
    return {
        "title": f"Learning Plan: {topic.title()}",
        "description": f"A structured learning path for {topic} using free resources",
        "estimated_duration": "4-6 weeks",
        "skill_level": "beginner",
        "modules": [
            {
                "module_number": 1,
                "title": "Foundations",
                "description": f"Core concepts and fundamentals of {topic}",
                "duration": "2 weeks",
                "topics": ["Core Concepts", "Fundamentals", "Key Terminology"],
                "resources": [
                    {
                        "title": f"{topic} - Complete Beginner Course (YouTube)",
                        "type": "youtube_playlist",
                        "url_hint": f"{topic} complete course beginner free",
                        "language": "English",
                        "description": "Comprehensive free course on YouTube",
                    },
                    {
                        "title": f"NPTEL / IIT Course on {topic}",
                        "type": "nptel_course",
                        "url_hint": f"NPTEL {topic} IIT course",
                        "language": "English",
                        "description": "University-level course from IIT, free on NPTEL",
                    },
                ],
            },
            {
                "module_number": 2,
                "title": "Intermediate Concepts",
                "description": f"Deeper dive into {topic} with hands-on practice",
                "duration": "2 weeks",
                "topics": ["Advanced Concepts", "Practical Applications", "Case Studies"],
                "resources": [
                    {
                        "title": f"{topic} Hindi Tutorial",
                        "type": "youtube_playlist",
                        "url_hint": f"{topic} tutorial Hindi",
                        "language": "Hindi",
                        "description": "Hindi tutorial for better understanding",
                    },
                ],
            },
            {
                "module_number": 3,
                "title": "Practice & Projects",
                "description": "Apply your knowledge through real projects",
                "duration": "2 weeks",
                "topics": ["Projects", "Portfolio Building", "Community"],
                "resources": [
                    {
                        "title": f"{topic} Projects for Beginners",
                        "type": "youtube_video",
                        "url_hint": f"{topic} projects beginners free",
                        "language": "English",
                        "description": "Project-based learning to build your portfolio",
                    },
                ],
            },
        ],
        "tips": [
            "Consistency is key - practice daily even if just 30 minutes",
            "Join online communities (Reddit, Discord) for support",
            "Teach what you learn to someone else - it helps retention",
            "Use free tools like Google Colab, Replit, or Codespaces for practice",
        ],
    }
