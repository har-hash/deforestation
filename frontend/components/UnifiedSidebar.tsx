"use client"
import { useState, useEffect } from 'react'
import { Search, Activity, BarChart3, ChevronLeft, ChevronRight, MapPin, Calendar, Loader2, AlertTriangle } from 'lucide-react'

interface UnifiedSidebarProps {
  onScanRequest: (params: ScanParams) => void
  onAlertClick: (alert: any) => void
  alerts: any[]
  statistics: Statistics
}

interface ScanParams {
  lat: number
  lon: number
  radius: number
  startDate: string
  endDate: string
  method: 'hansen' | 'combination'
}

interface Statistics {
  total_area_ha: number
  total_incidents: number
  avg_confidence: number
  rate_per_day_ha: number
}

export default function UnifiedSidebar({ onScanRequest, onAlertClick, alerts, statistics }: UnifiedSidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [activeTab, setActiveTab] = useState<'scan' | 'results' | 'stats'>('scan')
  
  // Scan tab state
  const [query, setQuery] = useState('Pune, India')
  const [lat, setLat] = useState('')
  const [lon, setLon] = useState('')
  const [radius, setRadius] = useState(5000)
  const [method, setMethod] = useState<'hansen' | 'combination'>('hansen')
  const [startDate, setStartDate] = useState('2020-01-01')
  const [endDate, setEndDate] = useState(new Date().toISOString().slice(0, 10))
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [pickOnMapMode, setPickOnMapMode] = useState(false)
  
  // Stats tab state
  const [statsMode, setStatsMode] = useState<'global' | 'mapview'>('global')

  const parseCoordinates = (text: string) => {
    const m = text.trim().match(/^\s*([-+]?\d+\.?\d*)\s*,\s*([-+]?\d+\.?\d*)\s*$/)
    if (!m) return null
    const la = parseFloat(m[1]); const lo = parseFloat(m[2])
    if (Number.isFinite(la) && Number.isFinite(lo)) return { lat: la, lon: lo }
    return null
  }

  const geocode = async (text: string) => {
    const resp = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(text)}&format=json&limit=1`, {
      headers: { 
        'Accept': 'application/json',
        'User-Agent': 'DeforestationTracker/1.0'
      }
    })
    
    if (resp.status === 429) {
      throw new Error('Rate limit exceeded. Please wait a moment and try again.')
    }
    
    const arr = await resp.json()
    if (Array.isArray(arr) && arr.length) {
      return { lat: parseFloat(arr[0].lat), lon: parseFloat(arr[0].lon) }
    }
    throw new Error('Location not found')
  }

  const startScan = async () => {
    try {
      setLoading(true)
      setError(null)
      let coords: { lat: number; lon: number } | null = null
      
      if (lat && lon && !isNaN(Number(lat)) && !isNaN(Number(lon))) {
        coords = { lat: Number(lat), lon: Number(lon) }
      } else {
        coords = parseCoordinates(query) || await geocode(query)
      }

      onScanRequest({
        lat: coords.lat,
        lon: coords.lon,
        radius: Number(radius) || 5000,
        startDate,
        endDate,
        method
      })
      
      // Switch to results tab after scan starts
      setTimeout(() => setActiveTab('results'), 1000)
    } catch (e: any) {
      setError(e?.message || 'Failed to scan')
    } finally {
      setLoading(false)
    }
  }

  const enablePickOnMap = () => {
    setPickOnMapMode(true)
    // @ts-ignore
    window.dispatchEvent(new CustomEvent('enable-map-pick', { 
      detail: { radius, method, startDate, endDate } 
    }))
  }

  // Listen for map pick completion
  useEffect(() => {
    const handler = () => {
      setPickOnMapMode(false)
    }
    // @ts-ignore
    window.addEventListener('map-pick-complete', handler)
    return () => {
      // @ts-ignore
      window.removeEventListener('map-pick-complete', handler)
    }
  }, [])

  const tabs = [
    { id: 'scan', label: 'Scan', icon: Search },
    { id: 'results', label: 'Results', icon: Activity },
    { id: 'stats', label: 'Statistics', icon: BarChart3 }
  ]

  return (
    <>
      {/* Main Sidebar */}
      <div 
        className={`fixed left-0 top-0 h-full bg-gray-900 text-white shadow-2xl transition-all duration-300 z-[1000] ${
          isCollapsed ? 'w-16' : 'w-96'
        }`}
      >
        {/* Header with Collapse Button */}
        <div className="h-16 border-b border-gray-700 flex items-center justify-between px-4">
          {!isCollapsed && (
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-6 h-6 text-red-500" />
              <span className="font-bold text-lg">Control Center</span>
            </div>
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
          >
            {isCollapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
          </button>
        </div>

        {!isCollapsed && (
          <>
            {/* Tab Navigation */}
            <div className="flex border-b border-gray-700">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`flex-1 flex items-center justify-center gap-2 py-3 transition-colors ${
                      activeTab === tab.id
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="text-sm font-medium">{tab.label}</span>
                  </button>
                )
              })}
            </div>

            {/* Tab Content */}
            <div className="h-[calc(100vh-128px)] overflow-y-auto">
              {/* SCAN TAB */}
              {activeTab === 'scan' && (
                <div className="p-4 space-y-4">
                  {loading && (
                    <div className="bg-blue-900/50 border border-blue-500 rounded-lg p-3 flex items-center gap-3">
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span className="text-sm">Analyzing satellite data...</span>
                    </div>
                  )}

                  <div>
                    <label className="text-xs text-gray-400 mb-2 block">📍 Location</label>
                    <input 
                      value={query} 
                      onChange={(e)=>setQuery(e.target.value)} 
                      placeholder="Enter place name or coordinates"
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs text-gray-400 mb-2 block">Latitude</label>
                      <input 
                        value={lat} 
                        onChange={(e)=>setLat(e.target.value)} 
                        placeholder="18.5204"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-gray-400 mb-2 block">Longitude</label>
                      <input 
                        value={lon} 
                        onChange={(e)=>setLon(e.target.value)} 
                        placeholder="73.8567"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="text-xs text-gray-400 mb-2 block">🎯 Scan Radius (meters)</label>
                    <input 
                      type="number" 
                      min={500} 
                      step={100} 
                      value={radius} 
                      onChange={(e)=>setRadius(Number(e.target.value))}
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                    />
                  </div>

                  <div>
                    <label className="text-xs text-gray-400 mb-2 block">🔬 Detection Method</label>
                    <select 
                      value={method} 
                      onChange={(e)=>setMethod(e.target.value as any)}
                      className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                    >
                      <option value="hansen">Hansen (Fast & Reliable)</option>
                      <option value="combination">Combination (Highest Accuracy)</option>
                    </select>
                  </div>

                  <div className="border-t border-gray-700 pt-4">
                    <div className="flex items-center gap-2 mb-3">
                      <Calendar className="w-4 h-4 text-blue-400" />
                      <label className="text-xs text-gray-400 font-semibold">DATE RANGE</label>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">Start Date</label>
                        <input 
                          type="date" 
                          value={startDate} 
                          onChange={(e)=>setStartDate(e.target.value)} 
                          max={endDate}
                          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                        />
                      </div>
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">End Date</label>
                        <input 
                          type="date" 
                          value={endDate} 
                          onChange={(e)=>setEndDate(e.target.value)} 
                          min={startDate}
                          max={new Date().toISOString().slice(0, 10)}
                          className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                        />
                      </div>
                    </div>
                  </div>

                  {error && (
                    <div className="bg-red-900/50 border border-red-500 rounded-lg p-3 text-sm text-red-200">
                      {error}
                    </div>
                  )}

                  <div className="space-y-2 pt-2">
                    <button 
                      disabled={loading} 
                      onClick={startScan}
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg shadow-lg disabled:opacity-50 transition-colors"
                    >
                      {loading ? 'Scanning...' : 'Start Scan'}
                    </button>
                    <button 
                      type="button" 
                      onClick={enablePickOnMap}
                      disabled={pickOnMapMode}
                      className="w-full bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 rounded-lg transition-colors disabled:opacity-50"
                    >
                      {pickOnMapMode ? 'Click on Map...' : 'Pick on Map'}
                    </button>
                  </div>
                </div>
              )}

              {/* RESULTS TAB */}
              {activeTab === 'results' && (
                <div className="p-4 space-y-3">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-sm text-gray-400">DETECTED INCIDENTS</h3>
                    <span className="text-xs bg-red-900/50 text-red-300 px-2 py-1 rounded">
                      {alerts.length} Active
                    </span>
                  </div>
                  
                  {alerts.length === 0 ? (
                    <div className="text-center py-12 text-gray-500">
                      <Activity className="w-12 h-12 mx-auto mb-3 opacity-50" />
                      <p className="text-sm">No incidents detected</p>
                      <p className="text-xs mt-1">Run a scan to see results</p>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {alerts.map((alert, idx) => (
                        <button
                          key={idx}
                          onClick={() => onAlertClick(alert)}
                          className="w-full text-left bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg p-3 transition-colors"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <span className={`text-xs font-semibold px-2 py-1 rounded ${
                              alert.severity === 'critical' ? 'bg-red-900 text-red-200' :
                              alert.severity === 'high' ? 'bg-orange-900 text-orange-200' :
                              'bg-yellow-900 text-yellow-200'
                            }`}>
                              {alert.severity?.toUpperCase() || 'MODERATE'}
                            </span>
                            <span className="text-xs text-gray-400">
                              {alert.area_ha?.toFixed(1) || 0} ha
                            </span>
                          </div>
                          <p className="text-sm text-gray-300 mb-1">{alert.location || 'Unknown location'}</p>
                          <p className="text-xs text-gray-500">
                            {alert.timestamp ? new Date(alert.timestamp).toLocaleString() : 'Recent'}
                          </p>
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* STATISTICS TAB */}
              {activeTab === 'stats' && (
                <div className="p-4 space-y-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-sm text-gray-400">STATISTICS</h3>
                    <div className="flex bg-gray-800 rounded-lg p-1">
                      <button
                        onClick={() => setStatsMode('global')}
                        className={`px-3 py-1 text-xs rounded transition-colors ${
                          statsMode === 'global' ? 'bg-blue-600 text-white' : 'text-gray-400'
                        }`}
                      >
                        Global
                      </button>
                      <button
                        onClick={() => setStatsMode('mapview')}
                        className={`px-3 py-1 text-xs rounded transition-colors ${
                          statsMode === 'mapview' ? 'bg-blue-600 text-white' : 'text-gray-400'
                        }`}
                      >
                        Map View
                      </button>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div className="bg-gradient-to-br from-red-900/30 to-red-800/20 border border-red-800/50 rounded-lg p-4">
                      <div className="text-xs text-red-300 mb-1">Total Forest Loss</div>
                      <div className="text-3xl font-bold text-white">
                        {statistics.total_area_ha?.toFixed(1) || 0}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">hectares</div>
                    </div>

                    <div className="bg-gradient-to-br from-orange-900/30 to-orange-800/20 border border-orange-800/50 rounded-lg p-4">
                      <div className="text-xs text-orange-300 mb-1">Detected Incidents</div>
                      <div className="text-3xl font-bold text-white">
                        {statistics.total_incidents || 0}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">events</div>
                    </div>

                    <div className="bg-gradient-to-br from-blue-900/30 to-blue-800/20 border border-blue-800/50 rounded-lg p-4">
                      <div className="text-xs text-blue-300 mb-1">Average Confidence</div>
                      <div className="text-3xl font-bold text-white">
                        {((statistics.avg_confidence || 0) * 100).toFixed(0)}%
                      </div>
                      <div className="text-xs text-gray-400 mt-1">detection accuracy</div>
                    </div>

                    <div className="bg-gradient-to-br from-purple-900/30 to-purple-800/20 border border-purple-800/50 rounded-lg p-4">
                      <div className="text-xs text-purple-300 mb-1">Daily Loss Rate</div>
                      <div className="text-3xl font-bold text-white">
                        {statistics.rate_per_day_ha?.toFixed(2) || 0}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">ha/day</div>
                    </div>
                  </div>

                  {statsMode === 'mapview' && (
                    <div className="bg-blue-900/20 border border-blue-700/50 rounded-lg p-3 text-xs text-blue-200">
                      💡 Pan or zoom the map to update statistics for the current view
                    </div>
                  )}
                </div>
              )}
            </div>
          </>
        )}

        {/* Collapsed State - Vertical Icons */}
        {isCollapsed && (
          <div className="flex flex-col items-center gap-4 pt-4">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    setIsCollapsed(false)
                    setActiveTab(tab.id as any)
                  }}
                  className={`p-3 rounded-lg transition-colors ${
                    activeTab === tab.id ? 'bg-blue-600' : 'hover:bg-gray-800'
                  }`}
                  title={tab.label}
                >
                  <Icon className="w-5 h-5" />
                </button>
              )
            })}
          </div>
        )}
      </div>

      {/* Pick on Map Instruction Overlay */}
      {pickOnMapMode && (
        <div className="fixed inset-0 pointer-events-none z-[999] flex items-center justify-center">
          <div className="bg-blue-600 text-white px-6 py-3 rounded-full shadow-2xl animate-pulse">
            <MapPin className="w-5 h-5 inline mr-2" />
            Click on the map to select scan center
          </div>
        </div>
      )}
    </>
  )
}


