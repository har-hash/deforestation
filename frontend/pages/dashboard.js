import { useState, useEffect } from 'react'
import Head from 'next/head'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { TrendingUp, AlertTriangle, Map as MapIcon, Activity } from 'lucide-react'
import { motion } from 'framer-motion'

export default function Dashboard() {
  const [timelineData, setTimelineData] = useState([])
  const [regionalData, setRegionalData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch timeline data
      const timelineResponse = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/stats/timeline?interval=month`
      )
      const timelineResult = await timelineResponse.json()
      if (timelineResult.success) {
        setTimelineData(timelineResult.timeline)
      }

      // Fetch regional data
      const regionResponse = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/stats/regions?days=90`
      )
      const regionResult = await regionResponse.json()
      if (regionResult.success) {
        setRegionalData(regionResult.regions)
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#dc2626', '#ea580c', '#f59e0b', '#fbbf24', '#22c55e', '#3b82f6']

  return (
    <>
      <Head>
        <title>Analytics Dashboard - Deforestation Tracker</title>
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        {/* Header */}
        <header className="bg-gray-900/80 backdrop-blur-sm border-b border-gray-700">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center space-x-3"
              >
                <Activity className="w-8 h-8 text-blue-500" />
                <div>
                  <h1 className="text-2xl font-bold text-white">
                    Analytics Dashboard
                  </h1>
                  <p className="text-sm text-gray-400">
                    Detailed insights and trends
                  </p>
                </div>
              </motion.div>

              <a
                href="/"
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center space-x-2"
              >
                <MapIcon className="w-4 h-4" />
                <span>Back to Map</span>
              </a>
            </div>
          </div>
        </header>

        <div className="container mx-auto px-4 py-8">
          {loading ? (
            <div className="flex items-center justify-center h-96">
              <div className="spinner" />
            </div>
          ) : (
            <>
              {/* Timeline Chart */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gray-800 rounded-xl p-6 mb-8"
              >
                <h2 className="text-xl font-bold text-white mb-4 flex items-center">
                  <TrendingUp className="w-6 h-6 mr-2 text-blue-500" />
                  Deforestation Timeline
                </h2>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={timelineData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis
                      dataKey="period"
                      stroke="#9ca3af"
                      tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', year: '2-digit' })}
                    />
                    <YAxis stroke="#9ca3af" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                      labelStyle={{ color: '#fff' }}
                    />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="total_area_ha"
                      stroke="#ef4444"
                      strokeWidth={2}
                      name="Area Lost (ha)"
                      dot={{ fill: '#ef4444', r: 4 }}
                    />
                    <Line
                      type="monotone"
                      dataKey="incidents"
                      stroke="#3b82f6"
                      strokeWidth={2}
                      name="Incidents"
                      dot={{ fill: '#3b82f6', r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </motion.div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Regional Bar Chart */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="bg-gray-800 rounded-xl p-6"
                >
                  <h2 className="text-xl font-bold text-white mb-4 flex items-center">
                    <AlertTriangle className="w-6 h-6 mr-2 text-orange-500" />
                    Regional Breakdown
                  </h2>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={regionalData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                      <XAxis dataKey="region" stroke="#9ca3af" />
                      <YAxis stroke="#9ca3af" />
                      <Tooltip
                        contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                        labelStyle={{ color: '#fff' }}
                      />
                      <Legend />
                      <Bar dataKey="total_area_ha" fill="#ef4444" name="Area Lost (ha)" />
                    </BarChart>
                  </ResponsiveContainer>
                </motion.div>

                {/* Regional Pie Chart */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="bg-gray-800 rounded-xl p-6"
                >
                  <h2 className="text-xl font-bold text-white mb-4">
                    Regional Distribution
                  </h2>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={regionalData}
                        dataKey="total_area_ha"
                        nameKey="region"
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        label={(entry) => `${entry.region}: ${entry.total_area_ha.toFixed(1)} ha`}
                      >
                        {regionalData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip
                        contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </motion.div>
              </div>

              {/* Regional Details Table */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-gray-800 rounded-xl p-6 mt-8"
              >
                <h2 className="text-xl font-bold text-white mb-4">
                  Detailed Regional Statistics
                </h2>
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="border-b border-gray-700">
                        <th className="pb-3 text-gray-300">Region</th>
                        <th className="pb-3 text-gray-300">Incidents</th>
                        <th className="pb-3 text-gray-300">Total Area (ha)</th>
                        <th className="pb-3 text-gray-300">Avg Confidence</th>
                      </tr>
                    </thead>
                    <tbody>
                      {regionalData.map((region, index) => (
                        <tr key={index} className="border-b border-gray-700/50">
                          <td className="py-3 text-white">{region.region}</td>
                          <td className="py-3 text-gray-300">{region.incidents}</td>
                          <td className="py-3 text-red-400">{region.total_area_ha.toFixed(2)}</td>
                          <td className="py-3 text-green-400">{(region.avg_confidence * 100).toFixed(0)}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </motion.div>
            </>
          )}
        </div>
      </main>
    </>
  )
}



