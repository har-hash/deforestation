# 🛰️ Deforestation Scanning Guide

## How to Scan for Deforestation on the Frontend

Your deforestation tracker now has a powerful **Scan Control Panel** that allows you to scan any location in the world for forest loss using real satellite data!

## 🎯 Features

### 1. **Interactive Scan Panel**
- Located in the top-left corner of the map
- Click to expand/collapse the control panel
- Clean, intuitive interface with all scan parameters

### 2. **Location Selection**

#### **Quick Presets**
Choose from pre-configured high-risk deforestation areas:
- 🌳 **Amazon Rainforest, Brazil** - The world's largest rainforest
- 🌍 **Congo Basin, DRC** - Africa's primary tropical forest
- 🌴 **Borneo, Indonesia** - Critical orangutan habitat
- ⛰️ **Western Ghats, India** - UNESCO World Heritage site
- 🏙️ **Pune, India** - Local monitoring

#### **Custom Location**
- Enter any location name
- Manually set latitude and longitude
- Coordinates update automatically when selecting presets

### 3. **Scan Parameters**

#### **Radius Control**
- Adjustable from **1 km to 50 km**
- Interactive slider with real-time updates
- Visual circle overlay shows scan area on map

#### **Date Range**
- **Start Date**: When to begin analysis
- **End Date**: When to end analysis (defaults to today)
- Analyze changes over months or years

#### **Detection Method**
Two powerful algorithms to choose from:

**Hansen Forest Change Dataset** 🌲
- Uses Google's Hansen Global Forest Change data
- Annual forest cover loss from 2000-present
- Best for: Long-term trends, official reports
- High accuracy, peer-reviewed

**NDVI (Vegetation Index)** 🌿
- Normalized Difference Vegetation Index
- Real-time vegetation health analysis
- Best for: Recent changes, seasonal monitoring
- Detects subtle vegetation changes

## 📖 Step-by-Step Usage

### Basic Scan (Quick Start)

1. **Open the Scan Panel**
   ```
   Click "Scan for Deforestation" in the top-left
   ```

2. **Select a Preset Location**
   ```
   Click any preset (e.g., "Amazon Rainforest, Brazil")
   ```

3. **Start the Scan**
   ```
   Click the blue "Start Scan" button
   ```

4. **View Results**
   ```
   Deforestation areas appear as colored polygons:
   - 🔴 Red = Critical (90%+ confidence)
   - 🟠 Orange = High (80-89% confidence)
   - 🟡 Yellow = Medium (70-79% confidence)
   ```

### Advanced Scan (Custom Parameters)

1. **Open Scan Panel**
2. **Set Custom Location**
   ```
   - Enter location name OR
   - Set exact latitude/longitude
   ```

3. **Adjust Scan Radius**
   ```
   - Drag slider to desired radius
   - Larger radius = wider area, longer scan time
   - Smaller radius = focused analysis, faster results
   ```

4. **Set Date Range**
   ```
   Start Date: 2022-01-01
   End Date: 2024-12-31
   (Analyzes 3 years of data)
   ```

5. **Choose Detection Method**
   ```
   - Hansen for historical trends
   - NDVI for recent/real-time changes
   ```

6. **Start Scan**
   ```
   Click "Start Scan"
   Watch the progress indicators
   ```

## 🎨 Understanding the Results

### Color-Coded Polygons

| Color | Confidence | Meaning |
|-------|-----------|---------|
| 🔴 Red | 90-100% | Critical deforestation - immediate action needed |
| 🟠 Orange-Red | 80-89% | High confidence - likely deforestation |
| 🟡 Orange | 70-79% | Medium confidence - significant change detected |
| 🟡 Yellow | <70% | Low-medium confidence - potential change |

### Polygon Information
Click any polygon to see:
- **Area**: Size in hectares
- **Confidence**: Detection confidence percentage
- **Detected**: When the change was detected
- **ID**: Unique identifier for the incident

## 🔍 What Happens During a Scan?

### Behind the Scenes

1. **Satellite Data Retrieval**
   ```
   - Connects to Google Earth Engine
   - Downloads Landsat/MODIS imagery
   - Covers your selected area and timeframe
   ```

2. **Change Detection Analysis**
   ```
   - Compares before/after images
   - Analyzes vegetation indices (NDVI, EVI)
   - Detects forest cover loss
   ```

3. **Algorithm Processing**
   ```
   Hansen Method:
   - Uses pre-computed forest change data
   - Fast, reliable, global coverage
   
   NDVI Method:
   - Calculates vegetation health changes
   - Detects recent deforestation
   - More sensitive to subtle changes
   ```

4. **Results Display**
   ```
   - Generates GeoJSON polygons
   - Color-codes by confidence
   - Displays on interactive map
   - Stores in BigQuery for history
   ```

## 💡 Tips & Best Practices

### For Best Results

