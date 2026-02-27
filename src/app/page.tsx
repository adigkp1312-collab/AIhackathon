"use client";

import { useState, useCallback } from "react";
import type {
  CoursePlan as CoursePlanType,
  SupportedLanguage,
} from "@/types";
import { t } from "@/lib/i18n";
import Header from "@/components/Header";
import VoiceInput from "@/components/VoiceInput";
import CoursePlan from "@/components/CoursePlan";
import LoadingSkeleton from "@/components/LoadingSkeleton";

export default function Home() {
  const [language, setLanguage] = useState<SupportedLanguage>("en");
  const [topic, setTopic] = useState("");
  const [skillLevel, setSkillLevel] = useState<
    "beginner" | "intermediate" | "advanced"
  >("beginner");
  const [weeks, setWeeks] = useState(4);
  const [isLoading, setIsLoading] = useState(false);
  const [plan, setPlan] = useState<CoursePlanType | null>(null);
  const [completedResources, setCompletedResources] = useState<Set<string>>(
    new Set()
  );
  const [error, setError] = useState<string | null>(null);

  const handleVoiceTranscript = useCallback((text: string) => {
    setTopic(text);
  }, []);

  const generatePlan = async () => {
    if (!topic.trim()) return;

    setIsLoading(true);
    setError(null);
    setPlan(null);
    setCompletedResources(new Set());

    try {
      const res = await fetch("/api/generate-plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: topic.trim(),
          language,
          skillLevel,
          weeks,
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Failed to generate plan");
      }

      const data = await res.json();
      setPlan(data.plan);
    } catch (err: any) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleMarkComplete = (resourceId: string) => {
    setCompletedResources((prev) => {
      const next = new Set(prev);
      next.add(resourceId);
      return next;
    });
  };

  const handleSpeak = async (text: string) => {
    try {
      const res = await fetch("/api/voice/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, language }),
      });

      if (res.ok) {
        const data = await res.json();
        if (data.audio) {
          const audio = new Audio(`data:audio/wav;base64,${data.audio}`);
          audio.play();
        }
      }
    } catch {
      // Fallback to browser TTS
      if ("speechSynthesis" in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        const langMap: Record<string, string> = {
          en: "en-IN",
          hi: "hi-IN",
          ta: "ta-IN",
          te: "te-IN",
          bn: "bn-IN",
        };
        utterance.lang = langMap[language] || "en-IN";
        window.speechSynthesis.speak(utterance);
      }
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Header language={language} onLanguageChange={setLanguage} />

      <main className="max-w-6xl mx-auto px-4 py-8">
        {!plan && !isLoading ? (
          /* ========== LANDING / INPUT SECTION ========== */
          <div className="flex flex-col items-center">
            {/* Hero */}
            <div className="text-center mb-10 mt-8">
              <h2 className="text-4xl md:text-5xl font-extrabold gradient-text mb-4">
                {t("tagline", language)}
              </h2>
              <p className="text-lg text-slate-500 max-w-xl mx-auto">
                {t("subtitle", language)}
              </p>
            </div>

            {/* Voice Input */}
            <div className="mb-8">
              <VoiceInput
                language={language}
                onTranscript={handleVoiceTranscript}
                disabled={isLoading}
              />
            </div>

            {/* Divider */}
            <div className="flex items-center gap-4 w-full max-w-lg mb-8">
              <div className="flex-1 h-px bg-slate-200" />
              <span className="text-sm text-slate-400">OR</span>
              <div className="flex-1 h-px bg-slate-200" />
            </div>

            {/* Text Input + Controls */}
            <div className="w-full max-w-lg space-y-4">
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder={t("placeholder", language)}
                onKeyDown={(e) => e.key === "Enter" && generatePlan()}
                className="w-full px-5 py-4 border-2 border-slate-200 rounded-xl text-lg focus:outline-none focus:border-[#1a237e] transition-colors placeholder:text-slate-300"
              />

              <div className="flex gap-3">
                {/* Skill Level */}
                <select
                  value={skillLevel}
                  onChange={(e) =>
                    setSkillLevel(
                      e.target.value as "beginner" | "intermediate" | "advanced"
                    )
                  }
                  className="flex-1 px-4 py-3 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-[#1a237e]"
                >
                  <option value="beginner">{t("beginner", language)}</option>
                  <option value="intermediate">
                    {t("intermediate", language)}
                  </option>
                  <option value="advanced">{t("advanced", language)}</option>
                </select>

                {/* Weeks */}
                <select
                  value={weeks}
                  onChange={(e) => setWeeks(Number(e.target.value))}
                  className="w-28 px-4 py-3 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-[#1a237e]"
                >
                  {[2, 4, 6, 8, 12].map((w) => (
                    <option key={w} value={w}>
                      {w} {t("weeks", language)}
                    </option>
                  ))}
                </select>
              </div>

              <button
                onClick={generatePlan}
                disabled={!topic.trim() || isLoading}
                className="w-full py-4 bg-gradient-to-r from-[#1a237e] to-[#3949ab] text-white rounded-xl font-semibold text-lg hover:shadow-lg hover:shadow-blue-900/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {t("generate", language)}
              </button>
            </div>

            {error && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm max-w-lg w-full">
                {error}
              </div>
            )}

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 w-full max-w-4xl">
              {[
                {
                  icon: "🎙️",
                  title: "Voice-First",
                  desc: "Speak in any of 11 Indian languages. Powered by Sarvam AI.",
                },
                {
                  icon: "🎓",
                  title: "Free Content",
                  desc: "Curated from YouTube, NPTEL, Khan Academy, MIT OCW & SWAYAM.",
                },
                {
                  icon: "🤖",
                  title: "AI Course Plans",
                  desc: "Amazon Bedrock creates personalized learning paths for you.",
                },
              ].map((f, i) => (
                <div
                  key={i}
                  className="card-hover bg-slate-50 rounded-xl p-6 text-center"
                >
                  <div className="text-4xl mb-3">{f.icon}</div>
                  <h3 className="font-bold text-slate-800 mb-1">{f.title}</h3>
                  <p className="text-sm text-slate-500">{f.desc}</p>
                </div>
              ))}
            </div>

            {/* Footer */}
            <p className="text-xs text-slate-400 mt-12 mb-4">
              {t("poweredBy", language)}
            </p>
          </div>
        ) : isLoading ? (
          /* ========== LOADING STATE ========== */
          <LoadingSkeleton message={t("generating", language)} />
        ) : plan ? (
          /* ========== COURSE PLAN VIEW ========== */
          <div>
            <button
              onClick={() => {
                setPlan(null);
                setTopic("");
              }}
              className="mb-6 flex items-center gap-2 text-sm text-slate-500 hover:text-[#1a237e] transition-colors"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
              New Search
            </button>

            <CoursePlan
              plan={plan}
              language={language}
              completedResources={completedResources}
              onMarkComplete={handleMarkComplete}
              onSpeak={handleSpeak}
            />
          </div>
        ) : null}
      </main>
    </div>
  );
}
