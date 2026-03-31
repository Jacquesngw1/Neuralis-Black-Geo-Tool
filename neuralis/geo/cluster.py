"""
cluster.py — Geographic clustering using K-Means and DBSCAN-like algorithms.
"""

import math
import random
from typing import Sequence


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


class KMeansGeo:
    """
    Simple K-Means clustering adapted for geographic coordinates.

    Uses Haversine distance; centroids are computed as arithmetic means of
    lat/lon values (acceptable for small geographic extents).
    """

    def __init__(self, k: int = 5, max_iter: int = 100, seed: int | None = None):
        self.k = k
        self.max_iter = max_iter
        self._rng = random.Random(seed)
        self.centroids: list[dict] = []
        self.labels: list[int] = []

    def fit(self, points: Sequence[dict]) -> list[int]:
        """
        Cluster *points* into self.k groups.

        Args:
            points: List of dicts each with 'lat' and 'lon' keys.

        Returns:
            List of integer cluster labels (same length as *points*).
        """
        pts = [(float(p["lat"]), float(p["lon"])) for p in points]
        if len(pts) < self.k:
            raise ValueError(f"Need at least {self.k} points to form {self.k} clusters.")

        # Initialise centroids randomly
        centroids = self._rng.sample(pts, self.k)

        for _ in range(self.max_iter):
            labels = [self._closest(p, centroids) for p in pts]
            new_centroids = []
            for ci in range(self.k):
                members = [pts[i] for i, lbl in enumerate(labels) if lbl == ci]
                if members:
                    new_lat = sum(m[0] for m in members) / len(members)
                    new_lon = sum(m[1] for m in members) / len(members)
                    new_centroids.append((new_lat, new_lon))
                else:
                    new_centroids.append(centroids[ci])
            if new_centroids == centroids:
                break
            centroids = new_centroids

        self.centroids = [{"lat": c[0], "lon": c[1]} for c in centroids]
        self.labels = labels
        return labels

    @staticmethod
    def _closest(point: tuple, centroids: list) -> int:
        return min(range(len(centroids)), key=lambda i: _haversine(point[0], point[1], centroids[i][0], centroids[i][1]))
