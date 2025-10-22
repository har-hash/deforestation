"""
BigQuery Handler
Manages data storage and querying in Google BigQuery
"""

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.oauth2.credentials import Credentials
import logging
from datetime import datetime
from typing import Dict, List, Optional
import json
import os
from pathlib import Path

from config import settings

logger = logging.getLogger(__name__)

class BigQueryHandler:
    """Handler for BigQuery operations"""
    
    def __init__(self):
        """Initialize BigQuery client"""
        try:
            # Auto-detect credentials file if not set in environment
            if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
                adc_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
                if adc_path.exists():
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(adc_path)
                    logger.info(f"Auto-detected credentials at: {adc_path}")
            
            self.client = bigquery.Client(project=settings.GCP_PROJECT_ID)
            self.dataset_id = settings.BIGQUERY_DATASET
            self.table_id = settings.BIGQUERY_TABLE
            self.full_table_id = f"{settings.GCP_PROJECT_ID}.{self.dataset_id}.{self.table_id}"
            
            # Ensure dataset and table exist
            self._ensure_dataset_exists()
            self._ensure_table_exists()
            
            logger.info(f"BigQuery handler initialized: {self.full_table_id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize BigQuery: {str(e)}")
            raise
    
    def check_connection(self) -> bool:
        """Check if BigQuery connection is working"""
        try:
            # Simple query to test connection
            query = f"SELECT COUNT(*) as count FROM `{self.full_table_id}` LIMIT 1"
            self.client.query(query).result()
            return True
        except Exception as e:
            logger.error(f"BigQuery connection check failed: {str(e)}")
            return False
    
    def _ensure_dataset_exists(self):
        """Create dataset if it doesn't exist"""
        try:
            self.client.get_dataset(self.dataset_id)
            logger.info(f"Dataset {self.dataset_id} already exists")
        except NotFound:
            dataset = bigquery.Dataset(f"{settings.GCP_PROJECT_ID}.{self.dataset_id}")
            dataset.location = "US"
            dataset = self.client.create_dataset(dataset)
            logger.info(f"Created dataset {self.dataset_id}")
    
    def _ensure_table_exists(self):
        """Create table if it doesn't exist"""
        try:
            self.client.get_table(self.full_table_id)
            logger.info(f"Table {self.table_id} already exists")
        except NotFound:
            schema = [
                bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
                bigquery.SchemaField("region", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("geometry", "GEOGRAPHY", mode="NULLABLE"),
                bigquery.SchemaField("loss_area_ha", "FLOAT64", mode="NULLABLE"),
                bigquery.SchemaField("confidence", "FLOAT64", mode="NULLABLE"),
                bigquery.SchemaField("detection_method", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("metadata", "JSON", mode="NULLABLE"),
            ]
            
            table = bigquery.Table(self.full_table_id, schema=schema)
            
            # Partition by date
            table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="timestamp"
            )
            
            table = self.client.create_table(table)
            logger.info(f"Created table {self.table_id}")
    
    def insert_forest_loss_data(self, geojson: Dict, metadata: Dict) -> bool:
        """
        Insert forest loss data from GeoJSON into BigQuery
        
        Args:
            geojson: GeoJSON FeatureCollection
            metadata: Additional metadata
            
        Returns:
            Success status
        """
        try:
            if not geojson.get('features'):
                logger.warning("No features to insert")
                return True
            
            rows_to_insert = []
            
            for feature in geojson['features']:
                # Extract geometry
                geometry_json = json.dumps(feature['geometry'])
                
                # Convert GeoJSON to WKT for BigQuery GEOGRAPHY
                geometry_wkt = self._geojson_to_wkt(feature['geometry'])
                
                # Prepare row
                row = {
                    'id': f"{metadata.get('region', 'unknown')}_{feature['properties'].get('id', 0)}_{int(datetime.utcnow().timestamp())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'region': metadata.get('region', 'unknown'),
                    'geometry': geometry_wkt,
                    'loss_area_ha': feature['properties'].get('area_ha', 0),
                    'confidence': feature['properties'].get('confidence', 0.85),
                    'detection_method': metadata.get('method', 'unknown'),
                    'metadata': json.dumps(metadata)
                }
                
                rows_to_insert.append(row)
            
            # Insert rows
            errors = self.client.insert_rows_json(self.full_table_id, rows_to_insert)
            
            if errors:
                logger.error(f"Errors inserting rows: {errors}")
                return False
            
            logger.info(f"Inserted {len(rows_to_insert)} rows into BigQuery")
            return True
            
        except Exception as e:
            logger.error(f"Failed to insert data: {str(e)}")
            return False
    
    def _geojson_to_wkt(self, geometry: Dict) -> str:
        """
        Convert GeoJSON geometry to WKT format for BigQuery
        
        Args:
            geometry: GeoJSON geometry object
            
        Returns:
            WKT string
        """
        geom_type = geometry['type']
        coords = geometry['coordinates']
        
        if geom_type == 'Polygon':
            # Format: POLYGON((lon lat, lon lat, ...))
            rings = []
            for ring in coords:
                points = [f"{lon} {lat}" for lon, lat in ring]
                rings.append(f"({', '.join(points)})")
            return f"POLYGON({', '.join(rings)})"
        
        elif geom_type == 'MultiPolygon':
            # Format: MULTIPOLYGON(((lon lat, ...)), ((lon lat, ...)))
            polygons = []
            for polygon in coords:
                rings = []
                for ring in polygon:
                    points = [f"{lon} {lat}" for lon, lat in ring]
                    rings.append(f"({', '.join(points)})")
                polygons.append(f"({', '.join(rings)})")
            return f"MULTIPOLYGON({', '.join(polygons)})"
        
        elif geom_type == 'Point':
            return f"POINT({coords[0]} {coords[1]})"
        
        else:
            logger.warning(f"Unsupported geometry type: {geom_type}")
            return None
    
    def query_forest_loss(
        self,
        region: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_confidence: Optional[float] = None,
        limit: int = 1000
    ) -> List[Dict]:
        """
        Query forest loss data from BigQuery
        
        Args:
            region: Filter by region name
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            min_confidence: Minimum confidence threshold
            limit: Maximum number of results
            
        Returns:
            List of forest loss records
        """
        try:
            # Build query
            query = f"""
                SELECT
                    id,
                    timestamp,
                    region,
                    ST_ASGEOJSON(geometry) as geometry,
                    loss_area_ha,
                    confidence,
                    detection_method,
                    metadata
                FROM `{self.full_table_id}`
                WHERE 1=1
            """
            
            params = []
            
            if region:
                query += " AND region = @region"
                params.append(bigquery.ScalarQueryParameter("region", "STRING", region))
            
            if start_date:
                query += " AND timestamp >= @start_date"
                params.append(bigquery.ScalarQueryParameter("start_date", "TIMESTAMP", start_date))
            
            if end_date:
                query += " AND timestamp <= @end_date"
                params.append(bigquery.ScalarQueryParameter("end_date", "TIMESTAMP", end_date))
            
            if min_confidence:
                query += " AND confidence >= @min_confidence"
                params.append(bigquery.ScalarQueryParameter("min_confidence", "FLOAT64", min_confidence))
            
            query += f" ORDER BY timestamp DESC LIMIT {limit}"
            
            # Configure query job
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            
            # Execute query
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()
            
            # Convert to list of dicts
            records = []
            for row in results:
                record = dict(row)
                # Parse geometry JSON string
                if record.get('geometry'):
                    record['geometry'] = json.loads(record['geometry'])
                # Parse metadata JSON string
                if record.get('metadata'):
                    record['metadata'] = json.loads(record['metadata'])
                records.append(record)
            
            logger.info(f"Query returned {len(records)} records")
            return records
            
        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            return []
    
    def get_statistics(self, region: Optional[str] = None, days: int = 30) -> Dict:
        """
        Get aggregated statistics for forest loss
        
        Args:
            region: Filter by region
            days: Number of days to look back
            
        Returns:
            Statistics dictionary
        """
        try:
            query = f"""
                SELECT
                    COUNT(*) as total_incidents,
                    SUM(loss_area_ha) as total_area_ha,
                    AVG(confidence) as avg_confidence,
                    MIN(timestamp) as first_detection,
                    MAX(timestamp) as last_detection
                FROM `{self.full_table_id}`
                WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
            """
            
            params = [bigquery.ScalarQueryParameter("days", "INT64", days)]
            
            if region:
                query += " AND region = @region"
                params.append(bigquery.ScalarQueryParameter("region", "STRING", region))
            
            job_config = bigquery.QueryJobConfig(query_parameters=params)
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()
            
            row = next(results, None)
            if row:
                return {
                    'total_incidents': row['total_incidents'] or 0,
                    'total_area_ha': round(row['total_area_ha'] or 0, 2),
                    'avg_confidence': round(row['avg_confidence'] or 0, 2),
                    'first_detection': row['first_detection'].isoformat() if row['first_detection'] else None,
                    'last_detection': row['last_detection'].isoformat() if row['last_detection'] else None,
                    'period_days': days
                }
            
            return {
                'total_incidents': 0,
                'total_area_ha': 0,
                'avg_confidence': 0,
                'first_detection': None,
                'last_detection': None,
                'period_days': days
            }
            
        except Exception as e:
            logger.error(f"Statistics query failed: {str(e)}")
            return {}
    
    def get_alerts(self, min_confidence: float = None, limit: int = 100) -> List[Dict]:
        """
        Get recent high-confidence alerts
        
        Args:
            min_confidence: Minimum confidence threshold
            limit: Maximum number of alerts
            
        Returns:
            List of alert records
        """
        if min_confidence is None:
            min_confidence = settings.CONFIDENCE_THRESHOLD
        
        return self.query_forest_loss(
            min_confidence=min_confidence,
            limit=limit
        )

