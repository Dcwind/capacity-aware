"use client"
import { useEffect, useState } from 'react'
import { toast } from 'sonner'

interface PendingItem {
  request_id: string
  name: string
  start: string
  end: string
  status: string
  age: number
}

export default function ManagerDashboardPage() {
  const [items, setItems] = useState<PendingItem[]>([])
  const [loading, setLoading] = useState(true)

  async function load() {
    setLoading(true)
    try {
      const r = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/manager/pending`)
      const data = await r.json()
      setItems(data.items || [])
    } catch (e) {
      toast.error('Failed to load pending requests')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function decide(request_id: string, decision: 'APPROVE' | 'REJECT') {
    try {
      const r = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/manager/decision`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ request_id, decision }),
      })
      if (!r.ok) throw new Error()
      toast.success(`${decision === 'APPROVE' ? 'Approved' : 'Rejected'} ${request_id}`)
      load()
    } catch (e) {
      toast.error('Action failed')
    }
  }

  return (
    <div className="grid gap-4">
      <h2 className="text-xl font-semibold">Manager dashboard</h2>
      <div className="rounded-2xl border shadow-lg/10 p-4">
        <div className="font-medium mb-2">Pending requests</div>
        {loading ? (
          <div className="text-sm text-muted-foreground">Loading…</div>
        ) : items.length === 0 ? (
          <div className="text-sm text-muted-foreground">No pending requests</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-left text-muted-foreground">
                <tr>
                  <th className="py-2">Name</th>
                  <th className="py-2">Dates</th>
                  <th className="py-2">Status</th>
                  <th className="py-2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((it) => (
                  <tr key={it.request_id} className="border-t">
                    <td className="py-2">{it.name}</td>
                    <td className="py-2">{it.start} → {it.end}</td>
                    <td className="py-2">{it.status}</td>
                    <td className="py-2">
                      <div className="flex gap-2">
                        <button className="rounded-lg border px-2 py-1 hover:bg-accent" onClick={() => decide(it.request_id, 'APPROVE')}>Approve</button>
                        <button className="rounded-lg border px-2 py-1 hover:bg-accent" onClick={() => decide(it.request_id, 'REJECT')}>Reject</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      <div className="rounded-2xl border shadow-lg/10 p-4">
        <div className="font-medium mb-2">Capacity snapshot</div>
        <div className="flex gap-1">
          {[...Array(14)].map((_, i) => {
            const d = new Date(); d.setDate(d.getDate() + i)
            const date = d.toISOString().slice(0,10)
            return <Dot key={i} date={date} />
          })}
        </div>
      </div>
    </div>
  )
}

function Dot({ date }: { date: string }) {
  const [color, setColor] = useState<'green'|'yellow'|'red'>('yellow')
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/capacity?date=${date}`)
      .then(r => r.json())
      .then(d => setColor(d.capacity))
      .catch(() => {})
  }, [date])
  const cls = color === 'green' ? 'bg-emerald-500' : color === 'yellow' ? 'bg-amber-500' : 'bg-red-500'
  return <div className={`h-3 w-3 rounded-full ${cls}`} title={`${date} ${color}`} />
}

