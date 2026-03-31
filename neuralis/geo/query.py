"""
query.py — Spatial query helpers: radius, bounding box, and polygon intersection.
"""

import math
from typing import Sequence
from .geocoder import haversine_distance


class SpatialQuery:
    """Perform spatial queries against a collection of geographic points."""

    def __init__(self, points: Sequence[dict] | None = None):
        """
        Args:
            points: Optional list of point dicts, each containing at minimum
                    'lat' and 'lon' keys (float values).
        """
        self._points: list[dict] = list(points) if points else []

    def load(self, points: Sequence[dict]) -> None:
        """Replace the current point set."""
        self._points = list(points)

    # ------------------------------------------------------------------
    # Query methods
    # ------------------------------------------------------------------

    def radius(self, lat: float, lon: float, radius_km: float) -> list[dict]:
        """
        Return all points within *radius_km* kilometres of (lat, lon).

        Each returned dict includes the original point data plus a
        'distance_km' key with the computed distance.
        """
        results = []
        for point in self._points:
            dist = haversine_distance(lat, lon, float(point["lat"]), float(point["lon"]))
            if dist <= radius_km:
                results.append({**point, "distance_km": round(dist, 4)})
        results.sort(key=lambda p: p["distance_km"])
        return results

    def bbox(
        self,
        min_lat: float,
        min_lon: float,
        max_lat: float,
        max_lon: float,
    ) -> list[dict]:
        """
        Return all points inside the given bounding box.

        Args:
            min_lat: Southern boundary latitude.
            min_lon: Western boundary longitude.
            max_lat: Northern boundary latitude.
            max_lon: Eastern boundary longitude.
        """
        return [
            p for p in self._points
            if min_lat <= float(p["lat"]) <= max_lat
            and min_lon <= float(p["lon"]) <= max_lon
        ]

    def nearest(self, lat: float, lon: float, n: int = 1) -> list[dict]:
        """
        Return the *n* closest points to (lat, lon).
        """
        scored = [
            {**p, "distance_km": round(haversine_distance(lat, lon, float(p["lat"]), float(p["lon"])), 4)}
            for p in self._points
        ]
        scored.sort(key=lambda p: p["distance_km"])
        return scored[:n]
