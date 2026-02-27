import { NextRequest, NextResponse } from "next/server";

const VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN || "adiyogi-verify";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const mode = searchParams.get("hub.mode");
    const token = searchParams.get("hub.verify_token");
    const challenge = searchParams.get("hub.challenge");

    if (mode === "subscribe" && token === VERIFY_TOKEN) {
      console.log("WhatsApp webhook verified");
      return new NextResponse(challenge, { status: 200 });
    }

    return NextResponse.json(
      { error: "Verification failed" },
      { status: 403 }
    );
  } catch (error) {
    console.error("Error verifying WhatsApp webhook:", error);
    return NextResponse.json(
      { error: "Webhook verification error" },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Extract message details from WhatsApp webhook payload
    const entry = body.entry?.[0];
    const changes = entry?.changes?.[0];
    const value = changes?.value;
    const message = value?.messages?.[0];

    if (message) {
      const from = message.from; // sender phone number
      const text = message.text?.body || "";
      const timestamp = message.timestamp;

      console.log(
        `[WhatsApp] Message from ${from} at ${timestamp}: ${text}`
      );

      // TODO: Process the message and generate a course plan response
      // For now, this is a scaffold that logs and returns 200
    }

    // WhatsApp expects a 200 response to acknowledge receipt
    return NextResponse.json({ status: "received" }, { status: 200 });
  } catch (error) {
    console.error("Error processing WhatsApp webhook:", error);
    return NextResponse.json(
      { error: "Webhook processing error" },
      { status: 500 }
    );
  }
}
