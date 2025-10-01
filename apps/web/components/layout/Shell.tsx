import { TopNav } from '@/components/layout/TopNav'

export function Shell({ children, side }: { children: React.ReactNode; side?: React.ReactNode }) {
  return (
    <div className="grid gap-4">
      <TopNav />
      <div className="grid gap-4 md:grid-cols-12">
        {side ? <aside className="md:col-span-3">{side}</aside> : null}
        <div className={side ? 'md:col-span-9' : 'md:col-span-12'}>{children}</div>
      </div>
    </div>
  )
}
