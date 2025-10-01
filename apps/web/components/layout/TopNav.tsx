"use client"
import { useTheme } from 'next-themes'
import { Moon, Sun } from 'lucide-react'

export function TopNav() {
  const { theme, setTheme } = useTheme()
  const isDark = theme === 'dark'
  return (
    <div className="w-full flex items-center justify-between">
      <div className="font-semibold">Leave Planner</div>
      <div className="flex items-center gap-3">
        <button
          aria-label="Toggle theme"
          onClick={() => setTheme(isDark ? 'light' : 'dark')}
          className="inline-flex items-center justify-center rounded-lg border h-9 w-9 hover:bg-accent"
        >
          {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </button>
        <div className="h-9 w-9 rounded-full bg-muted" />
      </div>
    </div>
  )
}
