"""
API routes for SeekhoFree — Adiyogi AI Education.

Pipeline: Profile -> Search -> Curriculum -> CourseJSON
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models import (
    ProfileInput, CourseCreateRequest, CourseResponse,
    LearnerProfile, CourseJSON,
)
from app.services import bedrock, content, voice, profiler, course_builder

router = APIRouter(prefix="/api")


# --- Legacy endpoints (kept for backward compat) ---

class ChatRequest(BaseModel):
    message: str
    history: list = []


class VoiceRequest(BaseModel):
    audio_base64: str
    language_code: str = "hi-IN"


class TTSRequest(BaseModel):
    text: str
    language_code: str = "hi-IN"


@router.post("/chat")
async def chat(req: ChatRequest):
    """Legacy chat endpoint — generates course plan via Bedrock/Gemini."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    plan = bedrock.generate_course_plan(req.message, req.history)
    youtube_results = []
    if plan.get("type") != "conversation":
        youtube_results = await content.search_youtube(req.message)
    return {"plan": plan, "youtube_results": youtube_results}


@router.post("/voice/stt")
async def speech_to_text(req: VoiceRequest):
    result = await voice.speech_to_text(req.audio_base64, req.language_code)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "STT failed"))
    return result


@router.post("/voice/tts")
async def text_to_speech(req: TTSRequest):
    result = await voice.text_to_speech(req.text, req.language_code)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "TTS failed"))
    return result


@router.get("/languages")
async def get_languages():
    return voice.get_supported_languages()


@router.get("/sources")
async def get_sources():
    return content.get_free_sources()


@router.get("/search")
async def search(q: str, max_results: int = 5):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    results = await content.search_youtube(q, max_results)
    return {"query": q, "results": results}


# --- New Course Pipeline Endpoints ---

@router.post("/course/profile")
async def profile_chat(req: ProfileInput):
    """
    Chat with the learner to build their profile.
    Send messages back and forth until is_complete=true.
    """
    current_profile = req.profile or LearnerProfile()
    history = []

    if req.course_id:
        course = course_builder.get_course(req.course_id)
        if course:
            current_profile = course.learner

    result = profiler.profile_chat(
        message=req.message,
        current_profile=current_profile,
        history=history,
    )

    # Merge any profile updates
    updated_profile = profiler.merge_profile(
        current_profile,
        result.get("profile_update", {}),
    )

    return {
        "reply": result["reply"],
        "profile": updated_profile.model_dump(),
        "is_complete": result["is_complete"],
    }


@router.post("/course/create")
async def create_course(req: CourseCreateRequest):
    """
    Full course creation pipeline.
    Call this after profiling is complete.
    Returns a designed CourseJSON.
    """
    course = await course_builder.create_course(
        profile=req.profile,
        topic=req.topic,
    )
    return CourseResponse(
        course=course,
        message="Course designed successfully!",
    )


@router.get("/course/{course_id}")
async def get_course(course_id: str):
    """Retrieve a stored course by ID."""
    course = course_builder.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseResponse(course=course)


@router.get("/courses")
async def list_courses():
    """List all stored courses."""
    courses = course_builder.list_courses()
    return {"courses": [c.model_dump() for c in courses]}


class ProgressUpdate(BaseModel):
    module_number: int


@router.patch("/course/{course_id}/progress")
async def update_progress(course_id: str, req: ProgressUpdate):
    """Mark a module as completed."""
    course = course_builder.update_progress(course_id, req.module_number)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseResponse(
        course=course,
        message=f"Module {req.module_number} marked as completed",
    )
