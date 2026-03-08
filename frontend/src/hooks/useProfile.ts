import { useState, useCallback } from 'react'
import type { UserProfile } from '@/types/api'

const STORAGE_KEY = 'adiyogi_profile'

function loadProfile(): UserProfile | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function useProfile() {
  const [profile, setProfile] = useState<UserProfile | null>(loadProfile)

  const saveProfile = useCallback((p: UserProfile) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(p))
    setProfile(p)
  }, [])

  const clearProfile = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY)
    setProfile(null)
  }, [])

  return { profile, saveProfile, clearProfile }
}
