"""
Adiyogi AI Education - Free AI-Powered Learning Platform

A voice-first AI learning assistant that aggregates free courses from
YouTube, NPTEL, MIT OCW, and more. Powered by Vertex AI (Gemini) for
intelligent course planning and Sarvam AI for multilingual voice.
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api, webhooks

app = FastAPI(
    title="Adiyogi AI Education",
    description="Free AI-powered learning platform for India",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve React build if it exists, otherwise fall back to old static
REACT_DIST = os.path.join(os.path.dirname(__file__), "static", "dist")
if os.path.isdir(REACT_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(REACT_DIST, "assets")), name="assets")

# Keep legacy static for fallback
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api.router)
app.include_router(webhooks.router)


@app.get("/")
async def serve_spa():
    """Serve React SPA if built, otherwise fall back to Jinja2 template."""
    index = os.path.join(REACT_DIST, "index.html")
    if os.path.isfile(index):
        return FileResponse(index)
    # Fallback to old template
    from fastapi.templating import Jinja2Templates
    from starlette.requests import Request
    templates = Jinja2Templates(directory="app/templates")
    return templates.TemplateResponse("index.html", {"request": Request(scope={"type": "http"})})
