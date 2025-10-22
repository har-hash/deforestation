# 🚀 Deployment Guide

Comprehensive guide for deploying the Illegal Deforestation Tracker to production.

## 📋 Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] Google Cloud services enabled
- [ ] Service account credentials secured
- [ ] API keys restricted to production domains
- [ ] Backend and frontend tested locally
- [ ] Database schema verified
- [ ] HTTPS certificates ready (for custom domains)

## 🔵 Option 1: Deploy Backend to Google Cloud Run

### Step 1: Prepare for Deployment

```bash
cd backend

# Ensure gcloud is configured
gcloud config set project deforestation-tracker
```

### Step 2: Build and Deploy

```bash
# Build container
gcloud builds submit --tag gcr.io/deforestation-tracker/backend

# Deploy to Cloud Run
gcloud run deploy deforestation-backend \
    --image gcr.io/deforestation-tracker/backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8000 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --set-env-vars GCP_PROJECT_ID=deforestation-tracker \
    --set-env-vars BIGQUERY_DATASET=forest_monitoring \
    --set-env-vars BIGQUERY_TABLE=forest_loss_zones \
    --set-env-vars DEBUG=False
```

### Step 3: Add Service Account Key

```bash
# Create secret
gcloud secrets create gee-private-key --data-file=gee-private-key.json

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding gee-private-key \
    --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor

# Update Cloud Run to use secret
gcloud run services update deforestation-backend \
    --region us-central1 \
    --update-secrets /app/gee-private-key.json=gee-private-key:latest
```

### Step 4: Get Backend URL

```bash
gcloud run services describe deforestation-backend \
    --region us-central1 \
    --format 'value(status.url)'
```

Save this URL - you'll need it for frontend deployment.

## 🟣 Option 2: Deploy Backend to Render

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up / Log in
3. Connect GitHub repository

### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure:
   - **Name**: deforestation-backend
   - **Region**: Choose closest to users
   - **Branch**: main
   - **Root Directory**: backend
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Starter ($7/month) or higher

### Step 3: Add Environment Variables

Add in Render dashboard:
```
GCP_PROJECT_ID=deforestation-tracker
GEE_SERVICE_ACCOUNT=your-service-account@...
BIGQUERY_DATASET=forest_monitoring
BIGQUERY_TABLE=forest_loss_zones
DEBUG=False
CORS_ORIGINS=["https://your-frontend-url.vercel.app"]
```

### Step 4: Upload Service Account Key

1. In Render dashboard, go to "Secret Files"
2. Add file: `gee-private-key.json`
3. Paste contents of your service account key
4. Update env var: `GEE_PRIVATE_KEY_PATH=./gee-private-key.json`

## 🟢 Deploy Frontend to Vercel

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Deploy from Local

```bash
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Step 3: Configure Environment Variables

In Vercel dashboard:
1. Go to Project Settings → Environment Variables
2. Add:
   ```
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-maps-api-key
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

### Step 4: Redeploy with Environment Variables

```bash
vercel --prod
```

## 🟠 Option: Deploy Frontend to Netlify

### Step 1: Install Netlify CLI

```bash
npm install -g netlify-cli
```

### Step 2: Deploy

```bash
cd frontend

# Build
npm run build

# Deploy
netlify deploy --prod --dir=.next
```

### Step 3: Configure Environment

In Netlify dashboard → Site Settings → Environment:
```
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-maps-api-key
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## 🐳 Docker Deployment

### Single Server Deployment

```bash
# Clone repository
git clone <your-repo>
cd deforestation-tracker

# Configure environment
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
# Edit both files with production values

# Add service account key
cp /path/to/gee-private-key.json backend/

# Deploy with Docker Compose
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

### Custom Docker Deployment

#### Backend
```bash
cd backend
docker build -t deforestation-backend .
docker run -d \
    -p 8000:8000 \
    --env-file .env \
    -v $(pwd)/gee-private-key.json:/app/gee-private-key.json:ro \
    --name deforestation-backend \
    deforestation-backend
```

#### Frontend
```bash
cd frontend
docker build -t deforestation-frontend .
docker run -d \
    -p 3000:3000 \
    -e NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-key \
    -e NEXT_PUBLIC_API_URL=http://backend:8000 \
    --name deforestation-frontend \
    --link deforestation-backend:backend \
    deforestation-frontend
```

## 🔐 Security Hardening

### 1. Restrict API Keys

#### Google Maps API Key
1. Go to GCP Console → Credentials
2. Edit API key
3. Set HTTP referrers:
   - `https://your-domain.com/*`
   - `https://*.vercel.app/*` (if using Vercel)

#### Service Account Permissions
```bash
# Review permissions
gcloud projects get-iam-policy deforestation-tracker

# Remove unnecessary roles if any
gcloud projects remove-iam-policy-binding deforestation-tracker \
    --member=serviceAccount:... \
    --role=roles/...
```

