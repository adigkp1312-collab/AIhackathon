import { Trash2, Clock, BarChart3, BookOpen } from 'lucide-react'
import type { LibraryItem } from '@/types/api'

interface LibraryProps {
  items: LibraryItem[]
  onRemove: (id: string) => void
  onOpen: (item: LibraryItem) => void
}

export function Library({ items, onRemove, onOpen }: LibraryProps) {
  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 px-6 text-center">
        <div className="w-16 h-16 rounded-2xl bg-muted flex items-center justify-center mb-4">
          <BookOpen className="w-8 h-8 text-muted-foreground/40" />
        </div>
        <h3 className="text-base font-semibold">Your library is empty</h3>
        <p className="text-sm text-muted-foreground mt-1 max-w-xs">
          Save course plans from chat to build your personal learning library
        </p>
      </div>
    )
  }

  return (
    <div className="p-5">
      <h2 className="text-lg font-bold mb-4">My Library</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {items.map(item => (
          <div
            key={item.id}
            className="group border border-border rounded-xl overflow-hidden hover:border-primary/30 hover:shadow-sm transition-all"
          >
            {/* Thumbnail — Coursera card style */}
            <button onClick={() => onOpen(item)} className="w-full text-left">
              {item.youtubeResults?.[0]?.thumbnail ? (
                <img
                  src={item.youtubeResults[0].thumbnail}
                  alt={item.plan.title}
                  className="w-full aspect-video object-cover"
                />
              ) : (
                <div className="w-full aspect-video bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center">
                  <BookOpen className="w-8 h-8 text-primary/25" />
                </div>
              )}

              <div className="p-3">
                <h3 className="text-sm font-semibold leading-tight line-clamp-2 group-hover:text-primary transition-colors">
                  {item.plan.title}
                </h3>
                <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                  {item.plan.description}
                </p>
                <div className="flex items-center gap-3 mt-2 text-[0.65rem] text-muted-foreground">
                  <span className="flex items-center gap-0.5"><Clock className="w-3 h-3" /> {item.plan.estimated_duration}</span>
                  <span className="flex items-center gap-0.5"><BarChart3 className="w-3 h-3" /> {item.plan.skill_level}</span>
                </div>
              </div>
            </button>

            <div className="flex items-center justify-between px-3 pb-2">
              <span className="text-[0.6rem] text-muted-foreground">
                Saved {new Date(item.savedAt).toLocaleDateString()}
              </span>
              <button
                onClick={() => onRemove(item.id)}
                className="text-muted-foreground hover:text-destructive transition-colors p-1"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
