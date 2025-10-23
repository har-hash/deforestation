"use client"
import { MapContainer, TileLayer, Polygon, Popup, Circle, useMap, useMapEvents } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { useEffect, useMemo, useState } from 'react'

function Recenter({ center, zoom }: { center: [number, number]; zoom: number }) {
  const map = useMap()
  useEffect(() => {
    map.setView(center, zoom, { animate: true })
  }, [center, zoom, map])
  return null
}

export default function MapView() {
  const [center, setCenter] = useState<[number, number]>([18.5204, 73.8567])
  const [zoom, setZoom] = useState(11)
  const [features, setFeatures] = useState<any[]>([])
  const [notice, setNotice] = useState<string>('')
  const [scanCircle, setScanCircle] = useState<{ center: [number, number]; radius: number } | null>(null)
  const [pickOnMap, setPickOnMap] = useState(false)
  const [pickParams, setPickParams] = useState<{ radius: number; method: string; startDate?: string; endDate?: string }>({ radius: 5000, method: 'hansen' })
  const [scanning, setScanning] = useState(false)

  useEffect(() => {
    const performScan = async (lat: number, lon: number, radius?: number, method?: string, startDate?: string, endDate?: string) => {
      try {
        setScanning(true)
        setFeatures([]) // Clear previous results
        setScanCircle({ center: [lat, lon], radius: Number(radius || 5000) })
        setCenter([lat, lon])
        setZoom(13)
        
        const base = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/$/, '')
        const url = `${base}/api/forest-loss?lat=${lat}&lon=${lon}&radius=${radius || 5000}&start_date=${startDate || '2020-01-01'}&end_date=${endDate || new Date().toISOString().slice(0,10)}&method=${method || 'hansen'}`
        const res = await fetch(url)
        const data = await res.json()
        console.log('🔍 Backend response:', data)
        const fc = data?.data?.features || data?.features || []
        const warning = data?.data?.warning || data?.warning || null
        console.log('🔍 Extracted features:', fc)
        console.log('🔍 Feature count:', fc.length)
        if (fc.length > 0) {
          console.log('🔍 First feature:', JSON.stringify(fc[0], null, 2))
        }
        setFeatures(fc)
        if (!fc.length) {
          setNotice('No deforestation detected for this area and date range.')
          setTimeout(()=>setNotice(''), 5000)
        } else if (warning) {
          setNotice(`⚠️ ${warning}`)
          setTimeout(()=>setNotice(''), 8000)
        } else {
          setNotice(`Found ${fc.length} deforestation polygon${fc.length > 1 ? 's' : ''}`)
          setTimeout(()=>setNotice(''), 5000)
        }
        
        // Keep circle visible for 3 seconds after results
        setTimeout(() => setScanCircle(null), 3000)
      } catch (err) {
        console.error('Scan failed:', err)
        setNotice('Scan failed. Please try again.')
        setTimeout(()=>setNotice(''), 3000)
        setScanCircle(null)
      } finally {
        setScanning(false)
      }
    }

    // scan event from the button/panel
    const handler = async (e: CustomEvent) => {
      try {
        const { lat, lon, radius, startDate, endDate, method } = e.detail || {}
        if (typeof lat !== 'number' || typeof lon !== 'number') return
        await performScan(lat, lon, radius, method, startDate, endDate)
      } catch (err) {
        console.error('Scan failed:', err)
      }
    }

    // enable pick-mode event
    const enablePick = (e: CustomEvent) => {
      const { radius, method, startDate, endDate } = e.detail || {}
      setPickParams({ 
        radius: Number(radius || 5000), 
        method: String(method || 'hansen'),
        startDate,
        endDate
      })
      setPickOnMap(true)
    }

    // zoom to alert event
    const zoomToAlert = (e: CustomEvent) => {
      const alert = e.detail
      if (alert && alert.coordinates) {
        // Extract center from polygon coordinates
        const coords = alert.coordinates[0]
        if (coords && coords.length > 0) {
          const lats = coords.map((c: number[]) => c[1])
          const lons = coords.map((c: number[]) => c[0])
          const centerLat = (Math.min(...lats) + Math.max(...lats)) / 2
          const centerLon = (Math.min(...lons) + Math.max(...lons)) / 2
          setCenter([centerLat, centerLon])
          setZoom(14)
        }
      }
    }

    // @ts-ignore
    window.addEventListener('start-scan', handler as EventListener)
    // @ts-ignore
    window.addEventListener('enable-map-pick', enablePick as EventListener)
    // @ts-ignore
    window.addEventListener('zoom-to-alert', zoomToAlert as EventListener)
    return () => {
      // @ts-ignore
      window.removeEventListener('start-scan', handler as EventListener)
      // @ts-ignore
      window.removeEventListener('enable-map-pick', enablePick as EventListener)
      // @ts-ignore
      window.removeEventListener('zoom-to-alert', zoomToAlert as EventListener)
    }
  }, [])

  // Click-to-pick handler component
  function ClickPicker() {
    useMapEvents({
      click: (e) => {
        if (!pickOnMap) return
        const { lat, lng } = e.latlng
        // dispatch same flow as start-scan
        // @ts-ignore
        window.dispatchEvent(new CustomEvent('start-scan', { 
          detail: { 
            lat, 
            lon: lng, 
            radius: pickParams.radius, 
            method: pickParams.method,
            startDate: pickParams.startDate,
            endDate: pickParams.endDate
          } 
        }))
        setPickOnMap(false)
        // Notify sidebar that pick is complete
        // @ts-ignore
        window.dispatchEvent(new CustomEvent('map-pick-complete'))
      }
    })
    return null
  }

  return (
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ height: '100%', width: '100%' }}
      zoomControl={true}
    >
      <Recenter center={center} zoom={zoom} />
      <TileLayer
        attribution='Tiles &copy; Esri'
        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        maxZoom={19}
      />
      <ClickPicker />

      {scanCircle && (
        <Circle
          center={scanCircle.center}
          radius={scanCircle.radius}
          pathOptions={{ color: '#3B82F6', weight: 2, fillColor: '#3B82F6', fillOpacity: 0.1 }}
        />
      )}

      {/* Loading spinner */}
      {scanning && (
        <div className="absolute inset-0 z-[999] bg-black/20 flex items-center justify-center">
          <div className="bg-white/95 rounded-xl shadow-2xl p-6 flex flex-col items-center gap-4">
            <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin" />
            <div className="text-gray-800 font-medium">Analyzing satellite data...</div>
            <div className="text-sm text-gray-500">This may take a few seconds</div>
          </div>
        </div>
      )}

      {/* Info toast */}
      {notice && (
        <div className="absolute top-4 right-4 z-[1000] bg-gray-900/90 text-white px-4 py-2 rounded-lg shadow">
          {notice}
        </div>
      )}

      {features.map((f, idx) => {
        const geom = f?.geometry
        const confidence = Number(f?.properties?.confidence ?? 0)
        const color = confidence >= 0.9 ? '#dc2626' : confidence >= 0.8 ? '#ea580c' : confidence >= 0.7 ? '#f59e0b' : '#fbbf24'

        console.log(`🎨 Rendering feature ${idx}:`, geom?.type, 'coords:', geom?.coordinates?.[0]?.length)

        if (!geom) {
          console.log(`❌ Feature ${idx} has no geometry`)
          return null
        }
        if (geom.type === 'Polygon') {
          const coords = (geom.coordinates?.[0] || []).map((c: number[]) => [c[1], c[0]] as [number, number])
          console.log(`📍 Polygon ${idx} first 3 coords:`, coords.slice(0, 3))
          return (
            <Polygon key={idx} positions={coords} pathOptions={{ color, fillColor: color, fillOpacity: 0.4, weight: 2 }}>
              <Popup>
                <div className="text-sm space-y-1">
                  <div className="font-semibold text-red-600">Deforestation</div>
                  <div><strong>Area:</strong> {Number(f?.properties?.area_ha ?? 0).toFixed(2)} ha</div>
                  <div><strong>Confidence:</strong> {(confidence * 100).toFixed(0)}%</div>
                  <div><strong>Detected:</strong> {f?.properties?.timestamp ? new Date(f.properties.timestamp).toLocaleDateString() : 'N/A'}</div>
                </div>
              </Popup>
            </Polygon>
          )
        }
        if (geom.type === 'MultiPolygon') {
          const polys: number[][][][] = geom.coordinates || []
          return (
            <>
              {polys.map((poly, pIdx) => {
                const ring: number[][] = poly?.[0] || []
                const coords = ring.map((c: number[]) => [c[1], c[0]] as [number, number])
                return (
                  <Polygon key={`${idx}-${pIdx}`} positions={coords} pathOptions={{ color, fillColor: color, fillOpacity: 0.4, weight: 2 }}>
                    <Popup>
                      <div className="text-sm space-y-1">
                        <div className="font-semibold text-red-600">Deforestation</div>
                        <div><strong>Area:</strong> {Number(f?.properties?.area_ha ?? 0).toFixed(2)} ha</div>
                        <div><strong>Confidence:</strong> {(confidence * 100).toFixed(0)}%</div>
                        <div><strong>Detected:</strong> {f?.properties?.timestamp ? new Date(f.properties.timestamp).toLocaleDateString() : 'N/A'}</div>
                      </div>
                    </Popup>
                  </Polygon>
                )
              })}
            </>
          )
        }
        return null
      })}
    </MapContainer>
  )
}
