# 🌲 Illegal Deforestation Tracker

> Real-time satellite-based deforestation detection using Google Earth Engine, BigQuery, DSA algorithms, and Google Maps API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)

## 🚀 Overview

A production-ready web application that tracks and visualizes real-time illegal deforestation using:

- **Google Earth Engine (GEE)** for satellite data processing
- **Google BigQuery** for cloud storage and querying
- **DSA algorithms** (Union-Find, KD-Tree) for spatial change detection
- **Google Maps API** for live visualization with satellite imagery
- **FastAPI** backend with async performance
- **Next.js + React** frontend with beautiful UI

## ✨ Features

### Backend
- ✅ Real-time satellite data processing from Google Earth Engine
- ✅ Hansen Global Forest Change dataset integration
- ✅ NDVI-based temporal change detection
- ✅ DSA algorithms for clustering and anomaly detection
- ✅ Automated data export to BigQuery
- ✅ RESTful API with FastAPI
- ✅ Production-ready with CORS, logging, and error handling

### Frontend
- ✅ Google Maps with satellite layer
- ✅ Real-time deforestation polygon overlays
- ✅ Color-coded confidence visualization
- ✅ Interactive timeline slider
- ✅ Live alerts panel
- ✅ Statistics dashboard with charts
- ✅ Modern UI with TailwindCSS and Framer Motion

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- Google Cloud Platform account
- Google Earth Engine account
- Google Maps API key

## 🔧 Setup Instructions

### 1. Google Cloud Platform Setup

#### Create a GCP Project
```bash
gcloud projects create deforestation-tracker
gcloud config set project deforestation-tracker
```

#### Enable Required APIs
```bash
gcloud services enable earthengine.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
```

#### Create Service Account
```bash
gcloud iam service-accounts create gee-service-account \
    --display-name="GEE Service Account"

gcloud projects add-iam-policy-binding deforestation-tracker \
    --member="serviceAccount:gee-service-account@deforestation-tracker.iam.gserviceaccount.com" \
    --role="roles/earthengine.admin"

gcloud projects add-iam-policy-binding deforestation-tracker \
    --member="serviceAccount:gee-service-account@deforestation-tracker.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"

gcloud iam service-accounts keys create gee-private-key.json \
    --iam-account=gee-service-account@deforestation-tracker.iam.gserviceaccount.com
```

### 2. Google Earth Engine Authentication

#### Option A: Service Account (Production)
- Download the private key JSON file from GCP
- Place it in the backend directory
- Set the path in `.env` file

#### Option B: User Authentication (Development)
```bash
earthengine authenticate
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

#### Backend `.env` Configuration
```env
GCP_PROJECT_ID=deforestation-tracker
GEE_SERVICE_ACCOUNT=gee-service-account@deforestation-tracker.iam.gserviceaccount.com
GEE_PRIVATE_KEY_PATH=./gee-private-key.json
BIGQUERY_DATASET=forest_monitoring
BIGQUERY_TABLE=forest_loss_zones
GCS_BUCKET=deforestation-exports
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
DEBUG=False
CORS_ORIGINS=["http://localhost:3000"]
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local

# Edit .env.local with your API key
nano .env.local
```

#### Frontend `.env.local` Configuration
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Google Maps API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Enable **Maps JavaScript API**
3. Create API credentials (API Key)
4. Restrict the key to your domains (optional but recommended)
5. Copy the API key to your `.env` files

## 🚀 Running Locally

### Start Backend
```bash
cd backend
python main.py
```
Backend will run on `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Start Frontend
```bash
cd frontend
npm run dev
```
Frontend will run on `http://localhost:3000`

## 📡 API Endpoints

### Forest Loss
- `GET /api/forest-loss` - Get forest loss data
  - Query params: `region`, `start_date`, `end_date`, `method`, `use_bigquery`
- `POST /api/forest-loss/process` - Trigger forest loss processing

### Alerts
- `GET /api/alerts` - Get real-time deforestation alerts
  - Query params: `min_confidence`, `limit`
