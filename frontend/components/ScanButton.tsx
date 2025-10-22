import { useState } from 'react'
import { Search, X, Calendar } from 'lucide-react'

export default function ScanButton() {
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState('Pune, India')
  const [lat, setLat] = useState('')
  const [lon, setLon] = useState('')
  const [radius, setRadius] = useState(5000)
  const [method, setMethod] = useState<'hansen' | 'combination'>('hansen')
  const [startDate, setStartDate] = useState('2020-01-01')
  const [endDate, setEndDate] = useState(new Date().toISOString().slice(0, 10))
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const parseCoordinates = (text: string) => {
    const m = text.trim().match(/^\s*([-+]?\d+\.?\d*)\s*,\s*([-+]?\d+\.?\d*)\s*$/)
    if (!m) return null
    const la = parseFloat(m[1]); const lo = parseFloat(m[2])
    if (Number.isFinite(la) && Number.isFinite(lo)) return { lat: la, lon: lo }
    return null
  }

  const geocode = async (text: string) => {
    const resp = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(text)}&format=json&limit=1`, {
      headers: { 'Accept': 'application/json' }
    })
    const arr = await resp.json()
    if (Array.isArray(arr) && arr.length) {
      return { lat: parseFloat(arr[0].lat), lon: parseFloat(arr[0].lon) }
    }
    throw new Error('Location not found')
  }

  const startScan = async () => {
    try {
      setLoading(true); setError(null)
      let coords: { lat: number; lon: number } | null = null
      // priority: explicit coordinates, else parse query as coords, else geocode
      if (lat && lon && !isNaN(Number(lat)) && !isNaN(Number(lon))) {
        coords = { lat: Number(lat), lon: Number(lon) }
      } else {
        coords = parseCoordinates(query) || await geocode(query)
      }

      const detail = {
        lat: coords.lat,
        lon: coords.lon,
        radius: Number(radius) || 5000,
        startDate,
        endDate,
        method
      }
      // @ts-ignore
      window.dispatchEvent(new CustomEvent('start-scan', { detail }))
      // Keep panel open to show loading state
      // setOpen(false)
    } catch (e: any) {
      setError(e?.message || 'Failed to scan')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Floating button */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="fixed left-4 top-20 z-[1000] bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-2"
        title="Scan for deforestation"
      >
        <Search className="w-5 h-5" />
        <span className="font-medium">Scan for Deforestation</span>
      </button>

      {/* Panel */}
      {open && (
        <div className="fixed left-4 top-36 z-[1001] w-[360px] bg-white text-gray-800 rounded-xl shadow-2xl border border-gray-200">
          <div className="flex items-center justify-between px-4 py-3 border-b">
            <div className="font-semibold">Scan Area</div>
            <button onClick={() => setOpen(false)} className="p-1 rounded hover:bg-gray-100">
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="p-4 space-y-3">
            <div>
              <label className="text-xs text-gray-600">Search place (or enter "lat, lon")</label>
              <input value={query} onChange={(e)=>setQuery(e.target.value)} placeholder="Pune, India or 18.52, 73.85" className="w-full mt-1 px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200 outline-none" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-gray-600">Latitude (optional)</label>
                <input value={lat} onChange={(e)=>setLat(e.target.value)} placeholder="18.5204" className="w-full mt-1 px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200 outline-none" />
              </div>
              <div>
                <label className="text-xs text-gray-600">Longitude (optional)</label>
                <input value={lon} onChange={(e)=>setLon(e.target.value)} placeholder="73.8567" className="w-full mt-1 px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200 outline-none" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-gray-600">Radius (meters)</label>
                <input type="number" min={500} step={100} value={radius} onChange={(e)=>setRadius(Number(e.target.value))} className="w-full mt-1 px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200 outline-none" />
              </div>
              <div>
                <label className="text-xs text-gray-600">Method</label>
                <select value={method} onChange={(e)=>setMethod(e.target.value as any)} className="w-full mt-1 px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200 outline-none">
                  <option value="hansen">Hansen</option>
                  <option value="combination">Combination</option>
                </select>
              </div>
            </div>

            <div className="border-t pt-3">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4 text-gray-600" />
                <label className="text-xs text-gray-600 font-medium">Date Range</label>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-gray-500">Start Date</label>
                  <input 
                    type="date" 
                    value={startDate} 
                    onChange={(e)=>setStartDate(e.target.value)} 
                    max={endDate}
                    className="w-full mt-1 px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200 outline-none text-sm" 
                  />
                </div>
                <div>
                  <label className="text-xs text-gray-500">End Date</label>
                  <input 
                    type="date" 
                    value={endDate} 
                    onChange={(e)=>setEndDate(e.target.value)} 
                    min={startDate}
                    max={new Date().toISOString().slice(0, 10)}
                    className="w-full mt-1 px-3 py-2 border rounded-lg focus:ring focus:ring-blue-200 outline-none text-sm" 
                  />
                </div>
              </div>
            </div>

            {error && <div className="text-xs text-red-600">{error}</div>}

            <button disabled={loading} onClick={startScan} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg shadow disabled:opacity-60">
              {loading ? 'Scanning...' : 'Start Scan'}
            </button>
            <button type="button" onClick={()=>{
              // enable pick-on-map with current settings
              // @ts-ignore
              window.dispatchEvent(new CustomEvent('enable-map-pick', { detail: { radius, method, startDate, endDate } }))
              setOpen(false)
            }} className="w-full mt-2 bg-white border border-gray-300 hover:bg-gray-50 text-gray-800 font-medium py-2.5 rounded-lg">
              Pick on Map
            </button>
          </div>
        </div>
      )}
    </>
  )
}


