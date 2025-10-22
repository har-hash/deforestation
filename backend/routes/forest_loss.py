"""
Forest Loss API Routes
Endpoints for querying and retrieving forest loss data
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
import logging

from dependencies import get_gee_pipeline, get_bq_handler

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/forest-loss")
async def get_forest_loss(
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    radius: Optional[float] = Query(10000, description="Radius in meters"),
    region: Optional[str] = Query(None, description="Region name or coordinates"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    method: Optional[str] = Query("hansen", description="Detection method: hansen, ndvi, local_smooth, or combination"),
    use_bigquery: bool = Query(False, description="Query from BigQuery instead of live GEE"),
    use_local_processing: bool = Query(False, description="Use local image processing for smooth boundaries"),
    use_fusion: bool = Query(False, description="Use multi-dataset fusion (research-grade)")
):
    """
    Get forest loss data for a specific region and time period
    
    Returns GeoJSON FeatureCollection with deforestation polygons
    """
    try:
        if use_bigquery:
            # Query from BigQuery
            bq_handler = get_bq_handler()
            if not bq_handler:
                raise HTTPException(status_code=503, detail="BigQuery not available")
            
            records = bq_handler.query_forest_loss(
                region=region,
                start_date=start_date,
                end_date=end_date
            )
            
            # Convert to GeoJSON
            features = []
            for record in records:
                feature = {
                    'type': 'Feature',
                    'geometry': record.get('geometry'),
                    'properties': {
                        'id': record.get('id'),
                        'timestamp': record.get('timestamp'),
                        'region': record.get('region'),
                        'area_ha': record.get('loss_area_ha'),
                        'confidence': record.get('confidence'),
                        'method': record.get('detection_method')
                    }
                }
                features.append(feature)
            
            geojson = {
                'type': 'FeatureCollection',
                'features': features
            }
            
            return {
                'success': True,
                'source': 'bigquery',
                'count': len(features),
                'data': geojson
            }
        
        else:
            # Live detection from GEE
            gee_pipeline = get_gee_pipeline()
            if not gee_pipeline:
                raise HTTPException(status_code=503, detail="GEE not available")
            
            # Parse region coordinates
            coords = None
            if lat is not None and lon is not None and radius:
                # Convert lat/lon + radius to bounding box
                # Approximate: 1 degree = 111km
                radius_deg = radius / 111000  # Convert meters to degrees
                coords = [[
                    [lon - radius_deg, lat - radius_deg],
                    [lon + radius_deg, lat - radius_deg],
                    [lon + radius_deg, lat + radius_deg],
                    [lon - radius_deg, lat + radius_deg],
                    [lon - radius_deg, lat - radius_deg]
                ]]
                logger.info(f"Scanning region: lat={lat}, lon={lon}, radius={radius}m")
            elif region and ',' in region:
                try:
                    # Format: "lon1,lat1;lon2,lat2;..."
                    coord_pairs = region.split(';')
                    coords = [[float(x) for x in pair.split(',')] for pair in coord_pairs]
                except Exception:
                    logger.warning(f"Failed to parse region coordinates: {region}")
            
            # Detect forest loss
            # Support multiple methods
            if method.lower() == "combination" or use_fusion:
                logger.info("🔬 Using MULTI-DATASET FUSION (research-grade)")
                result = gee_pipeline.detect_forest_loss(
                    region=coords,
                    start_date=start_date,
                    end_date=end_date,
                    use_hansen=False,
                    use_local_processing=False,
                    use_fusion=True
                )
            elif method.lower() == "local_smooth" or use_local_processing:
                logger.info("Using LOCAL image processing (smooth boundaries)")
                result = gee_pipeline.detect_forest_loss(
                    region=coords,
                    start_date=start_date,
                    end_date=end_date,
                    use_hansen=False,
                    use_local_processing=True,
                    use_fusion=False
                )
            else:
                use_hansen = (method.lower() == "hansen")
                result = gee_pipeline.detect_forest_loss(
                    region=coords,
                    start_date=start_date,
                    end_date=end_date,
                    use_hansen=use_hansen,
                    use_local_processing=False,
                    use_fusion=False
                )
            
            # Note: BigQuery streaming inserts disabled (not available in free tier)
            # If you have a paid BigQuery account, uncomment below:
            # bq_handler = get_bq_handler()
            # if bq_handler and result.get('geojson'):
            #     metadata = {
            #         'region': region or 'default',
            #         'method': result.get('method'),
            #         'start_date': start_date,
            #         'end_date': end_date
            #     }
            #     bq_handler.insert_forest_loss_data(result['geojson'], metadata)
            
            return {
                'success': True,
                'source': 'gee',
                'method': result.get('method'),
                'stats': result.get('stats'),
                'data': result.get('geojson')
            }
    
    except Exception as e:
        logger.error(f"Error getting forest loss data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/forest-loss/process")
async def process_forest_loss(
    region: str,
    start_date: str,
    end_date: str,
    method: str = "hansen"
):
    """
    Trigger forest loss processing for a region
    Runs detection and saves results to BigQuery
    """
    try:
        gee_pipeline = get_gee_pipeline()
        bq_handler = get_bq_handler()
        
        if not gee_pipeline or not bq_handler:
            raise HTTPException(status_code=503, detail="Services not available")
        
        # Parse coordinates if needed
        coords = None
        if ',' in region:
            coord_pairs = region.split(';')
            coords = [[float(x) for x in pair.split(',')] for pair in coord_pairs]
        
        # Run detection
        use_hansen = (method.lower() == "hansen")
        result = gee_pipeline.detect_forest_loss(
            region=coords,
            start_date=start_date,
            end_date=end_date,
            use_hansen=use_hansen
        )
        
        # Save to BigQuery
        metadata = {
            'region': region,
            'method': result.get('method'),
            'start_date': start_date,
            'end_date': end_date
        }
        
        success = bq_handler.insert_forest_loss_data(result['geojson'], metadata)
        
        return {
            'success': success,
            'method': result.get('method'),
            'features_detected': len(result['geojson'].get('features', [])),
            'stats': result.get('stats')
        }
    
    except Exception as e:
        logger.error(f"Error processing forest loss: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

