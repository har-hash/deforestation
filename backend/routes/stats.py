"""
Statistics API Routes
Aggregated deforestation statistics and analytics
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging
from datetime import datetime, timedelta

from dependencies import get_bq_handler

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/stats")
async def get_statistics(
    region: Optional[str] = Query(None, description="Filter by region"),
    days: int = Query(30, description="Time period in days", le=365)
):
    """
    Get aggregated deforestation statistics
    
    Returns:
        - Total deforested area
        - Number of incidents
        - Rate of change
        - Confidence metrics
    """
    try:
        bq_handler = get_bq_handler()
        if not bq_handler:
            raise HTTPException(status_code=503, detail="BigQuery not available")
        
        # Get statistics from BigQuery
        stats = bq_handler.get_statistics(region=region, days=days)
        
        # Calculate additional metrics
        total_area = stats.get('total_area_ha', 0)
        total_incidents = stats.get('total_incidents', 0)
        
        # Calculate rate (hectares per day)
        rate_per_day = total_area / days if days > 0 else 0
        
        # Calculate average incident size
        avg_incident_size = total_area / total_incidents if total_incidents > 0 else 0
        
        return {
            'success': True,
            'region': region or 'all',
            'period_days': days,
            'total_area_ha': round(total_area, 2),
            'total_incidents': total_incidents,
            'avg_confidence': stats.get('avg_confidence', 0),
            'rate_per_day_ha': round(rate_per_day, 2),
            'avg_incident_size_ha': round(avg_incident_size, 2),
            'first_detection': stats.get('first_detection'),
            'last_detection': stats.get('last_detection')
        }
    
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/timeline")
async def get_timeline_stats(
    region: Optional[str] = Query(None, description="Filter by region"),
    interval: str = Query("month", description="Time interval: day, week, month")
):
    """
    Get time-series statistics for visualization
    """
    try:
        bq_handler = get_bq_handler()
        if not bq_handler:
            raise HTTPException(status_code=503, detail="BigQuery not available")
        
        # Map interval to BigQuery time unit
        interval_map = {
            'day': 'DAY',
            'week': 'WEEK',
            'month': 'MONTH'
        }
        
        time_unit = interval_map.get(interval.lower(), 'MONTH')
        
        # Build timeline query
        query = f"""
            SELECT
                TIMESTAMP_TRUNC(timestamp, {time_unit}) as period,
                COUNT(*) as incidents,
                SUM(loss_area_ha) as total_area_ha,
                AVG(confidence) as avg_confidence
            FROM `{bq_handler.full_table_id}`
            WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 YEAR)
        """
        
        if region:
            query += f" AND region = '{region}'"
        
        query += " GROUP BY period ORDER BY period DESC LIMIT 12"
        
        # Execute query
        query_job = bq_handler.client.query(query)
        results = query_job.result()
        
        # Format results
        timeline = []
        for row in results:
            timeline.append({
                'period': row['period'].isoformat() if row['period'] else None,
                'incidents': row['incidents'] or 0,
                'total_area_ha': round(row['total_area_ha'] or 0, 2),
                'avg_confidence': round(row['avg_confidence'] or 0, 2)
            })
        
        # Reverse to show chronological order
        timeline.reverse()
        
        return {
            'success': True,
            'interval': interval,
            'region': region or 'all',
            'timeline': timeline
        }
    
    except Exception as e:
        logger.error(f"Error getting timeline stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/regions")
async def get_regional_stats(
    days: int = Query(30, description="Time period in days", le=365)
):
    """
    Get statistics broken down by region
    """
    try:
        bq_handler = get_bq_handler()
        if not bq_handler:
            raise HTTPException(status_code=503, detail="BigQuery not available")
        
        # Query regional breakdown
        query = f"""
            SELECT
                region,
                COUNT(*) as incidents,
                SUM(loss_area_ha) as total_area_ha,
                AVG(confidence) as avg_confidence
            FROM `{bq_handler.full_table_id}`
            WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
            GROUP BY region
            ORDER BY total_area_ha DESC
        """
        
        from google.cloud import bigquery
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("days", "INT64", days)
            ]
        )
        
        query_job = bq_handler.client.query(query, job_config=job_config)
        results = query_job.result()
        
        # Format results
        regions = []
        for row in results:
            regions.append({
                'region': row['region'],
                'incidents': row['incidents'] or 0,
                'total_area_ha': round(row['total_area_ha'] or 0, 2),
                'avg_confidence': round(row['avg_confidence'] or 0, 2)
            })
        
        return {
            'success': True,
            'period_days': days,
            'total_regions': len(regions),
            'regions': regions
        }
    
    except Exception as e:
        logger.error(f"Error getting regional stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

