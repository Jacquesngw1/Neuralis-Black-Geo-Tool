"""
geocoder.py — Forward and reverse geocoding using multiple providers.

Supported providers:
  - nominatim (default, no API key required)
  - google    (requires API key)
  - here      (requires API key)
"""

import math
import urllib.parse
import urllib.request
import json
from typing import Optional


class GeocoderError(Exception):
    """Raised when a geocoding request fails."""


class Geocoder:
    """Forward and reverse geocoder supporting multiple backend providers."""

    PROVIDERS = ("nominatim", "google", "here")
    _NOMINATIM_BASE = "https://nominatim.openstreetmap.org"

    def __init__(self, provider: str = "nominatim", api_key: str = "", timeout: int = 10):
        if provider not in self.PROVIDERS:
            raise ValueError(f"Unknown provider '{provider}'. Choose from: {self.PROVIDERS}")
        self.provider = provider
        self.api_key = api_key
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def forward(self, address: str) -> dict:
        """
        Convert a human-readable address to geographic coordinates.

        Args:
            address: The address string to geocode.

        Returns:
            A dict with keys: address, lat, lon, raw.
        """
        if self.provider == "nominatim":
            return self._nominatim_forward(address)
        raise NotImplementedError(f"Forward geocoding not implemented for provider '{self.provider}'")

    def reverse(self, lat: float, lon: float) -> dict:
        """
        Convert geographic coordinates to a human-readable address.

        Args:
            lat: Latitude in decimal degrees.
            lon: Longitude in decimal degrees.

        Returns:
            A dict with keys: address, lat, lon, raw.
        """
        if self.provider == "nominatim":
            return self._nominatim_reverse(lat, lon)
        raise NotImplementedError(f"Reverse geocoding not implemented for provider '{self.provider}'")

    # ------------------------------------------------------------------
    # Nominatim implementation
    # ------------------------------------------------------------------

    def _nominatim_forward(self, address: str) -> dict:
        params = urllib.parse.urlencode({
            "q": address,
            "format": "json",
            "limit": 1,
        })
        url = f"{self._NOMINATIM_BASE}/search?{params}"
        data = self._fetch_json(url)
        if not data:
            raise GeocoderError(f"No results found for address: '{address}'")
        hit = data[0]
        return {
            "address": hit.get("display_name", ""),
            "lat": float(hit["lat"]),
            "lon": float(hit["lon"]),
            "raw": hit,
        }

    def _nominatim_reverse(self, lat: float, lon: float) -> dict:
        params = urllib.parse.urlencode({
            "lat": lat,
            "lon": lon,
            "format": "json",
        })
        url = f"{self._NOMINATIM_BASE}/reverse?{params}"
        data = self._fetch_json(url)
        if "error" in data:
            raise GeocoderError(data["error"])
        return {
            "address": data.get("display_name", ""),
            "lat": float(data["lat"]),
            "lon": float(data["lon"]),
            "raw": data,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _fetch_json(self, url: str) -> dict | list:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Neuralis-Black-Geo-Tool/0.1"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # nosec B310
            return json.loads(resp.read().decode())


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance (km) between two points on Earth.

    Args:
        lat1, lon1: Coordinates of point 1 (decimal degrees).
        lat2, lon2: Coordinates of point 2 (decimal degrees).

    Returns:
        Distance in kilometres.
    """
    R = 6371.0  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
