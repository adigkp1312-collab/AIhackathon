"""
Voice interaction service powered by Sarvam AI.

Handles:
- Speech-to-Text (STT): Convert user's voice to text in any Indian language
- Text-to-Speech (TTS): Convert AI responses to natural speech in Indian languages
"""

import base64
import httpx
from app.config import settings

SUPPORTED_LANGUAGES = {
    "hi-IN": "Hindi",
    "bn-IN": "Bengali",
    "ta-IN": "Tamil",
    "te-IN": "Telugu",
    "gu-IN": "Gujarati",
    "kn-IN": "Kannada",
    "ml-IN": "Malayalam",
    "mr-IN": "Marathi",
    "pa-IN": "Punjabi",
    "od-IN": "Odia",
    "en-IN": "English (Indian)",
}


async def speech_to_text(audio_base64: str, language_code: str = "hi-IN") -> dict:
    """
    Convert speech audio to text using Sarvam AI STT.
    Falls back to a demo response if API key is not configured.
    """
    if settings.SARVAM_API_KEY:
        return await _sarvam_stt(audio_base64, language_code)
    return _demo_stt_response()


async def text_to_speech(text: str, language_code: str = "hi-IN", voice: str = "meera") -> dict:
    """
    Convert text to speech using Sarvam AI TTS (Bulbul v3).
    Falls back to a demo response if API key is not configured.
    """
    if settings.SARVAM_API_KEY:
        return await _sarvam_tts(text, language_code, voice)
    return _demo_tts_response(text)


async def _sarvam_stt(audio_base64: str, language_code: str) -> dict:
    """Call Sarvam AI Speech-to-Text API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.SARVAM_STT_URL,
                headers={
                    "Content-Type": "application/json",
                    "API-Subscription-Key": settings.SARVAM_API_KEY,
                },
                json={
                    "input": audio_base64,
                    "language_code": language_code,
                    "model": "saaras:v2",
                    "with_timestamps": False,
                },
                timeout=30,
            )
            data = response.json()
            return {
                "success": True,
                "transcript": data.get("transcript", ""),
                "language_code": data.get("language_code", language_code),
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def _sarvam_tts(text: str, language_code: str, voice: str) -> dict:
    """Call Sarvam AI Text-to-Speech API (Bulbul v3)."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.SARVAM_TTS_URL,
                headers={
                    "Content-Type": "application/json",
                    "API-Subscription-Key": settings.SARVAM_API_KEY,
                },
                json={
                    "input": text[:500],  # API limit
                    "target_language_code": language_code,
                    "speaker": voice,
                    "model": "bulbul:v2",
                    "pitch": 0,
                    "pace": 1.0,
                    "loudness": 1.0,
                    "enable_preprocessing": True,
                },
                timeout=30,
            )
            data = response.json()
            return {
                "success": True,
                "audio_base64": data.get("audios", [""])[0],
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


def _demo_stt_response() -> dict:
    """Demo STT response when Sarvam API is not configured."""
    return {
        "success": True,
        "transcript": "[Voice input demo] - Configure SARVAM_API_KEY for live voice recognition",
        "language_code": "hi-IN",
        "demo": True,
    }


def _demo_tts_response(text: str) -> dict:
    """Demo TTS response when Sarvam API is not configured."""
    return {
        "success": True,
        "audio_base64": "",
        "demo": True,
        "message": f"[TTS demo] Would speak: {text[:100]}... Configure SARVAM_API_KEY for live voice output",
    }


def get_supported_languages() -> dict:
    """Return supported Indian languages for voice interaction."""
    return SUPPORTED_LANGUAGES
