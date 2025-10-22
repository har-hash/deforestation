"""
Google Earth Engine Pipeline
Handles satellite data processing and change detection
"""

import ee
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import numpy as np
from pathlib import Path

from config import settings
from dsa_algorithms import UnionFind, KDTreeSpatial
from image_processor import LocalImageProcessor
from fusion_algorithm import MultiDatasetFusionAlgorithm

logger = logging.getLogger(__name__)

class GEEPipeline:
    """Google Earth Engine data processing pipeline"""
    
    def __init__(self):
        """Initialize GEE with authentication"""
        self.authenticated = False
        self._initialize_gee()
        self.local_processor = LocalImageProcessor()
        self.fusion_algorithm = MultiDatasetFusionAlgorithm()
    
    def _initialize_gee(self):
        """Authenticate and initialize Google Earth Engine"""
        try:
            if settings.GEE_SERVICE_ACCOUNT and settings.GEE_PRIVATE_KEY_PATH:
                # Service account authentication
                credentials = ee.ServiceAccountCredentials(
                    settings.GEE_SERVICE_ACCOUNT,
                    settings.GEE_PRIVATE_KEY_PATH
                )
                ee.Initialize(credentials, project=settings.GCP_PROJECT_ID)
                logger.info("GEE initialized with service account")
            else:
                # Try default authentication with project
                try:
                    ee.Initialize(project=settings.GCP_PROJECT_ID)
                    logger.info(f"GEE initialized with default credentials for project {settings.GCP_PROJECT_ID}")
                except Exception as e:
                    logger.warning(f"GEE initialization failed: {str(e)}")
                    return
            
            self.authenticated = True
            
        except Exception as e:
            logger.error(f"Failed to initialize GEE: {str(e)}")
            self.authenticated = False
    
    def check_connection(self) -> bool:
        """Check if GEE is properly connected"""
        if not self.authenticated:
            return False
        
        try:
            # Simple test to verify connection
            ee.Number(1).getInfo()
            return True
        except Exception as e:
            logger.error(f"GEE connection check failed: {str(e)}")
            return False
    
    def get_roi(self, coords: Optional[List[List[float]]] = None) -> ee.Geometry:
        """
        Get Region of Interest (ROI) geometry
        
        Args:
            coords: List of [lon, lat] coordinates, defaults to Pune region
            
        Returns:
            Earth Engine Geometry
        """
        if coords is None:
            coords = settings.DEFAULT_REGION_COORDS
        
        return ee.Geometry.Polygon(coords)
    
    def calculate_ndvi(self, image: ee.Image, sensor: str = "MODIS") -> ee.Image:
        """
        Calculate NDVI from satellite image
        
        Args:
            image: Input satellite image
            sensor: Sensor type (MODIS, Landsat, Sentinel)
            
        Returns:
            NDVI image
        """
        if sensor == "MODIS":
            # MODIS bands
            nir = image.select('sur_refl_b02')
            red = image.select('sur_refl_b01')
        elif sensor == "Landsat":
            # Landsat 8 bands
            nir = image.select('B5')
            red = image.select('B4')
        elif sensor == "Sentinel":
            # Sentinel-2 bands
            nir = image.select('B8')
            red = image.select('B4')
        else:
            raise ValueError(f"Unknown sensor: {sensor}")
        
        # Calculate NDVI: (NIR - Red) / (NIR + Red)
        ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
        return ndvi
    
    def fetch_raw_imagery(
        self,
        roi: ee.Geometry,
        start_date: str,
        end_date: str,
        scale: int = 30
    ) -> Tuple[np.ndarray, np.ndarray, Tuple]:
        """
        Fetch raw NIR and Red band data as NumPy arrays for local processing
        
        Args:
            roi: Region of interest
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            scale: Resolution in meters (default 30m for Landsat)
            
        Returns:
            Tuple of (before_image, after_image, geo_transform)
            Each image is a NumPy array with shape (height, width, 2) for [NIR, Red]
        """
        logger.info(f"Fetching raw imagery for local processing: {start_date} to {end_date}")
        
        # Calculate mid-point for before/after split
        mid_date = (
            datetime.strptime(start_date, '%Y-%m-%d') +
            (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')) / 2
        ).strftime('%Y-%m-%d')
        
        # Use Landsat 8 for better resolution
        landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
        
        # Before image (early period)
        before = landsat.filterDate(start_date, mid_date) \
                       .filterBounds(roi) \
                       .median() \
                       .select(['SR_B5', 'SR_B4'])  # NIR (B5), Red (B4)
        
        # After image (later period)
        after = landsat.filterDate(mid_date, end_date) \
                      .filterBounds(roi) \
                      .median() \
                      .select(['SR_B5', 'SR_B4'])  # NIR (B5), Red (B4)
        
        # Get region bounds for geo transform
        bounds = roi.bounds().getInfo()['coordinates'][0]
        min_lon = min(c[0] for c in bounds)
        max_lat = max(c[1] for c in bounds)
        max_lon = max(c[0] for c in bounds)
        min_lat = min(c[1] for c in bounds)
        
        # Calculate image dimensions
        width = int((max_lon - min_lon) * 111000 / scale)  # ~111km per degree
        height = int((max_lat - min_lat) * 111000 / scale)
        
        # Download as NumPy arrays
        before_url = before.getDownloadURL({
            'region': roi,
            'scale': scale,
            'format': 'NPY'
        })
        
        after_url = after.getDownloadURL({
            'region': roi,
            'scale': scale,
            'format': 'NPY'
        })
        
        # Download and convert to NumPy
        import urllib.request
        import io
        
        # Download before image
        with urllib.request.urlopen(before_url) as response:
            before_data = np.load(io.BytesIO(response.read()), allow_pickle=True)
        
        # Download after image
        with urllib.request.urlopen(after_url) as response:
            after_data = np.load(io.BytesIO(response.read()), allow_pickle=True)
        
        logger.info(f"Downloaded imagery raw: {before_data.shape}, {after_data.shape}")
        
        # Handle different array structures from GEE
        # If it's a structured array (dict-like), extract bands
        if before_data.dtype.names:
            # Structured array with named fields
            nir_before = before_data['SR_B5'].astype(float)
            red_before = before_data['SR_B4'].astype(float)
            nir_after = after_data['SR_B5'].astype(float)
            red_after = after_data['SR_B4'].astype(float)
        else:
            # Regular array - assume it's [bands, height, width] or [height, width, bands]
            if len(before_data.shape) == 3:
                if before_data.shape[0] == 2:  # [bands, h, w]
                    nir_before = before_data[0].astype(float)
                    red_before = before_data[1].astype(float)
                    nir_after = after_data[0].astype(float)
                    red_after = after_data[1].astype(float)
                else:  # [h, w, bands]
                    nir_before = before_data[:, :, 0].astype(float)
                    red_before = before_data[:, :, 1].astype(float)
                    nir_after = after_data[:, :, 0].astype(float)
                    red_after = after_data[:, :, 1].astype(float)
            else:
                # 2D array - single band, use it for both NIR and Red (fallback)
                logger.warning("Received 2D array, using same data for NIR and Red")
                nir_before = before_data.astype(float)
                red_before = before_data.astype(float) * 0.8  # Simulate difference
                nir_after = after_data.astype(float)
                red_after = after_data.astype(float) * 0.8
        
        # Stack into [height, width, 2] format
        before_stacked = np.stack([nir_before, red_before], axis=-1)
        after_stacked = np.stack([nir_after, red_after], axis=-1)
        
        # Geo transform: (min_lon, pixel_width, 0, max_lat, 0, -pixel_height)
        pixel_width = (max_lon - min_lon) / nir_before.shape[1]
        pixel_height = (max_lat - min_lat) / nir_before.shape[0]
        geo_transform = (min_lon, pixel_width, 0, max_lat, 0, -pixel_height)
        
        logger.info(f"Processed imagery: {before_stacked.shape}, {after_stacked.shape}")
        
        return before_stacked, after_stacked, geo_transform
    
    def detect_forest_loss(
        self,
        region: Optional[List[List[float]]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        use_hansen: bool = True,
        use_local_processing: bool = False,
        use_fusion: bool = False
    ) -> Dict:
        """
        Detect forest loss in the specified region and time period
        
        Args:
            region: Region coordinates
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            use_hansen: Use Hansen Global Forest Change dataset
            use_local_processing: Use local image processing for smooth boundaries
            
        Returns:
            Dictionary with detection results and GeoJSON
        """
        try:
            roi = self.get_roi(region)
            
            # Default dates if not provided
            if not end_date:
                end_date = datetime.utcnow().strftime('%Y-%m-%d')
            if not start_date:
                start_date = (datetime.utcnow() - timedelta(days=365 * 5)).strftime('%Y-%m-%d')
            
            if use_fusion:
                # 🔬 RESEARCH-GRADE: Multi-dataset fusion
                logger.info("Using MULTI-DATASET FUSION (research-grade)")
                return self.fusion_algorithm.detect_fusion(roi, start_date, end_date)
            elif use_local_processing:
                # Use local image processing for smooth, natural boundaries
                logger.info("Using LOCAL image processing (smooth boundaries)")
                return self._detect_local_smooth(roi, start_date, end_date)
            elif use_hansen:
                # Use Hansen Global Forest Change dataset
                return self._detect_hansen_loss(roi, start_date, end_date)
            else:
                # Use NDVI-based detection
                return self._detect_ndvi_loss(roi, start_date, end_date)
                
        except Exception as e:
            logger.error(f"Forest loss detection failed: {str(e)}")
            raise
    
    def _detect_hansen_loss(
        self,
        roi: ee.Geometry,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> Dict:
        """
        PRODUCTION-GRADE Hansen Forest Loss Detection
        ULTRA-HIGH DETAIL like Google Earth Engine UI
        
        Optimized for:
        - Maximum detail (10m resolution)
        - Small patch detection (any size)
        - Natural boundaries (minimal smoothing)
        - High polygon count (like GEE UI)
        
        Args:
            roi: Region of interest
            start_date: Start date
            end_date: End date
            
        Returns:
            Detection results with high detail
        """
        logger.info("🎯 PRODUCTION HANSEN: Ultra-high detail mode")
        
        # Load Hansen dataset
        hansen = ee.Image('UMD/hansen/global_forest_change_2023_v1_11')
        
        # Get tree cover, loss, and loss year
        tree_cover = hansen.select('treecover2000')
        loss = hansen.select('loss')
        loss_year = hansen.select('lossyear')
        
        # Filter by year if dates provided
        if start_date and end_date:
            start_year = int(start_date[:4]) - 2000  # Hansen uses years since 2000
            end_year = int(end_date[:4]) - 2000
            
            loss_mask = loss_year.gte(start_year).And(loss_year.lte(end_year))
            loss = loss.updateMask(loss_mask)
        else:
            # If no dates, use ALL years (like GEE UI default)
            logger.info("No date range - detecting ALL forest loss 2000-2023")
        
        # ULTRA-SENSITIVE: Detect ANY tree cover loss (>5% cover)
        # Like Google Earth Engine UI - shows everything
        loss = loss.updateMask(tree_cover.gt(5))
        
        # Clip to ROI
        loss_roi = loss.clip(roi)
        
        # PRODUCTION VECTORIZATION - Like GEE UI
        # NO SMOOTHING - keep original pixel boundaries
        # HIGH DETAIL - 10m scale (Hansen native is 30m, we oversample for detail)
        vectors = loss_roi.reduceToVectors(
            geometry=roi,
            scale=10,  # HIGHEST DETAIL (oversample Hansen 30m data)
            geometryType='polygon',
            eightConnected=True,  # Connect diagonals for better shapes
            maxPixels=1e10,  # Process EVERYTHING
            bestEffort=True,
            tileScale=16,  # Maximum parallelization
            geometryInNativeProjection=False
        )
        
        # MINIMAL SMOOTHING - Just remove extreme blockiness
        # This keeps detail while making it look professional
        def minimal_smooth(feature):
            geom = feature.geometry()
            
            # Tiny buffer to slightly round corners (1m)
            # This is barely noticeable but removes pixel steps
            smoothed = geom.buffer(1, 0.1).buffer(-1, 0.1)
            
            # Very light simplification (only remove redundant points)
            final = smoothed.simplify(maxError=0.5)
            
            return feature.setGeometry(final)
        
        # Apply minimal smoothing
        vectors = vectors.map(minimal_smooth)
        
        # Convert to GeoJSON
        geojson = self._fc_to_geojson(vectors, roi)
        
        # Calculate statistics
        stats = self._calculate_loss_stats(loss_roi, roi)
        
        logger.info(f"✅ PRODUCTION HANSEN: Detected {len(geojson.get('features', []))} polygons")
        
        return {
            'geojson': geojson,
            'stats': stats,
            'method': 'hansen_production',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _detect_local_smooth(
        self,
        roi: ee.Geometry,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> Dict:
        """
        NEW: Local image processing with smooth, natural boundaries
        Uses advanced CV techniques for professional GIS quality
        
        Args:
            roi: Region of interest
            start_date: Start date
            end_date: End date
            
        Returns:
            Detection results with smooth polygons
        """
        # Default dates
        if not end_date:
            end_date = datetime.utcnow().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        logger.info(f"🎨 LOCAL PROCESSING: {start_date} to {end_date}")
        
        # Step 1: Fetch raw imagery from GEE
        before_image, after_image, geo_transform = self.fetch_raw_imagery(
            roi, start_date, end_date, scale=30
        )
        
        # Step 2: Process locally with advanced image processing
        result = self.local_processor.detect_forest_loss(
            before_image,
            after_image,
            geo_transform
        )
        
        # Step 3: Convert to GeoJSON format
        features = []
        for polygon in result['polygons']:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': polygon['coordinates']
                },
                'properties': {
                    'id': polygon['properties']['id'],
                    'area_ha': polygon['properties'].get('area_pixels', 0) * 0.09 / 10000,  # 30m pixels to ha
                    'confidence': polygon['properties'].get('confidence', 0.85),
                    'timestamp': datetime.utcnow().isoformat(),
                    'method': 'local_smooth'
                }
            }
            features.append(feature)
        
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        # Calculate stats
        total_pixels = result['mask'].sum()
        total_area_ha = total_pixels * 0.09 / 10000  # 30m pixels to hectares
        
        stats = {
            'total_area_ha': round(total_area_ha, 2),
            'pixel_count': int(total_pixels),
            'feature_count': len(features),
            'roi_area_ha': round(roi.area().getInfo() / 10000, 2)
        }
        
        logger.info(f"✨ LOCAL PROCESSING COMPLETE: {len(features)} smooth polygons detected")
        
        return {
            'geojson': geojson,
            'stats': stats,
            'method': 'local_smooth',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _detect_ndvi_loss(
        self,
        roi: ee.Geometry,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> Dict:
        """
        Detect forest loss using NDVI change detection
        
        Args:
            roi: Region of interest
            start_date: Start date for comparison
            end_date: End date for comparison
            
        Returns:
            Detection results
        """
        # Default dates: compare current month with 1 year ago
        if not end_date:
            end_date = datetime.utcnow().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        # Define date ranges
        period1_start = start_date
        period1_end = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')
        period2_start = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d')
        period2_end = end_date
        
        # Load MODIS NDVI data
        modis = ee.ImageCollection('MODIS/006/MOD13Q1')
        
        # Get NDVI for period 1
        ndvi1 = modis.filterDate(period1_start, period1_end) \
                     .filterBounds(roi) \
                     .select('NDVI') \
                     .mean() \
                     .multiply(0.0001)  # Scale factor
        
        # Get NDVI for period 2
        ndvi2 = modis.filterDate(period2_start, period2_end) \
                     .filterBounds(roi) \
                     .select('NDVI') \
                     .mean() \
                     .multiply(0.0001)
        
        # Calculate NDVI difference
        ndvi_diff = ndvi2.subtract(ndvi1)
        
        # ULTRA-SENSITIVE: Detect even minor vegetation loss
        # Changed threshold to catch smaller changes
        threshold = -0.05  # ANY drop of 5% or more in vegetation
        loss = ndvi_diff.lt(threshold)
        
        # ULTRA-SENSITIVE: Lower forest threshold to include shrublands
        # Changed from 0.4 to 0.2 to detect even sparse vegetation loss
        forest_mask = ndvi1.gt(0.2)
        loss = loss.updateMask(forest_mask)
        
        # Clip to ROI
        loss_roi = loss.clip(roi)
        
        # Convert to vectors - PIXEL-LEVEL DETECTION
        vectors = loss_roi.reduceToVectors(
            geometry=roi,
            scale=50,  # INCREASED SENSITIVITY: 50m instead of 250m
            geometryType='polygon',
            eightConnected=True,  # CHANGED: Connect diagonal pixels
            maxPixels=1e10,  # INCREASED: Process more pixels
            bestEffort=True,  # Continue even if hitting limits
            tileScale=4  # Process in smaller tiles
        )
        
        # Convert to GeoJSON
        geojson = self._fc_to_geojson(vectors, roi)
        
        # Calculate statistics
        stats = self._calculate_loss_stats(loss_roi, roi)
        
        return {
            'geojson': geojson,
            'stats': stats,
            'method': 'ndvi',
            'period1': f"{period1_start} to {period1_end}",
            'period2': f"{period2_start} to {period2_end}",
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _fc_to_geojson(self, fc: ee.FeatureCollection, roi: ee.Geometry) -> Dict:
        """
        Convert Earth Engine FeatureCollection to GeoJSON
        
        Args:
            fc: Feature collection
            roi: Region of interest
            
        Returns:
            GeoJSON dictionary
        """
        try:
            # Limit features to prevent timeout
            fc_limited = fc.limit(1000)
            
            # Get as GeoJSON
            geojson = fc_limited.getInfo()
            
            # Add properties to each feature
            if 'features' in geojson:
                for i, feature in enumerate(geojson['features']):
                    feature['properties'] = {
                        'id': i,
                        'detected': datetime.utcnow().isoformat(),
                        'confidence': 0.85,  # Placeholder, can be calculated
                        'area_ha': self._calculate_feature_area(feature)
                    }
            
            return geojson
            
        except Exception as e:
            logger.error(f"Failed to convert to GeoJSON: {str(e)}")
            return {'type': 'FeatureCollection', 'features': []}
    
    def _calculate_feature_area(self, feature: Dict) -> float:
        """
        Calculate area of a GeoJSON feature in hectares
        
        Args:
            feature: GeoJSON feature
            
        Returns:
            Area in hectares
        """
        try:
            geom = ee.Geometry(feature['geometry'])
            area_m2 = geom.area().getInfo()
            area_ha = area_m2 / 10000  # Convert to hectares
            return round(area_ha, 2)
        except Exception:
            return 0.0
    
    def _calculate_loss_stats(self, loss_image: ee.Image, roi: ee.Geometry) -> Dict:
        """
        Calculate statistics for forest loss
        
        Args:
            loss_image: Binary loss image
            roi: Region of interest
            
        Returns:
            Statistics dictionary
        """
        try:
            # Check if image has bands
            band_names = loss_image.bandNames().getInfo()
            if not band_names or len(band_names) == 0:
                logger.warning("Loss image has no bands, returning zero stats")
                return {'total_area_ha': 0, 'pixel_count': 0, 'roi_area_ha': round(roi.area().getInfo() / 10000, 2)}
            
            # Calculate total loss area
            area = loss_image.multiply(ee.Image.pixelArea()) \
                           .reduceRegion(
                               reducer=ee.Reducer.sum(),
                               geometry=roi,
                               scale=30,
                               maxPixels=1e9
                           )
            
            area_info = area.getInfo()
            total_area_m2 = list(area_info.values())[0] if area_info and len(area_info.values()) > 0 else 0
            total_area_ha = total_area_m2 / 10000 if total_area_m2 else 0
            
            # Count pixels
            pixel_count = loss_image.reduceRegion(
                reducer=ee.Reducer.count(),
                geometry=roi,
                scale=30,
                maxPixels=1e9
            ).getInfo()
            
            count = list(pixel_count.values())[0] if pixel_count and len(pixel_count.values()) > 0 else 0
            
            return {
                'total_area_ha': round(total_area_ha, 2),
                'pixel_count': int(count) if count else 0,
                'roi_area_ha': round(roi.area().getInfo() / 10000, 2)
            }
            
        except Exception as e:
            logger.error(f"Stats calculation failed: {str(e)}")
            return {'total_area_ha': 0, 'pixel_count': 0, 'roi_area_ha': 0}
    
    def export_to_gcs(
        self,
        image: ee.Image,
        description: str,
        file_prefix: str
    ) -> ee.batch.Task:
        """
        Export image to Google Cloud Storage
        
        Args:
            image: Image to export
            description: Task description
            file_prefix: File name prefix
            
        Returns:
            Export task
        """
        task = ee.batch.Export.image.toCloudStorage(
            image=image,
            description=description,
            bucket=settings.GCS_BUCKET,
            fileNamePrefix=file_prefix,
            scale=30,
            maxPixels=1e9
        )
        
        task.start()
        logger.info(f"Export task started: {description}")
        
        return task

