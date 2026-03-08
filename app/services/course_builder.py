"""
Course Builder Service — combines Profile + Search + Curriculum into CourseJSON.

Like Adiyogi's Storyboard service that produces final ProductionJSON,
this service orchestrates the full pipeline and stores the result.

Pipeline: Profile → Search → Curriculum → CourseJSON (stored)
"""

import time
from typing import Dict, Optional
from app.models import (
    CourseJSON, CourseStatus, LearnerProfile,
    IndexedCourse, CurriculumModule,
)
from app.services import search, curriculum

# In-memory store (replace with Cosmos DB / DynamoDB in production)
COURSE_DB: Dict[str, CourseJSON] = {}


async def create_course(
    profile: LearnerProfile,
    topic: str = "AI and Machine Learning",
) -> CourseJSON:
    """
    Full course creation pipeline.
    1. Search for matching courses
    2. Design curriculum
    3. Build and store CourseJSON
    """
    # Create initial course shell
    course = CourseJSON(
        status=CourseStatus.SEARCHING,
        learner=profile,
        skill_level=profile.level or "beginner",
    )

    # Step 1: Search for courses
    matched = await search.search_courses(
        query=profile.goal or topic,
        profile=profile,
        max_results=15,
    )
    course.matched_courses = matched
    course.status = CourseStatus.DESIGNING

    # Step 2: Design curriculum
    curriculum_data = curriculum.design_curriculum(
        profile=profile,
        courses=matched,
        topic=topic,
    )

    # Step 3: Build CourseJSON
    course.title = curriculum_data.get("title", f"{topic} Course")
    course.description = curriculum_data.get("description", "")
    course.estimated_duration = curriculum_data.get("estimated_duration", "")
    course.skill_level = curriculum_data.get("skill_level", profile.level)
    course.tips = curriculum_data.get("tips", [])
    course.adaptive_notes = curriculum_data.get("adaptive_notes", "")

    # Parse modules
    for mod_data in curriculum_data.get("modules", []):
        mod_courses = []
        for c in mod_data.get("courses", []):
            try:
                mod_courses.append(IndexedCourse(**c))
            except Exception:
                pass

        module = CurriculumModule(
            module_number=mod_data.get("module_number", 0),
            title=mod_data.get("title", ""),
            objective=mod_data.get("objective", ""),
            duration=mod_data.get("duration", ""),
            topics=mod_data.get("topics", []),
            courses=mod_courses,
            practice=mod_data.get("practice", []),
            assessment=mod_data.get("assessment", ""),
            prerequisites=mod_data.get("prerequisites", []),
        )
        course.modules.append(module)

    # Set thumbnail from first matched course
    if matched and matched[0].thumbnail:
        course.thumbnail = matched[0].thumbnail

    course.status = CourseStatus.READY
    course.updated_at = time.time()

    # Store
    COURSE_DB[course.id] = course
    return course


def get_course(course_id: str) -> Optional[CourseJSON]:
    """Retrieve a stored course."""
    return COURSE_DB.get(course_id)


def list_courses() -> list[CourseJSON]:
    """List all stored courses."""
    return sorted(COURSE_DB.values(), key=lambda c: c.created_at, reverse=True)


def update_progress(course_id: str, module_number: int) -> Optional[CourseJSON]:
    """Mark a module as completed."""
    course = COURSE_DB.get(course_id)
    if not course:
        return None

    if module_number not in course.completed_modules:
        course.completed_modules.append(module_number)

    if len(course.completed_modules) >= len(course.modules):
        course.status = CourseStatus.COMPLETED
    else:
        course.status = CourseStatus.IN_PROGRESS

    course.updated_at = time.time()
    return course
