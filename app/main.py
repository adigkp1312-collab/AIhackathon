"""
SeekhoFree - Free AI-Powered Learning Platform

A voice-first AI learning assistant that aggregates free courses from
YouTube, NPTEL, MIT OCW, and more. Powered by Amazon Bedrock for
intelligent course planning and Sarvam AI for multilingual voice.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import api, pages, webhooks

app = FastAPI(
    title="SeekhoFree",
    description="Free AI-powered learning platform for India",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api.router)
app.include_router(webhooks.router)
app.include_router(pages.router)
