"use client"
import { useEffect, useRef, useState } from 'react'
import { MessageBubble } from './MessageBubble'
import { Composer } from './Composer'
import type { CapacityLevel } from '@/lib/types'
import { postChat } from '@/lib/api'
import { toast } from 'sonner'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  text: string
  capacity?: CapacityLevel
  capacityLabel?: string
  suggestions?: Array<{ startDate: string; endDate: string }>
  meta?: string
}

export function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const scrollRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
    }
  }, [messages])

  async function handleSubmit(text: string) {
    const userMsg: ChatMessage = { id: crypto.randomUUID(), role: 'user', text }
    setMessages((m) => [...m, userMsg])
    try {
      const res = await postChat(text)
      const label = res.capacity && res.status ? `${res.status}` : undefined
      const meta = res.requestId ? `requestId: ${res.requestId}` : undefined
      const assistant: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        text: res.message,
        capacity: (res.capacity as CapacityLevel) || undefined,
        capacityLabel: label,
        suggestions: res.suggestions,
        meta: meta,
      }
      setMessages((m) => [...m, assistant])
    } catch (e) {
      toast.error('Failed to send message')
    }
  }

  function handleSuggestion(s: { startDate: string; endDate: string }) {
    void handleSubmit(`request leave ${s.startDate} to ${s.endDate}`)
  }

  return (
    <div className="rounded-2xl border shadow-lg/10 p-3 h-[70vh] flex flex-col">
      <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-3 pr-1">
        {messages.length === 0 ? (
          <div className="h-full grid place-items-center text-sm text-muted-foreground">
            Try: request leave 2025-12-10 to 2025-12-12
          </div>
        ) : (
          messages.map((m) => (
            <MessageBubble
              key={m.id}
              role={m.role}
              text={m.text}
              capacity={m.capacity}
              capacityLabel={m.capacityLabel}
              suggestions={m.suggestions}
              onSuggestion={handleSuggestion}
              meta={m.meta}
            />
          ))
        )}
      </div>
      <div className="sticky bottom-0 mt-3">
        <Composer onSubmit={handleSubmit} />
      </div>
    </div>
  )
}
