import type { ChatResponse, LearnerProfile, ProfileChatResponse, CourseResponse, CourseJSON } from '@/types/api'

const BASE = ''

// --- Legacy ---

export async function sendChat(message: string, history: { role: string; content: string }[]): Promise<ChatResponse> {
  const res = await fetch(`${BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history: history.slice(-10) }),
  })
  if (!res.ok) throw new Error('Chat request failed')
  return res.json()
}

export async function speechToText(audioBase64: string, languageCode: string) {
  const res = await fetch(`${BASE}/api/voice/stt`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ audio_base64: audioBase64, language_code: languageCode }),
  })
  if (!res.ok) throw new Error('STT failed')
  return res.json()
}

export async function textToSpeech(text: string, languageCode: string) {
  const res = await fetch(`${BASE}/api/voice/tts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, language_code: languageCode }),
  })
  if (!res.ok) throw new Error('TTS failed')
  return res.json()
}

// --- New Course Pipeline ---

export async function profileChat(
  message: string,
  profile?: LearnerProfile,
  courseId?: string,
): Promise<ProfileChatResponse> {
  const res = await fetch(`${BASE}/api/course/profile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, profile, course_id: courseId }),
  })
  if (!res.ok) throw new Error('Profile chat failed')
  return res.json()
}

export async function createCourse(
  profile: LearnerProfile,
  topic: string = 'artificial intelligence',
): Promise<CourseResponse> {
  const res = await fetch(`${BASE}/api/course/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ profile, topic }),
  })
  if (!res.ok) throw new Error('Course creation failed')
  return res.json()
}

export async function getCourse(courseId: string): Promise<CourseResponse> {
  const res = await fetch(`${BASE}/api/course/${courseId}`)
  if (!res.ok) throw new Error('Course not found')
  return res.json()
}

export async function listCourses(): Promise<{ courses: CourseJSON[] }> {
  const res = await fetch(`${BASE}/api/courses`)
  if (!res.ok) throw new Error('Failed to list courses')
  return res.json()
}

export async function updateProgress(courseId: string, moduleNumber: number): Promise<CourseResponse> {
  const res = await fetch(`${BASE}/api/course/${courseId}/progress`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ module_number: moduleNumber }),
  })
  if (!res.ok) throw new Error('Failed to update progress')
  return res.json()
}
