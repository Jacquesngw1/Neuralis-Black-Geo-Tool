"""
classifier.py — Rule-based and heuristic geographic entity classifier.

Classifies points of interest into high-level categories based on
OSM tags, name keywords, and other available metadata.
"""

from __future__ import annotations

# Keyword maps for category detection
_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "infrastructure": [
        "airport", "port", "harbour", "railway", "station", "highway",
        "bridge", "tunnel", "power", "substation", "dam", "pipeline",
    ],
    "commercial": [
        "mall", "market", "shop", "store", "retail", "supermarket",
        "plaza", "shopping", "bank", "office", "business",
    ],
    "industrial": [
        "factory", "plant", "warehouse", "refinery", "mine", "quarry",
        "industrial", "manufacturing", "depot", "terminal",
    ],
    "residential": [
        "residential", "suburb", "neighborhood", "neighbourhood",
        "housing", "apartment", "villa", "estate",
    ],
    "government": [
        "embassy", "consulate", "government", "parliament", "ministry",
        "city hall", "courthouse", "police", "military", "barracks",
    ],
    "education": [
        "school", "university", "college", "academy", "institute",
        "campus", "library",
    ],
    "healthcare": [
        "hospital", "clinic", "pharmacy", "medical", "health",
        "emergency", "ambulance",
    ],
    "natural": [
        "park", "forest", "mountain", "lake", "river", "beach",
        "coast", "island", "valley", "desert", "wetland",
    ],
}

_DEFAULT_CONFIDENCE = 0.60
_KEYWORD_CONFIDENCE = 0.85


class GeoClassifier:
    """
    Classifies geographic entities into semantic categories.

    The default implementation uses keyword matching against
    name and tag fields.  Subclass and override `classify_one`
    to plug in a real neural model.
    """

    def classify(self, points: list[dict]) -> list[dict]:
        """
        Classify a list of geographic point dicts.

        Each point should have at least a 'name' or 'address' field.
        Returns a copy of each point with 'category' and 'confidence' keys added.
        """
        return [self.classify_one(p) for p in points]

    def classify_one(self, point: dict) -> dict:
        """Classify a single point dict and return it with classification metadata."""
        text = " ".join(str(v) for v in point.values()).lower()
        for category, keywords in _CATEGORY_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return {**point, "category": category, "confidence": _KEYWORD_CONFIDENCE}
        return {**point, "category": "unknown", "confidence": _DEFAULT_CONFIDENCE}
