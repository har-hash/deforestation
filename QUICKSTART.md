# ⚡ Quick Start Guide

Get the Illegal Deforestation Tracker running in 10 minutes!

## 🎯 Prerequisites

Before starting, ensure you have:
- ✅ Python 3.9+ installed
- ✅ Node.js 18+ installed  
- ✅ Google Cloud account (free tier available)
- ✅ Google Earth Engine access ([Sign up](https://earthengine.google.com))

## 📦 Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd deforestation-tracker
```

## 🔑 Step 2: Get API Keys (5 min)

### Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project: `deforestation-tracker`
3. Enable **Maps JavaScript API**
4. Create credentials → API Key
5. Copy the key

### Google Earth Engine
```bash
pip install earthengine-api
earthengine authenticate
```
Follow browser prompts to authenticate.

## 🖥️ Step 3: Setup Backend (2 min)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (choose your OS)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "GCP_PROJECT_ID=deforestation-tracker
BIGQUERY_DATASET=forest_monitoring
BIGQUERY_TABLE=forest_loss_zones
DEBUG=True
CORS_ORIGINS=[\"http://localhost:3000\"]" > .env

# Start backend
python main.py
```

Backend now running at: **http://localhost:8000** ✅

Open http://localhost:8000/docs to see API documentation.

## 🎨 Step 4: Setup Frontend (2 min)

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Configure environment
echo "NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-key-here
NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# IMPORTANT: Replace 'your-key-here' with your actual Google Maps API key!

# Start frontend
npm run dev
```

Frontend now running at: **http://localhost:3000** ✅

## 🧪 Step 5: Test It! (1 min)

### Test Backend
```bash
# Health check
curl http://localhost:8000/health

# Should return: {"status":"healthy","gee_connected":true,...}
```

### Test Frontend
1. Open browser to http://localhost:3000
2. You should see:
   - ✅ Map with satellite view
   - ✅ Stats cards (may show 0s initially)
   - ✅ Alert panel
   - ✅ Timeline slider

## 🚀 Step 6: Run First Detection

```bash
# In backend terminal
python -c "
from gee_pipeline import GEEPipeline

gee = GEEPipeline()
print('Running detection...')

result = gee.detect_forest_loss(
    start_date='2020-01-01',
    end_date='2023-12-31',
    use_hansen=True
)

print(f'✅ Detected {len(result[\"geojson\"][\"features\"])} deforestation areas!')
"
```

This may take 1-2 minutes on first run.

## 🎉 Success!

You should now see:
- **Green dots** on the map (deforestation areas)
- **Non-zero numbers** in stats cards
- **Alerts** in the sidebar

## 🔍 What Just Happened?

1. **Backend** connected to Google Earth Engine
2. **Satellite data** was analyzed (Hansen dataset)
3. **Deforestation** was detected using DSA algorithms
4. **Results** were displayed on the map

## 📊 Explore Features

### View Different Time Periods
Use the timeline slider at the bottom of the map.

### Check Analytics
Visit http://localhost:3000/dashboard for charts and graphs.

### API Endpoints
Try these in your browser or curl:

```bash
# Get statistics
curl http://localhost:8000/api/stats?days=30

# Get alerts
curl http://localhost:8000/api/alerts?limit=10

# Get forest loss data
curl "http://localhost:8000/api/forest-loss?method=hansen"
```

## 🐛 Common Issues

### Maps Not Loading
**Problem**: Blank map area
**Solution**: 
```bash
# Check your API key in frontend/.env.local
cat frontend/.env.local
# Make sure it starts with NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=
```

### Backend Connection Error
**Problem**: "GEE not authenticated"
**Solution**:
```bash
earthengine authenticate
```

### CORS Error
**Problem**: Frontend can't connect to backend
**Solution**: Ensure `CORS_ORIGINS` in backend/.env includes `http://localhost:3000`

### No Data Showing
**Problem**: Stats show 0
**Solution**: Run the detection script in Step 6 to generate data

## 🎓 Next Steps

### Customize Your Region
Edit `backend/config.py`:
```python
DEFAULT_REGION_COORDS: List[List[float]] = [
    [lon1, lat1],
    [lon2, lat2],
    [lon3, lat3],
    [lon4, lat4],
    [lon1, lat1]  # Close the polygon
]
```

### Enable BigQuery (Optional)
For persistent storage:
1. Go to GCP Console
2. Enable BigQuery API
3. Data will automatically save to BigQuery

### Deploy to Production
When ready, follow: **DEPLOYMENT.md**

## 📚 Documentation

- **Full Setup**: `SETUP_GUIDE.md` - Complete detailed setup
- **API Reference**: http://localhost:8000/docs - Interactive API docs
- **Deployment**: `DEPLOYMENT.md` - Production deployment
- **Architecture**: `README.md` - System overview

## 💡 Pro Tips

1. **Keep backend running** while developing frontend
2. **Check browser console** (F12) for frontend errors
3. **Check terminal** for backend errors
4. **Use /docs endpoint** to test API interactively
5. **Start with small regions** for faster processing

## ⏱️ Time Breakdown

- API Keys: 5 minutes
- Backend Setup: 2 minutes
- Frontend Setup: 2 minutes
- First Detection: 1-2 minutes
- **Total: ~10 minutes**

## ✅ Verification Checklist

After completing the quick start, verify:

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:3000
- [ ] Health check returns `"status":"healthy"`
- [ ] Map displays satellite imagery
- [ ] Stats cards show numbers (may be 0 initially)
- [ ] Alert panel is visible
- [ ] No errors in browser console
- [ ] API docs accessible at /docs

## 🆘 Need Help?

If you encounter issues:

1. **Check Prerequisites**: Ensure Python 3.9+, Node 18+ installed
2. **Verify API Keys**: Make sure they're correctly set in .env files
3. **Review Logs**: Check terminal output for errors
4. **Read Full Guide**: See `SETUP_GUIDE.md` for detailed instructions
5. **Test Components**: Use health check and API docs to isolate issues

## 🎊 Congratulations!

You now have a working deforestation tracker! 🌲

**What you've built:**
- ✅ Real-time satellite monitoring system
- ✅ Advanced change detection algorithms
- ✅ Interactive map visualization
- ✅ Analytics dashboard
- ✅ REST API for data access

**Next**: Customize regions, add features, or deploy to production!

---

**Remember**: This uses real satellite data, so detections are actual forest loss areas! 🌍



