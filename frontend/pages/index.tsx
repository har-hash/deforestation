import { useState, useEffect } from 'react'
import Head from 'next/head'
import dynamic from 'next/dynamic'

// Load components dynamically to avoid SSR issues
const MapView = dynamic(() => import('@/components/MapView'), { ssr: false })
const UnifiedSidebar = dynamic(() => import('@/components/UnifiedSidebar'), { ssr: false })

interface Stats {
  total_area_ha: number
  total_incidents: number
  avg_confidence: number
  rate_per_day_ha: number
}

interface ScanParams {
  lat: number
  lon: number
  radius: number
  startDate: string
  endDate: string
  method: 'hansen' | 'combination'
}

export default function Home() {
  const [stats, setStats] = useState<Stats>({
    total_area_ha: 0,
    total_incidents: 0,
    avg_confidence: 0,
    rate_per_day_ha: 0
  })
  const [alerts, setAlerts] = useState<any[]>([])
  const [timeRange, setTimeRange] = useState<number>(30)

  useEffect(() => {
    fetchStats()
    fetchAlerts()
  }, [timeRange])

  const fetchStats = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/stats?days=${timeRange}`
      )
      const data = await response.json()
      if (data.success || data.total_area_ha !== undefined) {
        setStats(data)
      }
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const fetchAlerts = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/alerts?limit=20`
      )
      const data = await response.json()
      if (data.success && data.alerts) {
        setAlerts(data.alerts)
      }
    } catch (error) {
      console.error('Error fetching alerts:', error)
    }
  }

  const handleScanRequest = (params: ScanParams) => {
    // Dispatch scan event to map
    // @ts-ignore
    window.dispatchEvent(new CustomEvent('start-scan', { detail: params }))
  }

  const handleAlertClick = (alert: any) => {
    // Zoom map to alert location
    // @ts-ignore
    window.dispatchEvent(new CustomEvent('zoom-to-alert', { detail: alert }))
  }

  return (
    <>
      <Head>
        <title>Illegal Deforestation Tracker - Command Center</title>
        <meta name="description" content="Real-time satellite-based deforestation detection" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="h-screen w-screen overflow-hidden bg-gray-900 flex">
        {/* Unified Left Sidebar */}
        <UnifiedSidebar
          onScanRequest={handleScanRequest}
          onAlertClick={handleAlertClick}
          alerts={alerts}
          statistics={stats}
        />

        {/* Full-Screen Map (Right Side) */}
        <div className="flex-1 h-full relative">
          <MapView />
        </div>
      </main>
    </>
  )
}
