import { useState, useCallback } from 'react'
import type { CourseJSON } from '@/types/api'

const STORAGE_KEY = 'adiyogi_courses'

function loadCourses(): CourseJSON[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function persist(courses: CourseJSON[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(courses))
}

export function useCourses() {
  const [courses, setCourses] = useState<CourseJSON[]>(loadCourses)

  const addCourse = useCallback((course: CourseJSON) => {
    setCourses(prev => {
      const exists = prev.some(c => c.id === course.id)
      if (exists) {
        const next = prev.map(c => c.id === course.id ? course : c)
        persist(next)
        return next
      }
      const next = [course, ...prev]
      persist(next)
      return next
    })
  }, [])

  const updateCourse = useCallback((updated: CourseJSON) => {
    setCourses(prev => {
      const next = prev.map(c => c.id === updated.id ? updated : c)
      persist(next)
      return next
    })
  }, [])

  const removeCourse = useCallback((id: string) => {
    setCourses(prev => {
      const next = prev.filter(c => c.id !== id)
      persist(next)
      return next
    })
  }, [])

  return { courses, addCourse, updateCourse, removeCourse }
}
