# 🚀 Complete Setup Guide

Step-by-step guide to get the Illegal Deforestation Tracker running locally and in production.

## 📋 Prerequisites Checklist

- [ ] Python 3.9 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] Git installed
- [ ] Google Cloud Platform account
- [ ] Google Earth Engine account
- [ ] Credit card for GCP (free tier available)

## 🔐 Part 1: Google Cloud Platform Setup

### Step 1: Create GCP Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a Project" → "New Project"
3. Enter project name: `deforestation-tracker`
4. Click "Create"
5. Wait for project creation (30 seconds)

### Step 2: Enable Billing

1. Go to "Billing" in the left menu
2. Link a billing account (free tier: $300 credit)
3. Confirm billing is enabled

### Step 3: Enable Required APIs

```bash
# Set your project
gcloud config set project deforestation-tracker

# Enable APIs
gcloud services enable earthengine.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable storage-component.googleapis.com
gcloud services enable maps-backend.googleapis.com
```

Or enable via Console:
1. Go to "APIs & Services" → "Library"
2. Search and enable:
   - Earth Engine API
   - BigQuery API
   - Cloud Storage API
   - Maps JavaScript API

### Step 4: Create Service Account

```bash
# Create service account
gcloud iam service-accounts create gee-service-account \
    --display-name="Google Earth Engine Service Account" \
    --description="Service account for deforestation tracker"

# Get your project number
export PROJECT_NUMBER=$(gcloud projects describe deforestation-tracker --format="value(projectNumber)")

# Grant Earth Engine permissions
gcloud projects add-iam-policy-binding deforestation-tracker \
    --member="serviceAccount:gee-service-account@deforestation-tracker.iam.gserviceaccount.com" \
    --role="roles/earthengine.admin"

# Grant BigQuery permissions
gcloud projects add-iam-policy-binding deforestation-tracker \
    --member="serviceAccount:gee-service-account@deforestation-tracker.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"

# Grant Storage permissions
gcloud projects add-iam-policy-binding deforestation-tracker \
    --member="serviceAccount:gee-service-account@deforestation-tracker.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Create and download key
gcloud iam service-accounts keys create gee-private-key.json \
    --iam-account=gee-service-account@deforestation-tracker.iam.gserviceaccount.com

# Move key to backend directory
mv gee-private-key.json ./backend/
```

### Step 5: Create Google Maps API Key

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API Key"
3. Copy the API key
4. Click "Edit API key" to restrict it:
   - **Application restrictions**: HTTP referrers
   - **Website restrictions**: 
     - `http://localhost:3000/*`
     - Your production domain
   - **API restrictions**: Restrict key
     - Maps JavaScript API

## 🌍 Part 2: Google Earth Engine Setup

### Step 1: Sign Up for Earth Engine

