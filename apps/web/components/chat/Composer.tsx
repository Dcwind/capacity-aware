"use client"
import { Send } from 'lucide-react'
import { useState } from 'react'

export function Composer({ onSubmit }: { onSubmit: (text: string) => void }) {
  const [value, setValue] = useState('')
  return (
    <div className="grid gap-2">
      <div className="flex gap-2">
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              if (value.trim()) {
                onSubmit(value.trim())
                setValue('')
              }
            }
          }}
          className="flex-1 rounded-xl border px-3 py-2 bg-background"
          placeholder="Try: request leave 2025-12-10 to 2025-12-12"
        />
        <button
          className="inline-flex items-center gap-2 rounded-xl px-4 py-2 bg-primary text-primary-foreground"
          onClick={() => {
            if (value.trim()) {
              onSubmit(value.trim())
              setValue('')
            }
          }}
        >
          <Send className="h-4 w-4" /> Send
        </button>
      </div>
      <div className="flex flex-wrap gap-2 text-xs">
        <button className="rounded-full border px-2 py-1 hover:bg-accent" onClick={() => onSubmit('request leave 2025-12-10 to 2025-12-12')}>request…</button>
        <button className="rounded-full border px-2 py-1 hover:bg-accent" onClick={() => onSubmit('status req_demo_123')}>status &lt;id&gt;</button>
        <button className="rounded-full border px-2 py-1 hover:bg-accent" onClick={() => onSubmit('pending')}>pending</button>
      </div>
    </div>
  )
}
