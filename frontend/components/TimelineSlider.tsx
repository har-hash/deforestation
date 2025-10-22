import { motion } from 'framer-motion'
import { Calendar } from 'lucide-react'

interface TimelineSliderProps {
  value: number
  onChange: (value: number) => void
}

export default function TimelineSlider({ value, onChange }: TimelineSliderProps) {
  const timeRanges = [
    { label: '7 days', value: 7 },
    { label: '30 days', value: 30 },
    { label: '90 days', value: 90 },
    { label: '180 days', value: 180 },
    { label: '1 year', value: 365 }
  ]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gray-900/90 backdrop-blur-md rounded-xl p-4 shadow-2xl border border-gray-700"
    >
      <div className="flex items-center space-x-3 mb-3">
        <Calendar className="w-5 h-5 text-blue-400" />
        <h3 className="text-white font-semibold">Time Period</h3>
      </div>

      <div className="flex items-center space-x-2">
        {timeRanges.map((range) => (
          <button
            key={range.value}
            onClick={() => onChange(range.value)}
            className={`flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
              value === range.value
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/50'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
            }`}
          >
            {range.label}
          </button>
        ))}
      </div>

      {/* Custom range slider */}
      <div className="mt-4">
        <label className="block text-xs text-gray-400 mb-2">
          Custom: {value} days
        </label>
        <input
          type="range"
          min="1"
          max="365"
          value={value}
          onChange={(e) => onChange(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
          style={{
            background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${(value / 365) * 100}%, #374151 ${(value / 365) * 100}%, #374151 100%)`
          }}
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>1 day</span>
          <span>1 year</span>
        </div>
      </div>
    </motion.div>
  )
}



