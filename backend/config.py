"""
Configuration management for the application
Loads environment variables and provides configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    
    # Google Cloud Project
    GCP_PROJECT_ID: str = "deforestation-tracker-475003"
    
    # Google Earth Engine
    GEE_SERVICE_ACCOUNT: str = ""
    GEE_PRIVATE_KEY_PATH: str = ""
    
    # BigQuery
    BIGQUERY_DATASET: str = "forest_monitoring"
    BIGQUERY_TABLE: str = "forest_loss_zones"
    
    # Google Cloud Storage
    GCS_BUCKET: str = "deforestation-exports"
    
    # Google Maps
    GOOGLE_MAPS_API_KEY: str = ""
    
    # Application settings
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:3005",
        "https://deforestation-tracker.vercel.app"
    ]
    
    # Detection parameters
    NDVI_THRESHOLD: float = -0.2  # Threshold for vegetation loss
    CONFIDENCE_THRESHOLD: float = 0.7  # Minimum confidence for alerts
    MIN_CLUSTER_SIZE: int = 5  # Minimum pixels for deforestation cluster
    
    # Data refresh interval (hours)
    REFRESH_INTERVAL: int = 24
    
    # Default region (Pune, India)
    DEFAULT_REGION_COORDS: List[List[float]] = [
        [73.6, 18.3],
        [74.2, 18.3],
        [74.2, 18.8],
        [73.6, 18.8],
        [73.6, 18.3]
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

# Create settings instance
settings = Settings()

# Ensure required directories exist
Path("logs").mkdir(exist_ok=True)
Path("exports").mkdir(exist_ok=True)

