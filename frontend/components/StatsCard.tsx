import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface StatsCardProps {
  title: string
  value: number
  unit: string
  icon: ReactNode
  color: 'red' | 'orange' | 'blue' | 'purple' | 'green'
  loading?: boolean
}

export default function StatsCard({
  title,
  value,
  unit,
  icon,
  color,
  loading = false
}: StatsCardProps) {
  const colorClasses = {
    red: 'from-red-500/20 to-red-600/20 border-red-500/50 text-red-400',
    orange: 'from-orange-500/20 to-orange-600/20 border-orange-500/50 text-orange-400',
    blue: 'from-blue-500/20 to-blue-600/20 border-blue-500/50 text-blue-400',
    purple: 'from-purple-500/20 to-purple-600/20 border-purple-500/50 text-purple-400',
    green: 'from-green-500/20 to-green-600/20 border-green-500/50 text-green-400'
  }

  const formatValue = (val: number) => {
    if (val >= 1000000) {
      return `${(val / 1000000).toFixed(2)}M`
    } else if (val >= 1000) {
      return `${(val / 1000).toFixed(2)}K`
    } else {
      return val.toFixed(2)
    }
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className={`bg-gray-800/90 bg-gradient-to-br ${colorClasses[color]} rounded-xl p-5 border backdrop-blur-sm transition-transform shadow-lg`}
      style={{ backgroundColor: 'rgba(31, 41, 55, 0.9)' }}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-gray-300 text-sm font-medium mb-2">{title}</p>
          {loading ? (
            <div className="h-8 w-24 bg-gray-700 animate-pulse rounded" />
          ) : (
            <div className="flex items-baseline space-x-2">
              <span className="text-3xl font-bold text-white">
                {formatValue(value)}
              </span>
              <span className={`text-sm font-medium ${colorClasses[color]}`}>
                {unit}
              </span>
            </div>
          )}
        </div>
        <div className={`p-3 rounded-lg bg-gray-800/50 ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>

      {/* Optional trend indicator */}
      <div className="mt-3 pt-3 border-t border-gray-700/50">
        <div className="flex items-center space-x-1">
          <span className="text-xs text-gray-400">Last 30 days</span>
        </div>
      </div>
    </motion.div>
  )
}



