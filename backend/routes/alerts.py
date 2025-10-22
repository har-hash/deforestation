"""
Alerts API Routes
Real-time illegal activity detection alerts
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

from dependencies import get_bq_handler
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/alerts")
async def get_alerts(
    min_confidence: Optional[float] = Query(
        None,
        description="Minimum confidence threshold (0-1)",
        ge=0.0,
        le=1.0
    ),
    limit: int = Query(100, description="Maximum number of alerts", le=1000)
):
    """
    Get recent high-confidence deforestation alerts
    
    Returns alerts for illegal activity based on confidence threshold
    """
    try:
        bq_handler = get_bq_handler()
        if not bq_handler:
            raise HTTPException(status_code=503, detail="BigQuery not available")
        
        # Use default threshold if not provided
        if min_confidence is None:
            min_confidence = settings.CONFIDENCE_THRESHOLD
        
        # Query alerts from BigQuery
        alerts = bq_handler.get_alerts(
            min_confidence=min_confidence,
            limit=limit
        )
        
        # Format alerts
        formatted_alerts = []
        for alert in alerts:
            formatted_alert = {
                'id': alert.get('id'),
                'timestamp': alert.get('timestamp'),
                'region': alert.get('region'),
                'area_ha': alert.get('loss_area_ha'),
                'confidence': alert.get('confidence'),
                'method': alert.get('detection_method'),
                'geometry': alert.get('geometry'),
                'severity': _calculate_severity(
                    alert.get('loss_area_ha', 0),
                    alert.get('confidence', 0)
                )
            }
            formatted_alerts.append(formatted_alert)
        
        return {
            'success': True,
            'count': len(formatted_alerts),
            'threshold': min_confidence,
            'alerts': formatted_alerts
        }
    
    except Exception as e:
        logger.error(f"Error getting alerts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/recent")
async def get_recent_alerts(
    hours: int = Query(24, description="Time window in hours", le=720)
):
    """
    Get alerts from the last N hours
    """
    try:
        bq_handler = get_bq_handler()
        if not bq_handler:
            raise HTTPException(status_code=503, detail="BigQuery not available")
        
        # Convert hours to days for BigQuery query
        days = hours / 24
        
        # Get statistics which includes recent data
        stats = bq_handler.get_statistics(days=int(days) + 1)
        
        # Get recent alerts
        alerts = bq_handler.get_alerts(
            min_confidence=settings.CONFIDENCE_THRESHOLD,
            limit=50
        )
        
        return {
            'success': True,
            'time_window_hours': hours,
            'total_incidents': stats.get('total_incidents', 0),
            'total_area_ha': stats.get('total_area_ha', 0),
            'alerts': alerts[:20]  # Return top 20 most recent
        }
    
    except Exception as e:
        logger.error(f"Error getting recent alerts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def _calculate_severity(area_ha: float, confidence: float) -> str:
    """
    Calculate alert severity based on area and confidence
    
    Args:
        area_ha: Deforested area in hectares
        confidence: Confidence score (0-1)
        
    Returns:
        Severity level: low, medium, high, critical
    """
    # Weighted score
    score = (area_ha * 0.6) + (confidence * 100 * 0.4)
    
    if score >= 50:
        return "critical"
    elif score >= 30:
        return "high"
    elif score >= 15:
        return "medium"
    else:
        return "low"

