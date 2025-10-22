"""
Dependency injection for FastAPI
Provides global instances of GEE pipeline and BigQuery handler
"""

from typing import Optional
from gee_pipeline import GEEPipeline
from bigquery_handler import BigQueryHandler

# Global instances
_gee_pipeline: Optional[GEEPipeline] = None
_bq_handler: Optional[BigQueryHandler] = None


def initialize_services():
    """Initialize global service instances"""
    global _gee_pipeline, _bq_handler
    
    print("Initializing services...")
    
    # Initialize GEE
    try:
        _gee_pipeline = GEEPipeline()
        if _gee_pipeline and _gee_pipeline.authenticated:
            print("Google Earth Engine connected")
        else:
            print("GEE not authenticated - sign up at https://earthengine.google.com/signup/")
    except Exception as e:
        print(f"GEE initialization failed: {e}")
        _gee_pipeline = None
    
    # Initialize BigQuery
    try:
        _bq_handler = BigQueryHandler()
        if _bq_handler and _bq_handler.check_connection():
            print("BigQuery connected")
        else:
            print("BigQuery not authenticated - using mock data")
    except Exception as e:
        print(f"BigQuery initialization failed: {e}")
        _bq_handler = None
    
    print("Server ready! (Some services may need authentication)")


def get_gee_pipeline() -> Optional[GEEPipeline]:
    """Get GEE pipeline instance"""
    return _gee_pipeline


def get_bq_handler() -> Optional[BigQueryHandler]:
    """Get BigQuery handler instance"""
    return _bq_handler

