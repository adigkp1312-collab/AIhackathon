"""
Webhook endpoints for messaging platform integrations.

Supports:
- WhatsApp (via WhatsApp Business API / Meta Cloud API)
- Facebook Messenger
- Telegram

Each platform receives messages via webhooks, processes them through
the same AI course planner (Bedrock), and responds back.
"""

import os
import json
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException
from app.services import bedrock

router = APIRouter(prefix="/webhooks")

# Verification tokens (set via env vars)
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "seekhofree_verify")
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "")
MESSENGER_VERIFY_TOKEN = os.getenv("MESSENGER_VERIFY_TOKEN", "seekhofree_verify")
MESSENGER_PAGE_TOKEN = os.getenv("MESSENGER_PAGE_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


# ─── WhatsApp Business API ───────────────────────────────────────────

@router.get("/whatsapp")
async def whatsapp_verify(request: Request):
    """Webhook verification for WhatsApp Business API."""
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        return int(challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def whatsapp_incoming(request: Request):
    """
    Handle incoming WhatsApp messages.
    Receives user message -> generates course plan -> sends reply.
    """
    body = await request.json()

    try:
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        message = value["messages"][0]
        from_number = message["from"]
        text = message.get("text", {}).get("body", "")

        if not text:
            return {"status": "ok"}

        # Generate course plan
        plan = bedrock.generate_course_plan(text)
        reply = _format_plan_for_text(plan)

        # Send reply via WhatsApp Cloud API
        if WHATSAPP_API_TOKEN:
            phone_id = value["metadata"]["phone_number_id"]
            await _send_whatsapp_message(phone_id, from_number, reply)

    except (KeyError, IndexError):
        pass  # Ignore non-message webhooks (status updates, etc.)

    return {"status": "ok"}


async def _send_whatsapp_message(phone_id: str, to: str, text: str):
    """Send a WhatsApp message via Cloud API."""
    import httpx

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://graph.facebook.com/v18.0/{phone_id}/messages",
            headers={"Authorization": f"Bearer {WHATSAPP_API_TOKEN}"},
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": text[:4096]},  # WhatsApp message limit
            },
        )


# ─── Facebook Messenger ──────────────────────────────────────────────

@router.get("/messenger")
async def messenger_verify(request: Request):
    """Webhook verification for Facebook Messenger."""
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == MESSENGER_VERIFY_TOKEN:
        return int(challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/messenger")
async def messenger_incoming(request: Request):
    """Handle incoming Messenger messages."""
    body = await request.json()

    try:
        for entry in body.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                text = event.get("message", {}).get("text", "")

                if not text:
                    continue

                plan = bedrock.generate_course_plan(text)
                reply = _format_plan_for_text(plan)

                if MESSENGER_PAGE_TOKEN:
                    await _send_messenger_message(sender_id, reply)
    except (KeyError, IndexError):
        pass

    return {"status": "ok"}


async def _send_messenger_message(recipient_id: str, text: str):
    """Send a Messenger message via Page API."""
    import httpx

    async with httpx.AsyncClient() as client:
        await client.post(
            "https://graph.facebook.com/v18.0/me/messages",
            params={"access_token": MESSENGER_PAGE_TOKEN},
            json={
                "recipient": {"id": recipient_id},
                "message": {"text": text[:2000]},  # Messenger limit
            },
        )


# ─── Telegram Bot ─────────────────────────────────────────────────────

@router.post("/telegram")
async def telegram_incoming(request: Request):
    """Handle incoming Telegram messages."""
    body = await request.json()

    try:
        message = body.get("message", {})
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if not text or text.startswith("/start"):
            reply = (
                "Namaste! I'm SeekhoFree Bot.\n\n"
                "Tell me what you want to learn and I'll create a free "
                "course plan from YouTube, NPTEL, and more.\n\n"
                "Example: 'I want to learn Python' or 'mujhe ML seekhna hai'"
            )
        else:
            plan = bedrock.generate_course_plan(text)
            reply = _format_plan_for_text(plan)

        if TELEGRAM_BOT_TOKEN:
            await _send_telegram_message(chat_id, reply)
    except (KeyError, IndexError):
        pass

    return {"status": "ok"}


async def _send_telegram_message(chat_id: int, text: str):
    """Send a Telegram message."""
    import httpx

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text[:4096],  # Telegram limit
                "parse_mode": "Markdown",
            },
        )


# ─── Helper: Format plan for text-based platforms ─────────────────────

def _format_plan_for_text(plan: dict) -> str:
    """Convert a structured course plan to plain text for messaging platforms."""
    if plan.get("type") == "conversation":
        return plan["message"]

    lines = []
    lines.append(f"*{plan.get('title', 'Learning Plan')}*")
    lines.append(plan.get("description", ""))
    lines.append(f"Duration: {plan.get('estimated_duration', 'N/A')} | Level: {plan.get('skill_level', 'N/A')}")
    lines.append("")

    for mod in plan.get("modules", []):
        lines.append(f"*Module {mod['module_number']}: {mod['title']}*")
        lines.append(f"  {mod['description']} ({mod.get('duration', '')})")
        for res in mod.get("resources", []):
            lines.append(f"  - {res['title']} ({res['language']})")
            lines.append(f"    Search: {res.get('url_hint', '')}")
        lines.append("")

    if plan.get("tips"):
        lines.append("*Tips:*")
        for tip in plan["tips"]:
            lines.append(f"  - {tip}")

    return "\n".join(lines)
