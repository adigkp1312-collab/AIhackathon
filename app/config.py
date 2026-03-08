import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # GCP / Vertex AI (reusing Adiyogi infra)
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "project-9881b278-0a45-47c1-9ed")
    GCP_REGION: str = os.getenv("GCP_REGION", "us-central1")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    # Legacy Bedrock (kept for hackathon pitch compatibility)
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    BEDROCK_MODEL_ID: str = os.getenv(
        "BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"
    )

    # Sarvam AI (voice in 11 Indian languages)
    SARVAM_API_KEY: str = os.getenv("SARVAM_API_KEY", "")
    SARVAM_TTS_URL: str = "https://api.sarvam.ai/text-to-speech"
    SARVAM_STT_URL: str = "https://api.sarvam.ai/speech-to-text-translate"

    # YouTube
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))


settings = Settings()