- `GET /api/alerts/recent` - Get recent alerts
  - Query params: `hours`

### Statistics
- `GET /api/stats` - Get aggregated statistics
  - Query params: `region`, `days`
- `GET /api/stats/timeline` - Get time-series data
  - Query params: `region`, `interval`
- `GET /api/stats/regions` - Get regional breakdown
  - Query params: `days`

### Health
- `GET /health` - Health check endpoint
- `GET /` - API root

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  MapView   │  │ AlertPanel │  │ StatsCard  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────┼────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   Routes   │  │ GEE Pipeline│  │ BQ Handler │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                         │                                    │
│                  ┌──────┴──────┐                             │
│                  │ DSA Algos   │                             │
│                  │ Union-Find  │                             │
│                  │   KD-Tree   │                             │
│                  └─────────────┘                             │
└──────────────────────┬──────────────┬────────────────────────┘
                       │              │
        ┌──────────────┘              └──────────────┐
        │                                            │
┌───────▼────────┐                          ┌────────▼──────┐
│ Google Earth   │                          │   BigQuery    │
│    Engine      │                          │   Database    │
│  (Satellite)   │                          │   (Storage)   │
└────────────────┘                          └───────────────┘
```

## 🧠 DSA Algorithms

### Union-Find (Disjoint Set Union)
- Groups spatially connected deforested pixels
- Path compression for O(α(n)) operations
- Used for clustering deforestation regions

### KD-Tree
- Spatial indexing for fast nearest neighbor queries
- Matches pixels between time periods
- Enables efficient spatial analysis

### Spatial Change Detection
- Combines Union-Find and KD-Tree
- Filters false positives
- Calculates confidence scores based on:
  - Cluster size
  - Spatial compactness
  - Temporal persistence

## 📊 Data Sources

### Hansen Global Forest Change Dataset
- **Dataset**: `UMD/hansen/global_forest_change_2023_v1_11`
- **Resolution**: 30m
- **Coverage**: Global
- **Years**: 2000-2023

### MODIS Vegetation Indices
- **Dataset**: `MODIS/006/MOD13Q1`
- **Resolution**: 250m
- **Temporal**: 16-day composite
- **Indices**: NDVI, EVI

## 🚢 Deployment

### Backend Deployment (Render / Cloud Run)

#### Render
```bash
# Install Render CLI
npm install -g render-cli

# Deploy
cd backend
render deploy
```

#### Google Cloud Run
```bash
# Build container
gcloud builds submit --tag gcr.io/deforestation-tracker/backend

# Deploy
gcloud run deploy backend \
    --image gcr.io/deforestation-tracker/backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod
```

## 🔐 Security Considerations

- ✅ Environment variables for all sensitive data
- ✅ CORS configuration for API security
- ✅ API key restrictions on Google Cloud
- ✅ Service account with minimum required permissions
- ✅ HTTPS enforcement in production
- ✅ Input validation on all endpoints

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📈 Performance Optimizations

- Partitioned BigQuery tables for fast queries
- Efficient spatial algorithms (Union-Find, KD-Tree)
- Async API endpoints with FastAPI
- Client-side caching with React
- Optimized polygon rendering on maps
- Lazy loading and code splitting

## 🐛 Troubleshooting

### GEE Authentication Issues
```bash
# Re-authenticate
earthengine authenticate

# Verify
python -c "import ee; ee.Initialize(); print('Success')"
```

### BigQuery Permission Errors
- Ensure service account has `bigquery.admin` role
- Check dataset and table exist
- Verify project ID is correct

### Frontend API Connection Issues
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify backend is running
- Check CORS configuration in backend

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Authors

- Built for research-grade deforestation monitoring
- Production-ready architecture
- Real-time satellite data processing

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation at `/docs`

## 🙏 Acknowledgments

- Google Earth Engine for satellite data
- Hansen Lab for Global Forest Change dataset
- Google Cloud Platform for infrastructure
- Open source community

---

**Built with ❤️ for forest conservation**



#   d e f o r e s t a t i o n  
 