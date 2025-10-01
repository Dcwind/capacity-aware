import Link from 'next/link'

export default function Home() {
  return (
    <div className="grid gap-6">
      <div className="max-w-xl">
        <h1 className="text-2xl font-semibold tracking-tight">Capacity-aware leave planner</h1>
        <p className="text-muted-foreground mt-2">Start a chat to request leave or open the manager dashboard to review pending requests.</p>
      </div>
      <div className="flex gap-3">
        <Link href="/employee/chat" className="inline-flex items-center rounded-xl px-4 py-2 bg-primary text-primary-foreground shadow hover:opacity-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary">Employee chat</Link>
        <Link href="/manager/dashboard" className="inline-flex items-center rounded-xl px-4 py-2 border shadow hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary">Manager dashboard</Link>
      </div>
    </div>
  )
}

