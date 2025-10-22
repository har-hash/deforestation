# 🔐 Complete Authentication Setup Guide

## Current Status
✅ **Backend server is running** at http://localhost:8000  
✅ **Health endpoint working** - shows "degraded" status (expected without full auth)  
⚠️ **Need to complete authentication for full functionality**

## Step 1: Earth Engine Authentication (REQUIRED)

### 1.1 Sign up for Earth Engine
1. **Visit**: https://earthengine.google.com/signup/
2. **Sign in** with your Google account (harsh.15121102@gmail.com)
3. **Fill out the form**:
   - Select "Academic" or "Commercial" use
   - Describe your project: "Real-time deforestation tracking using satellite data"
4. **Submit and wait** for approval (usually instant)

### 1.2 Test Earth Engine
After signup approval, run:
```bash
cd backend
python -c "import ee; ee.Initialize(); print('GEE Connected!')"
```

## Step 2: Google Cloud Authentication (REQUIRED)

### 2.1 Install Google Cloud SDK
Download from: https://cloud.google.com/sdk/docs/install

### 2.2 Authenticate
```bash
gcloud auth application-default login
```

### 2.3 Enable APIs
Visit: https://console.cloud.google.com/apis/library

Enable these APIs:
- **Earth Engine API**
- **BigQuery API** 
- **Cloud Storage API**

## Step 3: Verify Everything Works

### 3.1 Test Health Endpoint
```bash
curl http://localhost:8000/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "gee_connected": true,
  "bigquery_connected": true,
  "timestamp": "2025-10-20T08:53:39.550099"
}
```

### 3.2 Test API Endpoints
```bash
# Test forest loss detection
curl "http://localhost:8000/api/forest-loss/detect?lat=40.7128&lon=-74.0060&radius=1000"

# Test alerts
curl "http://localhost:8000/api/alerts"

# Test statistics
curl "http://localhost:8000/api/stats/summary"
```

## Current Server Status

The server is **RUNNING** and ready! You can:

1. **Access the API** at http://localhost:8000
2. **View health status** at http://localhost:8000/health
3. **Test endpoints** (they'll return mock data until auth is complete)

## Next Steps

1. **Complete Earth Engine signup** (5 minutes)
2. **Set up Google Cloud credentials** (10 minutes)  
3. **Test all endpoints** (2 minutes)
4. **Start building the frontend** (30+ minutes)

## Troubleshooting

### If Earth Engine fails:
- Make sure you're signed up at https://earthengine.google.com/signup/
- Wait a few minutes after signup for activation
- Try `earthengine authenticate --force`

### If BigQuery fails:
- Ensure billing is enabled on your GCP project
- Check you have BigQuery Admin role
- Verify project ID in `.env` matches your GCP project

### If server won't start:
- Kill existing processes: `taskkill /F /IM python.exe`
- Check port 8000 is free: `netstat -ano | findstr :8000`
- Restart: `cd backend && python -B main.py`

## Files Created
- `backend/simple_auth.py` - Mock credentials for development
- `backend/auth_setup.py` - OAuth authentication script
- `AUTHENTICATION_SETUP.md` - This guide

The server is **READY TO USE** - just complete the authentication steps above!


