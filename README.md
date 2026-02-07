# SeekhoFree

**Learn Anything. Free Forever.**

AI-powered learning platform that aggregates free courses from YouTube, NPTEL, MIT OCW, and more - then creates personalized, structured learning plans using AI. Voice-first, multilingual, available on WhatsApp.

## The Problem

World-class free content exists across YouTube, NPTEL, MIT OCW, Khan Academy - but learners don't know what to learn, in what order, from where. Paid platforms charge Rs 500-5000/month. SeekhoFree uses AI to organize free education and make it accessible to every Indian.

## How It Works

1. **Tell the AI what you want to learn** - voice or text, in any of 11 Indian languages
2. **AI generates a structured course plan** - powered by Amazon Bedrock
3. **Resources from the best free sources** - YouTube (CodeWithHarry, CampusX, Apna College), NPTEL, MIT OCW, Khan Academy
4. **Access anywhere** - web app, WhatsApp, Messenger, Telegram

## Architecture

```
User (Voice/Text, 11 Indian languages)
        |
   [Sarvam AI] -----> Speech-to-Text
        |
   [Amazon Bedrock] -> AI Course Plan Generator
        |
   [Content Layer] --> YouTube API + NPTEL + MIT OCW
        |
   [Sarvam AI] -----> Text-to-Speech (reads plan aloud)
        |
   Multi-Platform ---> Web | WhatsApp | Messenger | Telegram
```

## Tech Stack

| Component | Technology |
|---|---|
| AI Engine | Amazon Bedrock (Claude) |
| Voice | Sarvam AI (Bulbul TTS + Saaras STT) |
| Backend | Python, FastAPI |
| Content | YouTube Data API, NPTEL, MIT OCW |
| Messaging | WhatsApp Business API, Messenger, Telegram Bot |
| Frontend | HTML/CSS/JS (lightweight, mobile-first) |

## Quick Start

```bash
# Install dependencies
pip install -e .

# Copy env file and add your API keys
cp .env.example .env

# Run the server
python run.py
```

Open http://localhost:8000 in your browser.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat` | Send a learning query, get a structured course plan |
| `POST` | `/api/voice/stt` | Speech-to-text (Sarvam AI) |
| `POST` | `/api/voice/tts` | Text-to-speech (Sarvam AI) |
| `GET` | `/api/search?q=python` | Search free YouTube content |
| `GET` | `/api/sources` | List curated free learning sources |
| `GET` | `/api/languages` | List supported Indian languages |
| `POST` | `/webhooks/whatsapp` | WhatsApp webhook |
| `POST` | `/webhooks/messenger` | Facebook Messenger webhook |
| `POST` | `/webhooks/telegram` | Telegram bot webhook |

## Configuration

Set these environment variables (see `.env.example`):

| Variable | Required | Description |
|---|---|---|
| `AWS_REGION` | For Bedrock | AWS region (default: ap-south-1) |
| `AWS_ACCESS_KEY_ID` | For Bedrock | AWS credentials |
| `AWS_SECRET_ACCESS_KEY` | For Bedrock | AWS credentials |
| `SARVAM_API_KEY` | For voice | Sarvam AI API key |
| `YOUTUBE_API_KEY` | For search | YouTube Data API v3 key |
| `WHATSAPP_API_TOKEN` | For WhatsApp | Meta WhatsApp Cloud API token |
| `TELEGRAM_BOT_TOKEN` | For Telegram | Telegram Bot API token |

The app works in demo mode without any API keys configured.

## Project Structure

```
app/
  main.py              # FastAPI application
  config.py            # Configuration / env vars
  routers/
    api.py             # REST API endpoints
    pages.py           # Frontend page routes
    webhooks.py        # WhatsApp/Messenger/Telegram webhooks
  services/
    bedrock.py         # Amazon Bedrock AI course planner
    content.py         # YouTube/NPTEL content aggregation
    voice.py           # Sarvam AI voice (STT + TTS)
  templates/
    index.html         # Main chat UI
  static/
    css/style.css      # Styles
    js/app.js          # Frontend logic
docs/
  SLIDE_DECK.md        # Hackathon presentation content
```

## Hackathon

Built for **AI for Bharat** hackathon (Hack2Skill + AWS).
See `docs/SLIDE_DECK.md` for the full presentation deck content.
