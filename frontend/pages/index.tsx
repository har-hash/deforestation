import { useState, useEffect } from 'react'
import Head from 'next/head'
import { motion } from 'framer-motion'
import dynamic from 'next/dynamic'
// Load MapView only on the client to avoid SSR issues
const MapView = dynamic(() => import('@/components/MapView'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center bg-gray-800">
      <p className="text-gray-400">Loading map...</p>
    </div>
  )
})
const ScanButton = dynamic(() => import('@/components/ScanButton'), { ssr: false })
import AlertPanel from '@/components/AlertPanel'
import StatsCard from '@/components/StatsCard'
import { AlertTriangle, TrendingUp, MapPin, Activity } from 'lucide-react'

interface Stats {
  total_area_ha: number
  total_incidents: number
  avg_confidence: number
  rate_per_day_ha: number
}

export default function Home() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [selectedRegion, setSelectedRegion] = useState<string>('Pune, India')
  const [timeRange, setTimeRange] = useState<number>(30) // days
  const [loading, setLoading] = useState(true)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    fetchStats()
  }, [timeRange])

  const fetchStats = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/stats?days=${timeRange}`
      )
      const data = await response.json()
      if (data.success) {
        setStats(data)
      }
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>Illegal Deforestation Tracker</title>
        <meta name="description" content="Real-time satellite-based deforestation detection" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        {/* Header */}
        <header className="bg-gray-900/80 backdrop-blur-sm border-b border-gray-700 sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center space-x-3"
              >
                <AlertTriangle className="w-8 h-8 text-red-500" />
                <div>
                  <h1 className="text-2xl font-bold text-white">
                    Illegal Deforestation Tracker
                  </h1>
                  <p className="text-sm text-gray-400">
                    Real-time satellite monitoring powered by Google Earth Engine
                  </p>
                </div>
              </motion.div>

              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 bg-gray-800 px-4 py-2 rounded-lg">
                  <MapPin className="w-4 h-4 text-green-400" />
                  <span className="text-white text-sm">{selectedRegion}</span>
                </div>
                <div className="flex items-center space-x-2 bg-gray-800 px-4 py-2 rounded-lg">
                  <Activity className="w-4 h-4 text-blue-400" />
                  <span className="text-white text-sm">Live</span>
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                </div>
              </div>
            </div>
          </div>
        </header>

        <div className="container mx-auto px-4 py-6">
          {/* Stats Overview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6"
          >
            <StatsCard
              title="Total Forest Loss"
              value={stats?.total_area_ha || 0}
              unit="hectares"
              icon={<TrendingUp className="w-6 h-6" />}
              color="red"
              loading={loading}
            />
            <StatsCard
              title="Detected Incidents"
              value={stats?.total_incidents || 0}
              unit="events"
              icon={<AlertTriangle className="w-6 h-6" />}
              color="orange"
              loading={loading}
            />
            <StatsCard
              title="Average Confidence"
              value={stats?.avg_confidence ? stats.avg_confidence * 100 : 0}
              unit="%"
              icon={<Activity className="w-6 h-6" />}
              color="blue"
              loading={loading}
            />
            <StatsCard
              title="Daily Loss Rate"
              value={stats?.rate_per_day_ha || 0}
              unit="ha/day"
              icon={<TrendingUp className="w-6 h-6" />}
              color="purple"
              loading={loading}
            />
          </motion.div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Map Section */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="lg:col-span-3 bg-gray-800 rounded-xl shadow-2xl overflow-hidden"
            >
              <div className="h-[600px] relative">
                <MapView />
                {/* Scan Button */}
                <ScanButton />
              </div>
            </motion.div>

            {/* Alerts Panel */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="lg:col-span-1"
            >
              <AlertPanel />
            </motion.div>
          </div>

          {/* Footer Info */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="mt-6 text-center text-gray-400 text-sm"
          >
            <p>
              Data powered by{' '}
              <span className="text-blue-400">Google Earth Engine</span> •{' '}
              <span className="text-green-400">Hansen Global Forest Change</span> •{' '}
              <span className="text-purple-400">BigQuery</span>
            </p>
            <p className="mt-2">
              Last updated: {mounted ? new Date().toLocaleString() : 'Loading...'}
            </p>
          </motion.div>
        </div>
      </main>
    </>
  )
}
