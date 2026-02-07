"""
API routes for SeekhoFree.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import bedrock, content, voice

router = APIRouter(prefix="/api")


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
    """
    Main AI chat endpoint.
    Takes a learning query and returns a structured course plan.
    """
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Generate course plan using Bedrock
    plan = bedrock.generate_course_plan(req.message, req.history)

    # If it's a course plan (not conversation), also search for content
    youtube_results = []
    if plan.get("type") != "conversation":
        youtube_results = await content.search_youtube(req.message)

    return {
        "plan": plan,
        "youtube_results": youtube_results,
    }


@router.post("/voice/stt")
async def speech_to_text(req: VoiceRequest):
    """Convert voice audio to text."""
    result = await voice.speech_to_text(req.audio_base64, req.language_code)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "STT failed"))
    return result


@router.post("/voice/tts")
async def text_to_speech(req: TTSRequest):
    """Convert text to voice audio."""
    result = await voice.text_to_speech(req.text, req.language_code)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "TTS failed"))
    return result


@router.get("/languages")
async def get_languages():
    """Get supported Indian languages for voice interaction."""
    return voice.get_supported_languages()


@router.get("/sources")
async def get_sources():
    """Get curated free learning sources."""
    return content.get_free_sources()


@router.get("/search")
async def search(q: str, max_results: int = 5):
    """Search for free learning content on YouTube."""
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    results = await content.search_youtube(q, max_results)
    return {"query": q, "results": results}
