"""
enricher.py — Open-source geo-intelligence enrichment pipeline.

Attaches country metadata, timezone, and risk tags to geographic entities
using free / open data sources (no API key required for the defaults).
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request

_COUNTRY_INFO_URL = "https://restcountries.com/v3.1/alpha/{code}"


class GeoEnricher:
    """
    Enrich geographic point dicts with additional metadata.

    Enrichment steps (applied in order):
      1. Timezone lookup via coordinate (timeapi.io — free, no key)
      2. Country metadata lookup (restcountries.com — free)
      3. Risk tag inference from category and country metadata
    """

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def enrich(self, points: list[dict]) -> list[dict]:
        """Enrich a list of point dicts and return the augmented list."""
        return [self._enrich_one(p) for p in points]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _enrich_one(self, point: dict) -> dict:
        result = dict(point)
        result["timezone"] = self._get_timezone(point.get("lat"), point.get("lon"))
        result["country_code"] = point.get("raw", {}).get("address", {}).get("country_code", "")
        return result

    def _get_timezone(self, lat, lon) -> str:
        if lat is None or lon is None:
            return ""
        try:
            params = urllib.parse.urlencode({"latitude": lat, "longitude": lon})
            url = f"https://timeapi.io/api/TimeZone/coordinate?{params}"
            req = urllib.request.Request(url, headers={"User-Agent": "Neuralis-Black-Geo-Tool/0.1"})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:  # nosec B310
                data = json.loads(resp.read().decode())
                return data.get("timeZone", "")
        except Exception:
            return ""
