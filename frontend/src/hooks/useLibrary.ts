import { useState, useCallback } from 'react'
import type { LibraryItem, CoursePlan, YouTubeResult } from '@/types/api'

const STORAGE_KEY = 'adiyogi_library'

function loadLibrary(): LibraryItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

export function useLibrary() {
  const [items, setItems] = useState<LibraryItem[]>(loadLibrary)

  const save = useCallback((plan: CoursePlan, youtubeResults: YouTubeResult[], query: string) => {
    setItems(prev => {
      const exists = prev.some(i => i.plan.title === plan.title)
      if (exists) return prev
      const next = [{
        id: crypto.randomUUID(),
        plan,
        youtubeResults,
        savedAt: Date.now(),
        query,
      }, ...prev]
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
      return next
    })
  }, [])

  const remove = useCallback((id: string) => {
    setItems(prev => {
      const next = prev.filter(i => i.id !== id)
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
      return next
    })
  }, [])

  return { items, save, remove }
}
