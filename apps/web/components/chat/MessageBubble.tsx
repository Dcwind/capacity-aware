"use client"
import { motion } from 'framer-motion'
import { CapacityPill } from './CapacityPill'
import type { CapacityLevel } from '@/lib/types'

export function MessageBubble({
  role,
  text,
  capacity,
  capacityLabel,
  suggestions,
  onSuggestion,
  meta,
}: {
  role: 'user' | 'assistant'
  text: string
  capacity?: CapacityLevel
  capacityLabel?: string
  suggestions?: Array<{ startDate: string; endDate: string }>
  onSuggestion?: (s: { startDate: string; endDate: string }) => void
  meta?: string
}) {
  const isUser = role === 'user'
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`max-w-[80%] rounded-2xl border shadow-lg/10 px-3 py-2 text-sm ${
        isUser ? 'bg-primary text-primary-foreground ml-auto' : 'bg-card'
      }`}
    >
      <div className="whitespace-pre-wrap leading-tight">{text}</div>
      {!isUser && capacity ? (
        <div className="mt-2">
          <CapacityPill level={capacity} label={capacityLabel} />
        </div>
      ) : null}
      {!isUser && suggestions && suggestions.length > 0 ? (
        <div className="mt-2 flex flex-wrap gap-2">
          {suggestions.map((s, i) => (
            <button
              key={i}
              className="text-xs rounded-full border px-2 py-1 hover:bg-accent"
              onClick={() => onSuggestion?.(s)}
            >
              Try {s.startDate}–{s.endDate}
            </button>
          ))}
        </div>
      ) : null}
      {!isUser && meta ? (
        <div className="mt-2 text-xs text-muted-foreground flex items-center gap-2">
          <span>{meta}</span>
          <button
            className="rounded border px-1 py-0.5 hover:bg-accent"
            onClick={() => navigator.clipboard.writeText(meta)}
            title="Copy"
          >
            Copy
          </button>
        </div>
      ) : null}
    </motion.div>
  )
}
