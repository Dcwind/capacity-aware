import Link from 'next/link'
import { Shell } from '@/components/layout/Shell'
import { ChatWindow } from '@/components/chat/ChatWindow'

export default function EmployeeChatPage() {
  return (
    <Shell>
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-xl font-semibold">Employee chat</h2>
        <Link href="/" className="text-sm text-muted-foreground hover:underline">Back</Link>
      </div>
      <ChatWindow />
    </Shell>
  )
}

