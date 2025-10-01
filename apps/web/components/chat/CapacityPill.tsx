"use client"
import { motion } from 'framer-motion'
import type { CapacityLevel } from '@/lib/types'

const colorByLevel: Record<CapacityLevel, string> = {
  green: 'bg-emerald-500/20 text-emerald-600 dark:text-emerald-400',
  yellow: 'bg-amber-500/20 text-amber-600 dark:text-amber-400',
  red: 'bg-red-500/20 text-red-600 dark:text-red-400',
}

export function CapacityPill({ level, label }: { level: CapacityLevel; label?: string }) {
  return (
    <motion.div
      initial={{ scale: 0.95, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ type: 'spring', stiffness: 260, damping: 20 }}
      title={label}
      className={`inline-flex items-center gap-2 rounded-full px-2.5 py-1 text-xs font-medium ${colorByLevel[level]}`}
    >
      <span className={`h-2 w-2 rounded-full ${level === 'green' ? 'bg-emerald-500' : level === 'yellow' ? 'bg-amber-500' : 'bg-red-500'}`} />
      {level.toUpperCase()}
    </motion.div>
  )
}
