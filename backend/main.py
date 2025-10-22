"""
Illegal Deforestation Tracker - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Optional
import uvicorn
from datetime import datetime

from routes import forest_loss, alerts, stats
from dependencies import initialize_services, get_gee_pipeline, get_bq_handler
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown"""
    try:
        logger.info("Initializing services...")
        initialize_services()
        logger.info("Application startup complete")
        yield
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise
    finally:
        logger.info("Application shutdown")

# Create FastAPI app
app = FastAPI(
    title="Illegal Deforestation Tracker API",
    description="Real-time satellite-based deforestation detection using GEE, DSA & BigQuery",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(forest_loss.router, prefix="/api", tags=["Forest Loss"])
app.include_router(alerts.router, prefix="/api", tags=["Alerts"])
app.include_router(stats.router, prefix="/api", tags=["Statistics"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Illegal Deforestation Tracker API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check GEE connection
        gee_pipeline = get_gee_pipeline()
        gee_status = gee_pipeline.check_connection() if gee_pipeline else False
        
        # Check BigQuery connection
        bq_handler = get_bq_handler()
        bq_status = bq_handler.check_connection() if bq_handler else False
        
        return {
            "status": "healthy" if (gee_status and bq_status) else "degraded",
            "gee_connected": gee_status,
            "bigquery_connected": bq_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

