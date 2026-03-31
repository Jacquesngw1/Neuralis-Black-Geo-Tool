"""Tests for neuralis.geo.query"""

import pytest

from neuralis.geo.query import SpatialQuery

SAMPLE_POINTS = [
    {"lat": 48.8566, "lon": 2.3522, "name": "Paris"},
    {"lat": 51.5074, "lon": -0.1278, "name": "London"},
    {"lat": 52.5200, "lon": 13.4050, "name": "Berlin"},
    {"lat": 40.7128, "lon": -74.0060, "name": "New York"},
    {"lat": 35.6762, "lon": 139.6503, "name": "Tokyo"},
]


class TestSpatialQuery:
    def setup_method(self):
        self.sq = SpatialQuery(SAMPLE_POINTS)

    def test_radius_all_near_paris(self):
        # Radius that includes only Paris itself (< 1 km)
        results = self.sq.radius(48.8566, 2.3522, 1.0)
        assert len(results) == 1
        assert results[0]["name"] == "Paris"

    def test_radius_includes_multiple(self):
        # Very large radius should return all points
        results = self.sq.radius(48.8566, 2.3522, 15000)
        assert len(results) == len(SAMPLE_POINTS)

    def test_radius_sorted_by_distance(self):
        results = self.sq.radius(48.8566, 2.3522, 15000)
        distances = [r["distance_km"] for r in results]
        assert distances == sorted(distances)

    def test_bbox_single(self):
        # Tight box around Paris
        results = self.sq.bbox(48.0, 2.0, 49.0, 3.0)
        assert len(results) == 1
        assert results[0]["name"] == "Paris"

    def test_bbox_empty(self):
        results = self.sq.bbox(0, 0, 1, 1)
        assert results == []

    def test_nearest_one(self):
        results = self.sq.nearest(48.8566, 2.3522, n=1)
        assert len(results) == 1
        assert results[0]["name"] == "Paris"

    def test_nearest_two(self):
        results = self.sq.nearest(48.8566, 2.3522, n=2)
        assert len(results) == 2
        # Paris should be closest to itself, London is next
        assert results[0]["name"] == "Paris"

    def test_load_replaces_points(self):
        self.sq.load([{"lat": 0.0, "lon": 0.0, "name": "Origin"}])
        results = self.sq.radius(0.0, 0.0, 1.0)
        assert len(results) == 1
        assert results[0]["name"] == "Origin"
