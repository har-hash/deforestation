# Backend - Illegal Deforestation Tracker

FastAPI backend for real-time deforestation detection using Google Earth Engine and BigQuery.

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration and settings
├── gee_pipeline.py        # Google Earth Engine data processing
├── bigquery_handler.py    # BigQuery operations
├── dsa_algorithms.py      # DSA algorithms (Union-Find, KD-Tree)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── routes/
│   ├── __init__.py
│   ├── forest_loss.py    # Forest loss endpoints
│   ├── alerts.py         # Alert endpoints
│   └── stats.py          # Statistics endpoints
├── models/
│   └── __init__.py       # Data models
└── logs/                  # Application logs
```

## 🔧 Installation

### 1. Create Virtual Environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file in the backend directory:

```env
GCP_PROJECT_ID=deforestation-tracker
GEE_SERVICE_ACCOUNT=your-service-account@your-project.iam.gserviceaccount.com
GEE_PRIVATE_KEY_PATH=./gee-private-key.json
BIGQUERY_DATASET=forest_monitoring
BIGQUERY_TABLE=forest_loss_zones
GCS_BUCKET=deforestation-exports
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
DEBUG=False
CORS_ORIGINS=["http://localhost:3000"]
NDVI_THRESHOLD=-0.2
CONFIDENCE_THRESHOLD=0.7
MIN_CLUSTER_SIZE=5
```

### 4. Authenticate Google Earth Engine

#### Option A: Service Account (Recommended for Production)
1. Download service account key JSON from GCP
2. Place in backend directory
3. Update `GEE_PRIVATE_KEY_PATH` in `.env`

#### Option B: User Authentication (Development)
```bash
earthengine authenticate
```

### 5. Initialize BigQuery

The application will automatically create the required dataset and table on startup. Ensure your service account has the necessary permissions.

## 🚀 Running the Server

### Development Mode
```bash
python main.py
```

### Production Mode with Uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server will start at `http://localhost:8000`

## 📡 API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔌 API Endpoints

### Health Check
```http
GET /health
```

### Forest Loss Detection
```http
GET /api/forest-loss
  ?region=<region_name>
  &start_date=YYYY-MM-DD
  &end_date=YYYY-MM-DD
  &method=hansen|ndvi
  &use_bigquery=true|false
```

```http
POST /api/forest-loss/process
{
  "region": "Pune, India",
  "start_date": "2023-01-01",
  "end_date": "2024-01-01",
  "method": "hansen"
}
```

### Alerts
```http
GET /api/alerts
  ?min_confidence=0.7
  &limit=100
```

```http
GET /api/alerts/recent
  ?hours=24
```

### Statistics
```http
GET /api/stats
  ?region=<region_name>
  &days=30
```

```http
GET /api/stats/timeline
  ?region=<region_name>
  &interval=day|week|month
```

```http
GET /api/stats/regions
  ?days=30
```

## 🧠 Core Components

### Google Earth Engine Pipeline (`gee_pipeline.py`)

Handles satellite data processing:
- Hansen Global Forest Change dataset
- MODIS NDVI/EVI vegetation indices
- Temporal change detection
- Vector conversion and export

Key methods:
- `detect_forest_loss()` - Main detection function
- `calculate_ndvi()` - Vegetation index calculation
- `_detect_hansen_loss()` - Hansen dataset processing
- `_detect_ndvi_loss()` - NDVI-based detection

### BigQuery Handler (`bigquery_handler.py`)

Manages data storage and queries:
- Automatic dataset/table creation
- Efficient data insertion
- Parameterized queries
- Time-partitioned tables

Key methods:
- `insert_forest_loss_data()` - Store detection results
- `query_forest_loss()` - Retrieve forest loss data
- `get_statistics()` - Aggregated metrics
- `get_alerts()` - High-confidence detections

### DSA Algorithms (`dsa_algorithms.py`)

Spatial analysis algorithms:
- **Union-Find**: Cluster connected deforestation regions
- **KD-Tree**: Fast spatial queries and nearest neighbor search
- **Spatial Change Detector**: Combines algorithms for accurate detection

Key classes:
- `UnionFind` - Disjoint set union with path compression
- `KDTreeSpatial` - Spatial indexing and queries
- `SpatialChangeDetector` - Change detection and confidence scoring

## 🔐 Security

- Environment variables for sensitive data
- CORS middleware configured
- Input validation on all endpoints
- Parameterized database queries
- Service account with minimum permissions

## 📊 Data Flow

```
1. API Request
   ↓
2. FastAPI Route Handler
   ↓
3. Google Earth Engine
   - Load satellite imagery
   - Apply algorithms
   - Detect changes
   ↓
4. DSA Processing
   - Union-Find clustering
   - KD-Tree spatial analysis
   - Confidence scoring
   ↓
5. BigQuery Storage
   - Insert results
   - Create partitions
   ↓
6. API Response
   - Return GeoJSON
   - Include statistics
```

## 🐛 Troubleshooting

### GEE Authentication Failed
```bash
# Check authentication
python -c "import ee; ee.Initialize(); print('Success')"

# Re-authenticate
earthengine authenticate
```

### BigQuery Permission Denied
- Verify service account has `bigquery.admin` role
- Check project ID matches in `.env` and GCP
- Ensure billing is enabled on GCP project

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.9+
```

## 🧪 Testing

Run tests with pytest:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GCP_PROJECT_ID` | Google Cloud project ID | Yes |
| `GEE_SERVICE_ACCOUNT` | Service account email | Yes* |
| `GEE_PRIVATE_KEY_PATH` | Path to service account key | Yes* |
| `BIGQUERY_DATASET` | BigQuery dataset name | Yes |
| `BIGQUERY_TABLE` | BigQuery table name | Yes |
| `GCS_BUCKET` | Cloud Storage bucket | No |
| `GOOGLE_MAPS_API_KEY` | Google Maps API key | No |
| `DEBUG` | Debug mode | No |
| `CORS_ORIGINS` | Allowed CORS origins | No |

\* Required for production. Can use user auth in development.

## 🚢 Deployment

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Run
```bash
gcloud run deploy backend \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

## 📈 Performance Tips

- Use BigQuery partitioned tables for better performance
- Cache GEE results when possible
- Limit polygon features to prevent timeout
- Use async endpoints for long-running tasks
- Monitor API quotas on GCP

## 🔗 Related Documentation

- [Google Earth Engine Python API](https://developers.google.com/earth-engine/guides/python_install)
- [BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📧 Support

For backend-specific issues:
1. Check logs in `logs/` directory
2. Review API documentation at `/docs`
3. Verify GCP service status
4. Check environment configuration



