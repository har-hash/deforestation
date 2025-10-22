import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { AlertTriangle, Clock, MapPin, TrendingUp } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

interface Alert {
  id: string
  timestamp: string
  region: string
  area_ha: number
  confidence: number
  severity: string
}

export default function AlertPanel() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAlerts()
    const interval = setInterval(fetchAlerts, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchAlerts = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/alerts?limit=20`
      )
      const data = await response.json()
      if (data.success) {
        setAlerts(data.alerts)
      }
    } catch (error) {
      console.error('Error fetching alerts:', error)
    } finally {
      setLoading(false)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500'
      case 'high': return 'bg-orange-600'
      case 'medium': return 'bg-yellow-500'
      default: return 'bg-blue-500'
    }
  }

  const getSeverityBorder = (severity: string) => {
    switch (severity) {
      case 'critical': return 'border-red-500'
      case 'high': return 'border-orange-600'
      case 'medium': return 'border-yellow-500'
      default: return 'border-blue-500'
    }
  }

  return (
    <div className="bg-gray-800/95 rounded-xl shadow-2xl h-[600px] flex flex-col" style={{ backgroundColor: 'rgba(31, 41, 55, 0.95)' }}>
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <h2 className="text-lg font-bold text-white">Real-time Alerts</h2>
          </div>
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-xs text-gray-400">Live</span>
          </div>
        </div>
        <p className="text-sm text-gray-400 mt-1">
          {alerts.length} active alert{alerts.length !== 1 ? 's' : ''}
        </p>
      </div>

      {/* Alerts List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="spinner" />
          </div>
        ) : alerts.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <AlertTriangle className="w-12 h-12 mb-2 opacity-50" />
            <p>No alerts at this time</p>
          </div>
        ) : (
          <AnimatePresence>
            {alerts.map((alert, index) => (
              <motion.div
                key={alert.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.05 }}
                className={`bg-gray-900 rounded-lg p-3 border-l-4 ${getSeverityBorder(alert.severity)} hover:bg-gray-850 transition-colors cursor-pointer`}
              >
                {/* Severity Badge */}
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-xs font-semibold px-2 py-1 rounded ${getSeverityColor(alert.severity)} text-white uppercase`}>
                    {alert.severity}
                  </span>
                  <span className="text-xs text-gray-500">
                    {(alert.confidence * 100).toFixed(0)}% confidence
                  </span>
                </div>

                {/* Alert Details */}
                <div className="space-y-1.5">
                  <div className="flex items-start space-x-2">
                    <TrendingUp className="w-4 h-4 text-red-400 mt-0.5 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-white font-medium">
                        {alert.area_ha.toFixed(2)} hectares lost
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-2">
                    <MapPin className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-400 truncate">
                        {alert.region}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-2">
                    <Clock className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-400">
                        {formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true })}
                      </p>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        )}
      </div>

      {/* Footer */}
      <div className="p-3 border-t border-gray-700 bg-gray-850">
        <button
          onClick={fetchAlerts}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors"
        >
          Refresh Alerts
        </button>
      </div>
    </div>
  )
}



