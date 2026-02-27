import type { SupportedLanguage } from "@/types";

const SARVAM_API_URL = process.env.SARVAM_API_URL || "https://api.sarvam.ai";

const SARVAM_LANGUAGE_CODES: Record<SupportedLanguage, string> = {
  en: "en-IN",
  hi: "hi-IN",
  ta: "ta-IN",
  te: "te-IN",
  bn: "bn-IN",
  mr: "mr-IN",
  gu: "gu-IN",
  kn: "kn-IN",
  ml: "ml-IN",
  pa: "pa-IN",
  or: "or-IN",
  as: "as-IN",
};

export async function speechToText(
  audioBase64: string,
  language: SupportedLanguage = "hi"
): Promise<{ text: string; language: string }> {
  const apiKey = process.env.SARVAM_API_KEY;
  if (!apiKey) throw new Error("Sarvam API key not configured");

  const langCode = SARVAM_LANGUAGE_CODES[language] || "hi-IN";

  const response = await fetch(`${SARVAM_API_URL}/speech-to-text`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "api-subscription-key": apiKey,
    },
    body: JSON.stringify({
      input: audioBase64,
      language_code: langCode,
      model: "saarika:v2",
      with_timestamps: false,
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Sarvam STT failed: ${err}`);
  }

  const data = await response.json();
  return {
    text: data.transcript || data.text || "",
    language: language,
  };
}

export async function textToSpeech(
  text: string,
  language: SupportedLanguage = "hi"
): Promise<string> {
  const apiKey = process.env.SARVAM_API_KEY;
  if (!apiKey) throw new Error("Sarvam API key not configured");

  const langCode = SARVAM_LANGUAGE_CODES[language] || "hi-IN";

  const response = await fetch(`${SARVAM_API_URL}/text-to-speech`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "api-subscription-key": apiKey,
    },
    body: JSON.stringify({
      inputs: [text],
      target_language_code: langCode,
      speaker: "meera",
      model: "bulbul:v1",
      enable_preprocessing: true,
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Sarvam TTS failed: ${err}`);
  }

  const data = await response.json();
  return data.audios?.[0] || "";
}

export async function translateText(
  text: string,
  sourceLang: SupportedLanguage,
  targetLang: SupportedLanguage
): Promise<string> {
  const apiKey = process.env.SARVAM_API_KEY;
  if (!apiKey) throw new Error("Sarvam API key not configured");

  const response = await fetch(`${SARVAM_API_URL}/translate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "api-subscription-key": apiKey,
    },
    body: JSON.stringify({
      input: text,
      source_language_code: SARVAM_LANGUAGE_CODES[sourceLang] || "en-IN",
      target_language_code: SARVAM_LANGUAGE_CODES[targetLang] || "hi-IN",
      model: "mayura:v1",
      enable_preprocessing: true,
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Sarvam translate failed: ${err}`);
  }

  const data = await response.json();
  return data.translated_text || text;
}
