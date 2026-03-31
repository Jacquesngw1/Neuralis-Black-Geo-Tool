"""Tests for neuralis.geo.geocoder"""

import math
import pytest

from neuralis.geo.geocoder import haversine_distance, Geocoder


class TestHaversineDistance:
    def test_same_point(self):
        assert haversine_distance(0, 0, 0, 0) == 0.0

    def test_known_distance(self):
        # London (51.5074, -0.1278) to Paris (48.8566, 2.3522) ≈ 340 km
        dist = haversine_distance(51.5074, -0.1278, 48.8566, 2.3522)
        assert 330 < dist < 350

    def test_symmetry(self):
        d1 = haversine_distance(40.0, -74.0, 48.0, 2.0)
        d2 = haversine_distance(48.0, 2.0, 40.0, -74.0)
        assert math.isclose(d1, d2, rel_tol=1e-9)

    def test_positive(self):
        assert haversine_distance(0, 0, 1, 1) > 0


class TestGeocoderInit:
    def test_valid_provider(self):
        gc = Geocoder(provider="nominatim")
        assert gc.provider == "nominatim"

    def test_invalid_provider(self):
        with pytest.raises(ValueError, match="Unknown provider"):
            Geocoder(provider="invalid_xyz")
