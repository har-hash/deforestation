"""
DSA Algorithms for Spatial Change Detection
Implements Union-Find and KD-Tree for efficient spatial analysis

⚠️ STATUS: REFERENCE IMPLEMENTATION - NOT CURRENTLY IN PRODUCTION USE

This file contains custom implementations of spatial data structures (Union-Find, KD-Tree)
that were originally intended for clustering deforestation regions.

WHY NOT USED:
- Google Earth Engine's built-in reduceToVectors() is more efficient and reliable
- GEE handles vectorization and clustering natively on their servers
- Our custom Python DSA would require downloading full rasters (expensive/slow)
- Production code uses GEE's optimized server-side operations

KEPT FOR:
- Reference implementation for educational purposes
- Future experimentation with client-side clustering
- Potential use in post-processing of GEE results

To use these algorithms in production, you would need to:
1. Download full resolution imagery from GEE
2. Run detection locally (very CPU/memory intensive)
3. Implement worker queue architecture to handle load
"""

import numpy as np
from typing import List, Tuple, Dict, Set
from scipy.spatial import KDTree
import logging

logger = logging.getLogger(__name__)

class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure
    Used to group connected deforested regions
    """
    
    def __init__(self, n: int):
        """
        Initialize Union-Find structure
        
        Args:
            n: Number of elements
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
    
    def find(self, x: int) -> int:
        """
        Find the root of element x with path compression
        
        Args:
            x: Element to find
            
        Returns:
            Root of the set containing x
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """
        Union two sets by rank
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if union was performed, False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1
        
        return True
    
    def get_size(self, x: int) -> int:
        """
        Get size of the set containing x
        
        Args:
            x: Element
            
        Returns:
            Size of the set
        """
        root = self.find(x)
        return self.size[root]
    
    def get_components(self) -> Dict[int, List[int]]:
        """
        Get all connected components
        
        Returns:
            Dictionary mapping root to list of elements in that component
        """
        components = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in components:
                components[root] = []
            components[root].append(i)
        return components


