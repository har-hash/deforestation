# Frontend - Illegal Deforestation Tracker

Next.js frontend with Google Maps visualization for real-time deforestation monitoring.

## 📁 Project Structure

```
frontend/
├── pages/
│   ├── _app.tsx           # App wrapper
│   ├── index.tsx          # Main dashboard page
│   └── dashboard.js       # (Optional) Additional dashboard
├── components/
│   ├── MapView.tsx        # Google Maps with satellite layer
│   ├── AlertPanel.tsx     # Real-time alerts sidebar
│   ├── StatsCard.tsx      # Statistics display cards
│   └── TimelineSlider.tsx # Time period selector
├── styles/
│   └── globals.css        # Global styles with Tailwind
├── public/
│   └── favicon.ico        # App icon
├── package.json           # Dependencies
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── .env.local            # Environment variables
```

## 🔧 Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local` file:

```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Google Maps API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Enable **Maps JavaScript API**
3. Create credentials (API Key)
4. (Optional) Restrict key to your domain
5. Add key to `.env.local`

## 🚀 Running the Application

### Development Mode
```bash
npm run dev
```
Opens at `http://localhost:3000`

### Production Build
```bash
npm run build
npm start
```

### Linting
```bash
npm run lint
```

## 🎨 Features

### MapView Component
- Google Maps with satellite layer
- Real-time deforestation polygon overlays
- Color-coded by confidence level
- Interactive info windows
- Automatic data refresh

### AlertPanel Component
- Live alerts feed
- Severity-based color coding
- Time-relative timestamps
- Auto-refresh every 30 seconds
- Detailed alert information

### StatsCard Component
- Animated statistics display
- Color-coded by metric type
- Responsive design
- Loading states
- Formatted large numbers

### TimelineSlider Component
- Quick time period selection
- Custom range slider
- Smooth animations
- Real-time data updates

## 🗺️ Google Maps Integration

### Satellite Layer
```typescript
mapTypeId: 'satellite'
```

### Polygon Overlay
```typescript
const polygon = new google.maps.Polygon({
  paths: coordinates,
  strokeColor: color,
  strokeOpacity: 0.8,
  strokeWeight: 2,
  fillColor: color,
  fillOpacity: 0.4
})
```

### Color Coding
- **Red** (#dc2626): Critical (confidence ≥ 90%)
- **Orange-Red** (#ea580c): High (confidence ≥ 80%)
- **Orange** (#f59e0b): Medium (confidence ≥ 70%)
- **Yellow** (#fbbf24): Low (confidence < 70%)

## 🎨 Styling

### TailwindCSS
Custom theme with forest-inspired colors:

```javascript
colors: {
  forest: {
    50: '#f0fdf4',
    ...
    900: '#14532d',
  },
  alert: {
    low: '#fbbf24',
    medium: '#f59e0b',
    high: '#ea580c',
    critical: '#dc2626',
  }
}
```

### Framer Motion Animations
- Page transitions
- Card hover effects
- Alert entry animations
- Loading states

## 📡 API Integration

### Fetch Statistics
```typescript
const response = await fetch(
  `${process.env.NEXT_PUBLIC_API_URL}/api/stats?days=${timeRange}`
)
```

### Fetch Forest Loss Data
```typescript
const response = await fetch(
  `${process.env.NEXT_PUBLIC_API_URL}/api/forest-loss?use_bigquery=true`
)
```

### Fetch Alerts
```typescript
const response = await fetch(
  `${process.env.NEXT_PUBLIC_API_URL}/api/alerts?limit=20`
)
```

## 🔄 State Management

### React Hooks
- `useState` - Component state
- `useEffect` - Side effects and data fetching
- `useRef` - DOM references and mutable values

### Data Refresh
- Stats: On time range change
- Alerts: Every 30 seconds
- Map data: On component mount

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px (1 column)
- **Tablet**: 768px - 1024px (2 columns)
- **Desktop**: > 1024px (4 columns for stats, 3+1 for map+alerts)

### Mobile Optimizations
- Touch-friendly controls
- Stacked layout
- Simplified map controls
- Collapsible alert panel

## 🎯 Performance Optimizations

### Next.js Features
- Automatic code splitting
- Image optimization
- Static generation where possible
- Fast Refresh for development

### Custom Optimizations
- Lazy loading for maps
- Debounced API calls
- Memoized components
- Efficient re-renders

## 🐛 Troubleshooting

### Maps Not Loading
```bash
# Check API key
echo $NEXT_PUBLIC_GOOGLE_MAPS_API_KEY

# Verify API is enabled in GCP
# Check browser console for errors
```

### API Connection Issues
```bash
# Check API URL
echo $NEXT_PUBLIC_API_URL

# Verify backend is running
curl http://localhost:8000/health

# Check CORS configuration
```

### Build Errors
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules
npm install

# Check TypeScript errors
npm run lint
```

## 🚢 Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

### Environment Variables on Vercel
1. Go to Project Settings
2. Add environment variables:
   - `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`
   - `NEXT_PUBLIC_API_URL`

### Netlify
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod
```

### Docker
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

## 🧪 Testing

### Component Testing
```bash
npm run test
```

### E2E Testing (if configured)
```bash
npm run test:e2e
```

## 📊 Data Visualization

### Stats Display
- Total forest loss (hectares)
- Number of incidents
- Average confidence
- Daily loss rate

### Timeline Visualization
- Time period selector
- Historical data comparison
- Trend analysis

### Map Visualization
- Satellite imagery base layer
- Deforestation polygons
- Confidence-based colors
- Interactive tooltips

## 🔐 Security

- Environment variables for API keys
- No sensitive data in client code
- API key restrictions in GCP
- HTTPS in production

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` | Google Maps API key | Yes |
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |

## 🎓 Technologies Used

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Framer Motion** - Animations
- **Google Maps API** - Mapping
- **Lucide React** - Icons
- **date-fns** - Date formatting
- **Axios** - HTTP client

## 📈 Future Enhancements

- [ ] User authentication
- [ ] Custom region selection
- [ ] Export reports (PDF/CSV)
- [ ] Email notifications
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Advanced filtering
- [ ] Comparison view

## 📧 Support

For frontend-specific issues:
1. Check browser console for errors
2. Verify environment variables
3. Test API endpoints directly
4. Review component props and state

## 🔗 Related Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
- [TailwindCSS](https://tailwindcss.com/docs)
- [Framer Motion](https://www.framer.com/motion/)



