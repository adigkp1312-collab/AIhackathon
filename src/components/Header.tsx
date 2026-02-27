"use client";

import { SUPPORTED_LANGUAGES, type SupportedLanguage } from "@/types";
import { t } from "@/lib/i18n";

interface HeaderProps {
  language: SupportedLanguage;
  onLanguageChange: (lang: SupportedLanguage) => void;
}

export default function Header({ language, onLanguageChange }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 bg-[#1a237e] text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-orange-400 to-orange-600 flex items-center justify-center font-bold text-lg">
            A
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">
              {t("appName", language)}
            </h1>
            <p className="text-xs text-blue-200 hidden sm:block">
              {t("voiceFirst", language)}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className="hidden md:inline-block text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded-full border border-green-500/30">
            {t("freeForever", language)}
          </span>
          <select
            value={language}
            onChange={(e) =>
              onLanguageChange(e.target.value as SupportedLanguage)
            }
            className="bg-white/10 border border-white/20 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-orange-400 cursor-pointer"
          >
            {SUPPORTED_LANGUAGES.map((lang) => (
              <option
                key={lang.code}
                value={lang.code}
                className="bg-[#1a237e] text-white"
              >
                {lang.nativeName}
              </option>
            ))}
          </select>
        </div>
      </div>
    </header>
  );
}
