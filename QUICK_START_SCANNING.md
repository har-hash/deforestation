# 🚀 Quick Start: Scanning for Deforestation

## 3-Minute Tutorial

### Step 1: Start Your Application

**Backend:**
```bash
cd backend
$env:GOOGLE_APPLICATION_CREDENTIALS="$env:USERPROFILE\.config\gcloud\application_default_credentials.json"
$env:GOOGLE_CLOUD_PROJECT="deforestation-tracker-475003"
python -B main.py
```
✅ Backend running at http://localhost:8000

**Frontend:**
```bash
cd frontend
npm run dev
```
✅ Frontend running at http://localhost:3000

### Step 2: Open the Application

1. Open your browser to **http://localhost:3000**
2. You'll see the main dashboard with an interactive map

### Step 3: Start Your First Scan

#### Option A: Quick Preset Scan (30 seconds)

1. **Click** the "Scan for Deforestation" button (top-left of map)
2. **Select** a preset location:
   - Amazon Rainforest, Brazil ← **Try this first!**
3. **Click** the blue "Start Scan" button
4. **Wait** 15-30 seconds while the system analyzes satellite data
5. **View** results! Red/orange polygons show deforestation areas

#### Option B: Custom Location Scan (2 minutes)

1. **Click** "Scan for Deforestation"
2. **Enter coordinates** or adjust the preset:
   ```
   Example: Monitor an area near you
   Latitude: 18.5204
   Longitude: 73.8567
   ```
3. **Set radius**: Drag slider to 10 km
4. **Set dates**: 
   - From: 2023-01-01
   - To: Today
5. **Choose method**: Hansen (recommended for first scan)
6. **Click** "Start Scan"

### Step 4: Interpret Results

**Polygon Colors:**
- 🔴 **Red** = Critical deforestation (>90% confidence)
- 🟠 **Orange** = High confidence (80-90%)
- 🟡 **Yellow** = Medium confidence (70-80%)

**Click any polygon** to see detailed information:
- Area in hectares
- Detection confidence
- Date detected
- Unique ID

### Step 5: Try Different Locations

**High-Activity Areas to Scan:**

1. **Amazon Rainforest**
   ```
   Preset: Amazon Rainforest, Brazil
   Radius: 25 km
   Best Method: Hansen
   ```

2. **Congo Basin**
   ```
   Preset: Congo Basin, DRC
   Radius: 20 km
   Best Method: Hansen
   ```

3. **Borneo**
   ```
   Preset: Borneo, Indonesia  
   Radius: 15 km
   Best Method: Both (compare results)
   ```

## 🎯 What You Should See

### During Scan:
```
✨ Animation overlay appears
🔄 "Analyzing Satellite Data" message
📊 Progress indicators:
   - Fetching satellite imagery...
   - Running change detection algorithms...
   - Analyzing forest cover patterns...
```

### After Scan:
```
✅ "Scan Complete!" message
🗺️ Map centers on scanned area
🔵 Blue circle shows scan radius (briefly)
🔴 Red/orange/yellow polygons show deforestation
📍 Click polygons for details
```

## 🎓 Understanding the Two Methods

### Hansen Forest Change
```
When to use: Historical analysis, official reports
Speed: Fast (pre-computed data)
Coverage: Global, annual updates
Time Range: 2000-present
```

### NDVI Vegetation Index
```
When to use: Recent changes, real-time monitoring  
Speed: Moderate (live calculation)
Coverage: Global, near real-time
Time Range: Any date range
```

## 💡 Pro Tips

1. **Start Small**: Use 5-10 km radius for first scans
2. **Compare Methods**: Run same location with both Hansen and NDVI
3. **Check Time Ranges**: Try "Last 6 months" vs "Last 2 years"
4. **Explore Presets**: Each preset shows different deforestation patterns
5. **Click Everything**: Click polygons, stats cards, timeline slider

## 📊 Reading the Dashboard

### Top Stats Cards:
- **Total Forest Loss**: Cumulative area lost (hectares)
- **Detected Incidents**: Number of deforestation events
- **Average Confidence**: Mean detection certainty
- **Daily Loss Rate**: Hectares lost per day

### Alert Panel (Right Side):
- Real-time deforestation alerts
- Severity levels (Critical/High/Medium)
- Recent incidents
- Quick navigation to alert locations

### Timeline Slider (Bottom):
- Adjust time range: 7-365 days
- Dynamic data updates
- Historical comparison

## 🔧 Troubleshooting Quick Fixes

**Map not loading?**
```
1. Check Google Maps API key in frontend/.env.local
2. Verify NEXT_PUBLIC_GOOGLE_MAPS_API_KEY is set
3. Refresh the page
```

**Scan button doesn't work?**
```
1. Confirm backend is running: http://localhost:8000/health
2. Check console for errors (F12)
3. Verify coordinates are valid
```

**No results showing?**
```
✅ This might be good news! 
   The area may have no deforestation.
   
Try:
- Expand scan radius
- Change date range
- Try a different preset location
```

**Scan taking forever?**
```
- Large radius (>30km) takes 1-3 minutes
- Reduce radius to 10-15 km for faster results
- Check backend logs for processing status
```

## 🎉 You're Scanning!

That's it! You're now using real satellite data to detect deforestation anywhere in the world.

### Next Steps:

1. ✅ **Scan multiple locations** - Compare deforestation rates
2. ✅ **Experiment with methods** - See Hansen vs NDVI differences
3. ✅ **Adjust parameters** - Find optimal settings for your use case
4. ✅ **Share findings** - Export data, take screenshots, report issues

### Full Documentation:
- **Scanning Guide**: `frontend/SCANNING_GUIDE.md`
- **API Documentation**: http://localhost:8000/docs
- **Project Status**: `STATUS.md`

---

**Happy scanning! 🌍🛰️🌳**

*You're making a difference by monitoring and protecting our planet's forests!*



