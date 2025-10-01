import { z } from 'zod'

export const ChatResponseSchema = z.object({
  message: z.string(),
  requestId: z.string().optional(),
  capacity: z.enum(['green', 'yellow', 'red']).optional(),
  suggestions: z.array(z.object({ startDate: z.string(), endDate: z.string() })).optional(),
  status: z.string().optional(),
})
export type TChatResponse = z.infer<typeof ChatResponseSchema>

export async function postChat(text: string): Promise<TChatResponse> {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/chat`
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
  if (!r.ok) {
    throw new Error(`Chat request failed: ${r.status}`)
  }
  const data = await r.json()
  return ChatResponseSchema.parse(data)
}

