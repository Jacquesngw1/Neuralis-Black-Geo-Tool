"""Tests for neuralis.geo.cluster and neuralis.neural.classifier"""

import pytest

from neuralis.geo.cluster import KMeansGeo
from neuralis.neural.classifier import GeoClassifier

CITY_POINTS = [
    {"lat": 48.8566, "lon": 2.3522, "name": "Paris"},
    {"lat": 48.9000, "lon": 2.4000, "name": "Pantin"},
    {"lat": 51.5074, "lon": -0.1278, "name": "London"},
    {"lat": 51.4800, "lon": -0.1000, "name": "Lambeth"},
    {"lat": 52.5200, "lon": 13.4050, "name": "Berlin"},
    {"lat": 52.5300, "lon": 13.3800, "name": "Mitte"},
]


class TestKMeansGeo:
    def test_basic_clustering(self):
        km = KMeansGeo(k=3, seed=42)
        labels = km.fit(CITY_POINTS)
        assert len(labels) == len(CITY_POINTS)

    def test_labels_in_range(self):
        km = KMeansGeo(k=3, seed=42)
        labels = km.fit(CITY_POINTS)
        assert all(0 <= lbl < 3 for lbl in labels)

    def test_centroids_generated(self):
        km = KMeansGeo(k=3, seed=42)
        km.fit(CITY_POINTS)
        assert len(km.centroids) == 3

    def test_too_few_points_raises(self):
        km = KMeansGeo(k=10)
        with pytest.raises(ValueError):
            km.fit(CITY_POINTS)  # only 6 points, k=10


class TestGeoClassifier:
    def setup_method(self):
        self.clf = GeoClassifier()

    def test_infrastructure_detection(self):
        point = {"name": "Heathrow Airport", "lat": 51.47, "lon": -0.45}
        result = self.clf.classify_one(point)
        assert result["category"] == "infrastructure"
        assert result["confidence"] > 0.5

    def test_commercial_detection(self):
        point = {"name": "Oxford Street Mall", "lat": 51.51, "lon": -0.13}
        result = self.clf.classify_one(point)
        assert result["category"] == "commercial"

    def test_unknown_category(self):
        point = {"name": "XYZ 123", "lat": 0.0, "lon": 0.0}
        result = self.clf.classify_one(point)
        assert result["category"] == "unknown"

    def test_classify_batch(self):
        points = [
            {"name": "City Hospital", "lat": 0.0, "lon": 0.0},
            {"name": "Central Park", "lat": 0.0, "lon": 0.0},
        ]
        results = self.clf.classify(points)
        assert len(results) == 2
        assert results[0]["category"] == "healthcare"
        assert results[1]["category"] == "natural"