class KDTreeSpatial:
    """
    KD-Tree for spatial point matching and nearest neighbor search
    Used to quickly match forest change pixels between time periods
    """
    
    def __init__(self, points: np.ndarray):
        """
        Initialize KD-Tree with points
        
        Args:
            points: Nx2 array of (lon, lat) coordinates
        """
        self.points = points
        self.tree = KDTree(points)
        logger.info(f"KD-Tree built with {len(points)} points")
    
    def query_radius(self, query_points: np.ndarray, radius: float) -> List[List[int]]:
        """
        Find all points within radius of each query point
        
        Args:
            query_points: Mx2 array of query coordinates
            radius: Search radius (in same units as points)
            
        Returns:
            List of lists containing indices of neighbors for each query point
        """
        return self.tree.query_ball_point(query_points, radius)
    
    def query_nearest(self, query_points: np.ndarray, k: int = 1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find k nearest neighbors for each query point
        
        Args:
            query_points: Mx2 array of query coordinates
            k: Number of nearest neighbors
            
        Returns:
            Tuple of (distances, indices)
        """
        distances, indices = self.tree.query(query_points, k=k)
        return distances, indices


class SpatialChangeDetector:
    """
    Spatial change detection using DSA algorithms
    Combines Union-Find and KD-Tree for efficient deforestation clustering
    """
    
    def __init__(self, min_cluster_size: int = 5, neighbor_distance: float = 0.001):
        """
        Initialize spatial change detector
        
        Args:
            min_cluster_size: Minimum pixels for valid deforestation cluster
            neighbor_distance: Distance threshold for connecting pixels (degrees)
        """
        self.min_cluster_size = min_cluster_size
        self.neighbor_distance = neighbor_distance
    
    def cluster_changes(self, change_pixels: np.ndarray) -> List[np.ndarray]:
        """
        Cluster spatially connected change pixels using Union-Find
        
        Args:
            change_pixels: Nx2 array of (lon, lat) coordinates of detected changes
            
        Returns:
            List of clusters, each cluster is an array of pixel coordinates
        """
        if len(change_pixels) == 0:
            return []
        
        n = len(change_pixels)
        uf = UnionFind(n)
        
        # Build KD-Tree for efficient spatial queries
        kdtree = KDTreeSpatial(change_pixels)
        
        # Find neighbors for each pixel and union them
        neighbors_list = kdtree.query_radius(change_pixels, self.neighbor_distance)
        
        for i, neighbors in enumerate(neighbors_list):
            for j in neighbors:
                if i != j:
                    uf.union(i, j)
        
        # Get connected components
        components = uf.get_components()
        
        # Filter by minimum cluster size
        clusters = []
        for root, indices in components.items():
            if len(indices) >= self.min_cluster_size:
                cluster_pixels = change_pixels[indices]
                clusters.append(cluster_pixels)
        
        logger.info(f"Detected {len(clusters)} valid clusters from {n} change pixels")
        return clusters
    
    def match_temporal_changes(
        self,
        t1_pixels: np.ndarray,
        t2_pixels: np.ndarray,
        max_distance: float = 0.0005
    ) -> List[Tuple[int, int]]:
        """
        Match pixels between two time periods using KD-Tree
        
        Args:
            t1_pixels: Pixels from time period 1
            t2_pixels: Pixels from time period 2
            max_distance: Maximum distance for matching
            
        Returns:
            List of (t1_index, t2_index) matches
        """
        if len(t1_pixels) == 0 or len(t2_pixels) == 0:
            return []
        
        # Build KD-Tree for t2 pixels
        kdtree = KDTreeSpatial(t2_pixels)
        
        # Find nearest neighbor in t2 for each t1 pixel
        distances, indices = kdtree.query_nearest(t1_pixels, k=1)
        
        # Filter by maximum distance
        matches = []
        for i, (dist, j) in enumerate(zip(distances, indices)):
            if dist <= max_distance:
                matches.append((i, j))
        
        logger.info(f"Matched {len(matches)} pixels between time periods")
        return matches
    
    def calculate_change_confidence(
        self,
        cluster_pixels: np.ndarray,
        reference_pixels: np.ndarray
    ) -> float:
        """
        Calculate confidence score for a deforestation cluster
        
        Args:
            cluster_pixels: Pixels in the detected cluster
            reference_pixels: Reference pixels for validation
            
        Returns:
            Confidence score (0-1)
        """
        if len(cluster_pixels) == 0:
            return 0.0
        
        # Factors for confidence:
        # 1. Cluster size (larger = more confident)
        size_score = min(len(cluster_pixels) / 100, 1.0)
        
        # 2. Spatial compactness (more compact = more confident)
        if len(cluster_pixels) > 1:
            centroid = np.mean(cluster_pixels, axis=0)
            distances = np.linalg.norm(cluster_pixels - centroid, axis=1)
            avg_distance = np.mean(distances)
            compactness_score = 1.0 / (1.0 + avg_distance * 100)
        else:
            compactness_score = 1.0
        
        # 3. Temporal persistence (if reference data available)
        if len(reference_pixels) > 0:
            kdtree = KDTreeSpatial(reference_pixels)
            distances, _ = kdtree.query_nearest(cluster_pixels, k=1)
            persistence_score = np.mean(distances < self.neighbor_distance)
        else:
            persistence_score = 0.8  # Default if no reference
        
        # Combine scores
        confidence = (size_score * 0.3 + compactness_score * 0.4 + persistence_score * 0.3)
        
        return round(confidence, 2)
    
    def filter_false_positives(
        self,
        clusters: List[np.ndarray],
        reference_data: np.ndarray = None
    ) -> List[Tuple[np.ndarray, float]]:
        """
        Filter false positives from detected clusters
        
        Args:
            clusters: List of detected clusters
            reference_data: Optional reference data for validation
            
        Returns:
            List of (cluster, confidence) tuples
        """
        filtered = []
        
        for cluster in clusters:
            confidence = self.calculate_change_confidence(
                cluster,
                reference_data if reference_data is not None else np.array([])
            )
            
            # Only keep high-confidence clusters
            if confidence >= 0.5:
                filtered.append((cluster, confidence))
        
        logger.info(f"Filtered to {len(filtered)} high-confidence clusters from {len(clusters)}")
        return filtered



