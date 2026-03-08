import { Sparkles, Wand2 } from 'lucide-react'
import type { UserProfile } from '@/types/api'

const CATEGORIES = [
  { label: 'Machine Learning', icon: '🤖', query: 'I want to learn machine learning' },
  { label: 'Deep Learning', icon: '🧠', query: 'I want to learn deep learning and neural networks' },
  { label: 'NLP & LLMs', icon: '💬', query: 'I want to learn NLP and large language models' },
  { label: 'Computer Vision', icon: '👁️', query: 'I want to learn computer vision' },
  { label: 'Generative AI', icon: '✨', query: 'I want to learn generative AI' },
  { label: 'Python for AI', icon: '🐍', query: 'I want to learn Python for AI and ML' },
  { label: 'Data Science', icon: '📊', query: 'I want to learn data science with Python' },
  { label: 'MLOps', icon: '⚙️', query: 'I want to learn MLOps and model deployment' },
]

const TRENDING_SECTIONS = [
  {
    title: 'Most Popular',
    courses: [
      { title: 'Python for Beginners', provider: 'CodeWithHarry', type: 'Full Course', thumb: 'https://i.ytimg.com/vi/7wnove7K-ZQ/mqdefault.jpg', query: 'I want to learn Python programming from scratch' },
      { title: 'Machine Learning A-Z', provider: 'CampusX', type: 'Series', thumb: 'https://i.ytimg.com/vi/7uwa9aPbBRU/mqdefault.jpg', query: 'I want to learn machine learning step by step' },
      { title: 'Web Dev Bootcamp', provider: 'Apna College', type: 'Full Course', thumb: 'https://i.ytimg.com/vi/tVzUXW6siu0/mqdefault.jpg', query: 'I want to learn web development HTML CSS JavaScript' },
    ],
  },
  {
    title: 'In-Demand AI Skills',
    courses: [
      { title: 'Deep Learning', provider: 'Stanford Online', type: 'Lecture Series', thumb: 'https://i.ytimg.com/vi/PySo_6S4ZAg/mqdefault.jpg', query: 'I want to learn deep learning and neural networks' },
      { title: 'Gen AI & LLMs', provider: 'freeCodeCamp', type: 'Tutorial', thumb: 'https://i.ytimg.com/vi/mEsleV16qdo/mqdefault.jpg', query: 'I want to learn generative AI and large language models' },
      { title: 'Data Analysis', provider: 'freeCodeCamp', type: 'Full Course', thumb: 'https://i.ytimg.com/vi/GPVsHOlRBBI/mqdefault.jpg', query: 'I want to learn data analysis with Python pandas' },
    ],
  },
]

const SOURCES = [
  { name: 'YouTube', icon: '▶️' },
  { name: 'NPTEL', icon: '🏛️' },
  { name: 'MIT OCW', icon: '🎓' },
  { name: 'Khan Academy', icon: '📐' },
  { name: 'freeCodeCamp', icon: '🔥' },
  { name: 'SWAYAM', icon: '🇮🇳' },
]

interface WelcomeProps {
  profile: UserProfile | null
  onTopicClick: (query: string) => void
  onCreateCourse?: () => void
}

export function Welcome({ profile, onTopicClick, onCreateCourse }: WelcomeProps) {
  return (
    <div className="pb-8">
      {/* Hero */}
      <div className="px-5 pt-6 pb-4">
        <h2 className="text-xl font-bold leading-tight">
          {profile ? `Welcome back, ${profile.name}` : 'Learn from 350+ free sources'}
        </h2>
        <p className="text-sm text-muted-foreground mt-1">
          AI-curated learning paths from YouTube, NPTEL, MIT OCW & more
        </p>
      </div>

      {/* Create Course CTA */}
      {onCreateCourse && (
        <div className="px-5 pb-4">
          <button
            onClick={onCreateCourse}
            className="w-full flex items-center gap-3 bg-gradient-to-r from-primary to-primary/80 text-primary-foreground rounded-2xl px-5 py-4 group hover:shadow-lg transition-shadow"
          >
            <div className="w-10 h-10 rounded-xl bg-white/20 flex items-center justify-center flex-shrink-0">
              <Wand2 className="w-5 h-5" />
            </div>
            <div className="text-left">
              <div className="text-sm font-bold">Create Your AI Course</div>
              <div className="text-xs opacity-80">Adaptive curriculum designed by AI, just for you</div>
            </div>
          </button>
        </div>
      )}

      {/* Source logos */}
      <div className="px-5 pb-4">
        <div className="flex gap-3 overflow-x-auto pb-1 scrollbar-none">
          {SOURCES.map(s => (
            <div key={s.name} className="flex items-center gap-1.5 bg-card border border-border rounded-full px-3 py-1.5 text-xs font-medium whitespace-nowrap flex-shrink-0">
              <span>{s.icon}</span> {s.name}
            </div>
          ))}
        </div>
      </div>

      {/* Category pills */}
      <div className="px-5 pb-5">
        <h3 className="text-sm font-semibold mb-2.5">Explore categories</h3>
        <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none">
          {CATEGORIES.map(cat => (
            <button
              key={cat.label}
              onClick={() => onTopicClick(cat.query)}
              className="flex items-center gap-1.5 border border-border rounded-full px-3.5 py-2 text-sm whitespace-nowrap hover:border-primary hover:text-primary transition-colors flex-shrink-0"
            >
              <span>{cat.icon}</span> {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Trending bento sections */}
      {TRENDING_SECTIONS.map(section => (
        <div key={section.title} className="px-5 pb-5">
          <h3 className="text-sm font-semibold mb-3 flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-primary" />
            {section.title}
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {section.courses.map(course => (
              <button
                key={course.title}
                onClick={() => onTopicClick(course.query)}
                className="group text-left border border-border rounded-xl overflow-hidden hover:border-primary/40 hover:shadow-sm transition-all"
              >
                <div className="relative w-full aspect-video bg-muted overflow-hidden">
                  <img
                    src={course.thumb}
                    alt={course.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    loading="lazy"
                  />
                  <div className="absolute top-2 right-2 bg-black/70 text-white text-[0.6rem] font-medium px-1.5 py-0.5 rounded">
                    FREE
                  </div>
                </div>
                <div className="p-3">
                  <div className="text-[0.65rem] text-muted-foreground">{course.provider}</div>
                  <h4 className="text-sm font-semibold leading-tight mt-0.5 group-hover:text-primary transition-colors line-clamp-2">
                    {course.title}
                  </h4>
                  <div className="text-[0.65rem] text-muted-foreground mt-1">{course.type}</div>
                </div>
              </button>
            ))}
          </div>
        </div>
      ))}

      {/* Intent cards */}
      <div className="mx-5 p-5 bg-muted/50 rounded-2xl border border-border">
        <h3 className="text-sm font-semibold text-center mb-3">What brings you here today?</h3>
        <div className="grid grid-cols-2 gap-2">
          {[
            { label: 'Start AI career', query: 'I want to start a career in AI and machine learning' },
            { label: 'Build AI projects', query: 'I want to build hands-on AI projects with Python' },
            { label: 'Crack GATE AI', query: 'I want to prepare for GATE AI exam' },
            { label: 'Learn GenAI', query: 'I want to learn generative AI and build LLM apps' },
          ].map(intent => (
            <button
              key={intent.label}
              onClick={() => onTopicClick(intent.query)}
              className="flex items-center justify-center gap-2 bg-white border border-border rounded-xl px-3 py-2.5 text-sm font-medium hover:border-primary hover:text-primary transition-colors"
            >
              {intent.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
