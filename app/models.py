"""
CourseJSON — the education equivalent of ProductionJSON.

Like Adiyogi's script_layer → scenes → storyboard pipeline,
education follows: profile → search → curriculum → CourseJSON.
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import time
import uuid


class CourseStatus(str, Enum):
    PROFILING = "profiling"        # Collecting learner info
    SEARCHING = "searching"        # Finding courses via Vertex AI Search
    DESIGNING = "designing"        # Gemini designing curriculum
    READY = "ready"                # Course built and stored
    IN_PROGRESS = "in_progress"    # Learner started
    COMPLETED = "completed"


class LearnerProfile(BaseModel):
    """Detailed learner info — collected via Profiler service."""
    name: str = ""
    goal: str = ""                          # "I want to become an ML engineer"
    prior_knowledge: list[str] = []         # ["Python basics", "linear algebra"]
    weak_areas: list[str] = []              # ["probability", "calculus"]
    available_hours_per_week: int = 10
    preferred_language: str = "en-IN"       # hi-IN, ta-IN, etc.
    level: str = "beginner"                 # beginner / intermediate / advanced
    learning_style: str = "visual"          # visual / reading / hands-on / video
    deadline: str = ""                      # "3 months", "before GATE 2026"
    education_background: str = ""          # "B.Tech CS 2nd year"


class IndexedCourse(BaseModel):
    """A real course from our Vertex AI Search index."""
    id: str = ""
    title: str
    provider: str                           # "CodeWithHarry", "Stanford Online", "NPTEL"
    platform: str                           # "youtube", "nptel", "coursera_audit", "mit_ocw"
    url: str
    thumbnail: str = ""
    description: str = ""
    duration: str = ""                      # "12 hours", "8 weeks"
    level: str = ""                         # beginner / intermediate / advanced
    language: str = "English"
    topics: list[str] = []
    rating: float = 0.0
    free: bool = True


class CurriculumModule(BaseModel):
    """A designed module — not a suggestion, a designed learning unit."""
    module_number: int
    title: str
    objective: str                          # "By end of this module, you will..."
    duration: str                           # "1 week"
    topics: list[str] = []
    courses: list[IndexedCourse] = []       # Real courses from index
    practice: list[str] = []                # Hands-on exercises
    assessment: str = ""                    # "Build a linear regression model"
    prerequisites: list[str] = []           # Which modules must come before


class CourseJSON(BaseModel):
    """
    The designed course — stored in DB.
    Like ProductionJSON but for education.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    status: CourseStatus = CourseStatus.PROFILING

    # Course meta
    title: str = ""
    description: str = ""
    estimated_duration: str = ""
    skill_level: str = ""
    thumbnail: str = ""

    # The learner
    learner: LearnerProfile = Field(default_factory=LearnerProfile)

    # Designed curriculum
    modules: list[CurriculumModule] = []

    # All matched courses from search (the raw pool)
    matched_courses: list[IndexedCourse] = []

    # Tips / adaptive notes
    tips: list[str] = []
    adaptive_notes: str = ""                # Why this path was chosen

    # Progress tracking
    completed_modules: list[int] = []


# --- Request/Response models for API ---

class ProfileInput(BaseModel):
    """Input for profiler — can be partial, builds up over chat."""
    message: str = ""
    course_id: Optional[str] = None
    profile: Optional[LearnerProfile] = None


class CourseCreateRequest(BaseModel):
    """Full course creation request — after profiling is done."""
    profile: LearnerProfile
    topic: str = "artificial intelligence"


class CourseResponse(BaseModel):
    """API response for a course."""
    course: CourseJSON
    message: str = ""