1. Go to [earthengine.google.com](https://earthengine.google.com)
2. Click "Sign Up"
3. Register with your Google account
4. Wait for approval (usually instant for development)

### Step 2: Authenticate

```bash
# Install Earth Engine CLI
pip install earthengine-api

# Authenticate
earthengine authenticate

# Follow browser prompts to authenticate
# Copy the authorization code back to terminal
```

### Step 3: Test Connection

```bash
# Test Python API
python -c "import ee; ee.Initialize(); print('Earth Engine is ready!')"
```

If successful, you'll see: `Earth Engine is ready!`

## 💻 Part 3: Backend Setup

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd deforestation-tracker
```

### Step 2: Setup Python Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create `backend/.env`:

```env
# Google Cloud Project
GCP_PROJECT_ID=deforestation-tracker

# Google Earth Engine
GEE_SERVICE_ACCOUNT=gee-service-account@deforestation-tracker.iam.gserviceaccount.com
GEE_PRIVATE_KEY_PATH=./gee-private-key.json

# BigQuery
BIGQUERY_DATASET=forest_monitoring
BIGQUERY_TABLE=forest_loss_zones

# Google Cloud Storage
GCS_BUCKET=deforestation-exports

# Google Maps (for backend reference)
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Application Settings
DEBUG=True
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# Detection Parameters
NDVI_THRESHOLD=-0.2
CONFIDENCE_THRESHOLD=0.7
MIN_CLUSTER_SIZE=5
REFRESH_INTERVAL=24
```

### Step 4: Verify Service Account Key

```bash
# Ensure the key file exists
ls gee-private-key.json

# Should show the file - if not, re-download from GCP
```

### Step 5: Test Backend

```bash
# Start the server
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Verify Backend

Open browser to:
- API root: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Expected health response:
```json
{
  "status": "healthy",
  "gee_connected": true,
  "bigquery_connected": true,
  "timestamp": "2024-..."
}
```

## 🎨 Part 4: Frontend Setup

### Step 1: Install Dependencies

```bash
# Open new terminal
cd frontend

# Install packages
npm install
```

### Step 2: Configure Environment

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 3: Start Frontend

```bash
npm run dev
```

You should see:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

### Step 4: Open Application

Go to http://localhost:3000

You should see:
- ✅ Satellite map loading
- ✅ Stats cards with data
- ✅ Alert panel
- ✅ Timeline slider

## 🧪 Part 5: Testing the System

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

### Test 2: Get Statistics

```bash
curl http://localhost:8000/api/stats?days=30
```

### Test 3: Forest Loss Detection

```bash
curl "http://localhost:8000/api/forest-loss?method=hansen&use_bigquery=false"
```

### Test 4: Frontend Components

1. Open http://localhost:3000
2. Check browser console (F12) for errors
3. Click on map - should show satellite view
4. Wait for stats to load
5. Check alerts panel updates

## 🚀 Part 6: First Data Run

### Run Initial Detection

```bash
# From backend directory
python -c "
from gee_pipeline import GEEPipeline
from bigquery_handler import BigQueryHandler

# Initialize
gee = GEEPipeline()
bq = BigQueryHandler()

# Run detection
print('Running forest loss detection...')
result = gee.detect_forest_loss(
    start_date='2020-01-01',
    end_date='2023-12-31',
    use_hansen=True
)

print(f'Found {len(result[\"geojson\"][\"features\"])} deforestation areas')

# Save to BigQuery
print('Saving to BigQuery...')
metadata = {'region': 'Pune, India', 'method': 'hansen'}
bq.insert_forest_loss_data(result['geojson'], metadata)

print('Complete! Check http://localhost:3000')
"
```

## 🐛 Troubleshooting

### Problem: GEE Authentication Failed

**Solution:**
```bash
earthengine authenticate --quiet
python -c "import ee; ee.Initialize(); print('OK')"
```

### Problem: BigQuery Permission Denied

**Solution:**
```bash
# Verify service account email
gcloud iam service-accounts list

# Re-grant permissions
gcloud projects add-iam-policy-binding deforestation-tracker \
    --member="serviceAccount:gee-service-account@deforestation-tracker.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"
```

### Problem: Maps Not Loading

**Solution:**
1. Check browser console for API key error
2. Verify API key in `.env.local`
3. Check Maps JavaScript API is enabled
4. Verify referrer restrictions allow localhost

### Problem: CORS Errors

**Solution:**
Update `backend/config.py`:
```python
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Problem: Module Not Found Errors

**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules
npm install
```

## 📊 Verify Data Pipeline

### 1. Check BigQuery Table

```bash
# List tables
bq ls forest_monitoring

# Query data
bq query --use_legacy_sql=false \
'SELECT COUNT(*) as count FROM `deforestation-tracker.forest_monitoring.forest_loss_zones`'
```

### 2. Check Frontend Data

Open http://localhost:3000 and verify:
- Stats cards show numbers > 0
- Map shows polygon overlays
- Alerts panel populated

## 🎉 Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] GEE connection healthy
- [ ] BigQuery connection healthy
- [ ] Maps loading with satellite view
- [ ] Stats cards showing data
- [ ] Alerts panel populated
- [ ] Polygons visible on map
- [ ] No console errors

## 📚 Next Steps

1. **Customize Region**
   - Edit `backend/config.py` → `DEFAULT_REGION_COORDS`
   
2. **Add More Data**
   - Run detection for different time periods
   - Process multiple regions
   
3. **Deploy to Production**
   - Follow deployment guides
   - Update environment variables
   - Set up HTTPS

4. **Monitor Performance**
   - Check GCP quotas
   - Monitor API usage
   - Review logs

## 💡 Tips

- Keep backend running while developing
- Use separate terminals for backend and frontend
- Check logs in `backend/logs/` for debugging
- Browser DevTools Network tab shows API calls
- BigQuery free tier: 1 TB queries/month
- Earth Engine: 2000 requests/day free

## 📧 Getting Help

If you encounter issues:

1. Check error messages carefully
2. Review logs in backend
3. Check browser console
4. Verify all environment variables
5. Ensure services are running
6. Check GCP billing and quotas

## 🔗 Useful Links

- [Google Earth Engine Docs](https://developers.google.com/earth-engine)
- [BigQuery Docs](https://cloud.google.com/bigquery/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Next.js Docs](https://nextjs.org/docs)
- [Google Maps JS API](https://developers.google.com/maps/documentation/javascript)

---

**Congratulations! Your deforestation tracker is now running! 🌲**