1. **Start with Presets**
   - Use preset locations to learn the interface
   - Compare different detection methods
   - Understand typical patterns

2. **Optimize Scan Radius**
   ```
   Small Areas (1-5 km):  ✅ Fast, detailed analysis
   Medium Areas (5-20 km): ⚡ Good balance
   Large Areas (20-50 km): 🐌 Slower but comprehensive
   ```

3. **Choose Appropriate Date Ranges**
   ```
   Recent Changes:    Last 30-90 days
   Seasonal Analysis: Last 12 months
   Long-term Trends:  2+ years
   ```

4. **Method Selection**
   ```
   Use Hansen for:
   - Historical analysis
   - Annual reports
   - Official documentation
   
   Use NDVI for:
   - Real-time monitoring
   - Recent incidents (<6 months)
   - Vegetation health tracking
   ```

### Common Scenarios

**Scenario 1: Monitor Protected Area**
```
Location: Western Ghats, India
Radius: 10 km
Date Range: Last 1 year
Method: Hansen
Purpose: Annual conservation report
```

**Scenario 2: Emergency Response**
```
Location: Custom coordinates
Radius: 5 km
Date Range: Last 30 days
Method: NDVI
Purpose: Verify illegal logging reports
```

**Scenario 3: Research Study**
```
Location: Amazon Rainforest
Radius: 25 km
Date Range: 2020-2024
Method: Both (compare)
Purpose: Climate impact research
```

## 🚨 Interpreting Alerts

### What to Do When Deforestation is Detected

1. **High Confidence (>80%)**
   - Immediate investigation recommended
   - Contact local authorities
   - Document findings
   - Export data for reports

2. **Medium Confidence (70-80%)**
   - Verify with additional scans
   - Check historical data
   - Monitor for progression

3. **Low Confidence (<70%)**
   - May be seasonal changes
   - Could be natural events
   - Requires verification

## 📊 Scan Performance

### Expected Scan Times

| Radius | Time | Data Points |
|--------|------|-------------|
| 1-5 km | 5-15 sec | ~100-500 |
| 5-10 km | 15-30 sec | ~500-1000 |
| 10-20 km | 30-60 sec | ~1000-5000 |
| 20-50 km | 1-3 min | ~5000-20000 |

*Times vary based on:*
- Network speed
- Backend server load
- Data complexity
- Selected date range

## 🛠️ Troubleshooting

### Common Issues

**"No deforestation detected"**
- ✅ Good news! Area is stable
- Try expanding radius
- Check different time periods
- Verify location coordinates

**"Scan taking too long"**
- Reduce scan radius
- Shorten date range
- Check internet connection
- Backend may be processing

**"Error loading data"**
- Verify backend is running (port 8000)
- Check API URL in .env.local
- Ensure Google Earth Engine is authenticated
- Try refreshing the page

## 🎓 Learning Resources

### Understanding the Science

**NDVI (Normalized Difference Vegetation Index)**
```
Formula: NDVI = (NIR - Red) / (NIR + Red)

Where:
- NIR = Near-Infrared reflectance
- Red = Red band reflectance

Values:
- 0.8-1.0: Dense, healthy forest
- 0.6-0.8: Moderate vegetation
- 0.2-0.6: Sparse vegetation
- <0.2: No vegetation (deforested)
```

**Hansen Global Forest Change**
- Annual updates
- 30-meter resolution
- Global coverage
- Peer-reviewed methodology
- Based on Landsat imagery

### Data Sources

1. **Google Earth Engine**
   - Landsat 8/9 (optical)
   - MODIS (daily monitoring)
   - Sentinel-2 (high resolution)

2. **Hansen Dataset**
   - University of Maryland
   - Global Forest Watch
   - Annual updates since 2000

## 📱 Mobile Usage

The scan interface is fully responsive:
- Touch-friendly controls
- Optimized for smaller screens
- Swipe gestures for map interaction
- Collapsible panel to maximize map view

## 🔐 Privacy & Data

- **No location tracking**: Your searches are not stored
- **Anonymous scans**: No user identification required
- **Public data only**: Uses publicly available satellite imagery
- **Secure connection**: All API calls use HTTPS

## 🌍 Making an Impact

### Share Your Findings

1. **Screenshot results** (built-in map tools)
2. **Export GeoJSON** data
3. **Share with authorities**
4. **Report to conservation groups**
5. **Use in research papers**

### Organizations to Contact

- **Global Forest Watch**: forestwatcher@wri.org
- **WWF**: deforestation@wwf.org  
- **Rainforest Foundation**: info@rainforestfoundation.org
- **Local forest departments**

---

## 🎉 You're Ready!

You now have everything you need to scan for and detect illegal deforestation using real satellite data. Start with a preset location, explore the features, and help protect our planet's forests! 🌳🌍

**Questions?** Check the backend API docs at http://localhost:8000/docs



