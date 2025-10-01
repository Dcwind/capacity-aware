import '@/styles/globals.css'
import type { Metadata } from 'next'
import { ThemeProvider } from 'next-themes'
import { Toaster } from 'sonner'
import { TopNav } from '@/components/layout/TopNav'

export const metadata: Metadata = {
  title: 'Leave Planner',
  description: 'Capacity-aware leave planning with chat',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <div className="min-h-screen flex flex-col">
            <header className="sticky top-0 z-30 border-b bg-gradient-to-b from-primary/5 to-background backdrop-blur supports-[backdrop-filter]:bg-primary/5">
              <div className="container py-3">
                <TopNav />
              </div>
            </header>
            <main className="flex-1 container py-6">{children}</main>
          </div>
          <Toaster richColors closeButton />
        </ThemeProvider>
      </body>
    </html>
  )
}

