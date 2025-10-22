# 🚀 Deforestation Tracker - Quick Start

## ✅ ALL FIXED! Ready to Use!

### 🌟 What's Running:

**Backend**: http://localhost:8000  
**Frontend**: http://localhost:3000

---

## 🎯 Open Your Application:

**Click here**: http://localhost:3000

---

## 🗺️ New Features (No Google API Key Needed!):

### ✅ FREE Leaflet Map
- **Replaced Google Maps** with FREE Leaflet
- **NO credit card** required
- **NO API key** needed
- **FREE satellite imagery** from Esri

### 🎨 What You'll See:

1. **Satellite Map** - Free high-quality imagery
2. **Scan Button** - Blue button on top-left
3. **Deforestation Zones** - Color-coded polygons:
   - 🔴 Red = Critical (90%+ confidence)
   - 🟠 Orange = High (80-89%)
   - 🟡 Yellow = Medium (70-79%)

---

## 📍 How to Use:

### Step 1: Open Browser
Go to: **http://localhost:3000**

### Step 2: Click "Scan for Deforestation"
- Blue button on top-left corner
- Sidebar will slide in from left

### Step 3: Choose Location
**Quick Presets:**
- Amazon Rainforest, Brazil
- Congo Basin, DRC
- Borneo, Indonesia
- Papua New Guinea
- Pune, India (default)

**Or enter custom coordinates:**
- Latitude: e.g., -3.4653
- Longitude: e.g., -62.2159

### Step 4: Configure Scan
- **Radius**: 1-50 km (default: 5 km)
- **Date Range**: From → To
- **Method**: 
  - Hansen (Forest Change dataset)
  - NDVI (Vegetation index)

### Step 5: Start Scan
Click the **"Start Scan"** button!

### Step 6: View Results
- Map centers on location
- Blue circle shows scan area
- Colored polygons show deforestation
- **Click any polygon** for details:
  - Area (hectares)
  - Confidence (%)
  - Date detected
  - Incident ID

---

## 🔧 Commands:

### Start Both Services:
```powershell
# Terminal 1 - Backend
cd C:\Users\harsh\OneDrive\Desktop\bq\backend
python -B main.py

# Terminal 2 - Frontend
cd C:\Users\harsh\OneDrive\Desktop\bq\frontend
npm run dev
```

### Stop Services:
Press `Ctrl + C` in each terminal

---

## 🎉 Key Improvements:

### ✅ NO Google Maps
- Removed Google Maps API requirement
- No credit card needed
- No billing account needed

### ✅ FREE Leaflet
- Open-source mapping library
- Used by NASA, GitHub, Facebook
- Professional quality
- Zero cost

### ✅ FREE Satellite Imagery
- Esri World Imagery (free)
- CARTO basemap (free)
- No usage limits

### ✅ Sidebar Design
- Fixed-height panel
- Slides in from left
- No scrolling issues
- Clean, modern UI

### ✅ Real-time Data
- Google Earth Engine integration
- Live satellite data
- BigQuery storage
- DSA algorithms for detection

---

## 📊 Check Status:

### Backend Health:
http://localhost:8000/health

Should show:
```json
{
  "status": "healthy",
  "gee_connected": true,
  "bigquery_connected": true
}
```

### Frontend:
http://localhost:3000

Should show:
- Beautiful map with satellite imagery
- "Scan for Deforestation" button
- Stats cards at top
- Alerts panel on right

---

## 🐛 Troubleshooting:

### Frontend Not Loading?
```powershell
cd C:\Users\harsh\OneDrive\Desktop\bq\frontend
npm run dev
```
(Use `npm run dev`, NOT `npm start`)

### Backend Not Running?
```powershell
cd C:\Users\harsh\OneDrive\Desktop\bq\backend
python -B main.py
```

### Port Already in Use?
The frontend will automatically try port 3001 if 3000 is busy.
Check: http://localhost:3001

---

## 🎊 You're All Set!

**Your deforestation tracker is now:**
- ✅ Running with FREE map tiles
- ✅ No API key needed
- ✅ Beautiful sidebar interface
- ✅ Real-time satellite data
- ✅ Production-ready!

**Enjoy tracking deforestation! 🌍🌲**



