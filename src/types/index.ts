export interface CoursePlan {
  id: string;
  topic: string;
  language: string;
  skillLevel: "beginner" | "intermediate" | "advanced";
  totalWeeks: number;
  weeks: CourseWeek[];
  createdAt: string;
}

export interface CourseWeek {
  weekNumber: number;
  title: string;
  description: string;
  topics: string[];
  resources: ContentResource[];
}

export interface ContentResource {
  id: string;
  title: string;
  source: "youtube" | "nptel" | "khan_academy" | "mit_ocw" | "swayam";
  url: string;
  thumbnail?: string;
  duration?: string;
  language: string;
  rating?: number;
  viewCount?: number;
}

export interface UserProfile {
  userId: string;
  name: string;
  preferredLanguage: string;
  interests: string[];
  activePlans: string[];
  createdAt: string;
}

export interface UserProgress {
  userId: string;
  planId: string;
  completedResources: string[];
  currentWeek: number;
  lastAccessedAt: string;
  progressPercent: number;
}

export type SupportedLanguage =
  | "en"
  | "hi"
  | "ta"
  | "te"
  | "bn"
  | "mr"
  | "gu"
  | "kn"
  | "ml"
  | "pa"
  | "or"
  | "as";

export interface LanguageOption {
  code: SupportedLanguage;
  name: string;
  nativeName: string;
}

export const SUPPORTED_LANGUAGES: LanguageOption[] = [
  { code: "en", name: "English", nativeName: "English" },
  { code: "hi", name: "Hindi", nativeName: "हिन्दी" },
  { code: "ta", name: "Tamil", nativeName: "தமிழ்" },
  { code: "te", name: "Telugu", nativeName: "తెలుగు" },
  { code: "bn", name: "Bengali", nativeName: "বাংলা" },
  { code: "mr", name: "Marathi", nativeName: "मराठी" },
  { code: "gu", name: "Gujarati", nativeName: "ગુજરાતી" },
  { code: "kn", name: "Kannada", nativeName: "ಕನ್ನಡ" },
  { code: "ml", name: "Malayalam", nativeName: "മലയാളം" },
  { code: "pa", name: "Punjabi", nativeName: "ਪੰਜਾਬੀ" },
  { code: "or", name: "Odia", nativeName: "ଓଡ଼ିଆ" },
  { code: "as", name: "Assamese", nativeName: "অসমীয়া" },
];
