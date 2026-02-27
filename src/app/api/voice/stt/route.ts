import { NextRequest, NextResponse } from "next/server";
import { speechToText } from "@/lib/sarvam";
import type { SupportedLanguage } from "@/types";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { audio, language } = body;

    if (!audio) {
      return NextResponse.json(
        { error: "Audio base64 string is required" },
        { status: 400 }
      );
    }

    const result = await speechToText(
      audio,
      (language as SupportedLanguage) || "hi"
    );

    return NextResponse.json({
      text: result.text,
      language: result.language,
    });
  } catch (error) {
    console.error("Error in speech-to-text:", error);
    return NextResponse.json(
      { error: "Failed to convert speech to text" },
      { status: 500 }
    );
  }
}