### 2. Enable HTTPS

- **Vercel/Netlify**: Automatic HTTPS
- **Cloud Run**: Automatic HTTPS
- **Custom server**: Use Let's Encrypt

### 3. Configure CORS Properly

Update `backend/config.py`:
```python
CORS_ORIGINS: List[str] = [
    "https://your-production-domain.com",
    "https://your-frontend.vercel.app"
]
```

### 4. Secure Environment Variables

- Never commit `.env` files
- Use secret managers in production
- Rotate API keys regularly
- Use different keys for dev/prod

## 📊 Monitoring and Logging

### Google Cloud Monitoring

```bash
# Enable Cloud Monitoring
gcloud services enable monitoring.googleapis.com

# View logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

### Application Logs

- **Cloud Run**: Logs appear in Cloud Console
- **Render**: Built-in log viewer
- **Docker**: `docker-compose logs -f`

### Set Up Alerts

1. Go to Cloud Console → Monitoring → Alerting
2. Create alert policy:
   - Metric: HTTP 5xx errors
   - Threshold: > 10 in 5 minutes
   - Notification: Email

## 🔄 CI/CD Setup (Optional)

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Google Cloud
        uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: deforestation-tracker
      
      - name: Deploy to Cloud Run
        run: |
          cd backend
          gcloud builds submit --tag gcr.io/deforestation-tracker/backend
          gcloud run deploy deforestation-backend \
            --image gcr.io/deforestation-tracker/backend \
            --region us-central1

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## 🧪 Post-Deployment Testing

### 1. Health Check
```bash
curl https://your-backend-url.com/health
```

### 2. API Endpoints
```bash
# Stats
curl https://your-backend-url.com/api/stats

# Alerts
curl https://your-backend-url.com/api/alerts?limit=5

# Forest Loss
curl "https://your-backend-url.com/api/forest-loss?method=hansen&use_bigquery=true"
```

### 3. Frontend Verification
- Visit `https://your-frontend-url.com`
- Check browser console for errors
- Verify map loads
- Check API calls in Network tab
- Test all interactive features

## 📈 Performance Optimization

### Backend
- Enable Cloud CDN
- Use Cloud Run min instances: 1
- Enable connection pooling for BigQuery
- Cache frequent queries

### Frontend
- Enable Vercel Edge Network
- Optimize images with Next.js Image
- Enable gzip compression
- Use lazy loading for components

### Database
- Use partitioned tables in BigQuery
- Set up table expiration for old data
- Enable query caching

## 💰 Cost Management

### Estimated Monthly Costs (Moderate Usage)

- **Cloud Run**: $10-30 (depends on traffic)
- **BigQuery**: $5-20 (1TB query/month free)
- **Cloud Storage**: $1-5
- **Earth Engine**: Free (2000 requests/day)
- **Google Maps**: $0-200 (28,000 loads/month free)
- **Vercel**: Free (for hobby) or $20 (Pro)
- **Total**: ~$15-280/month

### Cost Optimization Tips
- Use Cloud Run with min instances: 0 for dev
- Set BigQuery query limits
- Implement caching to reduce API calls
- Monitor usage in GCP Console

## 🐛 Troubleshooting Production Issues

### Backend Not Starting
```bash
# Check logs
gcloud run logs read --service deforestation-backend

# Common issues:
# - Missing environment variables
# - Service account key not found
# - Port not exposed correctly
```

### Frontend Can't Reach Backend
- Verify CORS origins include frontend URL
- Check backend URL in frontend env vars
- Ensure backend is public (--allow-unauthenticated)

### Maps Not Loading
- Verify Maps JavaScript API enabled
- Check API key restrictions
- Review browser console errors

## 📞 Support and Maintenance

### Regular Maintenance Tasks
- [ ] Review logs weekly
- [ ] Check error rates
- [ ] Monitor costs
- [ ] Update dependencies monthly
- [ ] Rotate API keys quarterly
- [ ] Review access permissions

### Backup Strategy
- BigQuery: Automatic backups (7 days)
- Service account keys: Store securely
- Code: Git repository

## 🎉 Go Live Checklist

- [ ] Backend deployed and health check passing
- [ ] Frontend deployed and loading
- [ ] API endpoints responding correctly
- [ ] Maps displaying with satellite imagery
- [ ] Data flowing from GEE to BigQuery
- [ ] Alerts and stats displaying
- [ ] HTTPS enabled
- [ ] API keys restricted
- [ ] Monitoring and logging configured
- [ ] Error tracking enabled
- [ ] Documentation updated with production URLs
- [ ] Team notified of production environment

---

**Your deforestation tracker is now live! 🌍🌲**



