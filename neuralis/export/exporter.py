"""
exporter.py — Export geographic data to GeoJSON, KML, and CSV formats.
"""

from __future__ import annotations

import csv
import json
import os
from typing import Sequence


class Exporter:
    """Export geographic point collections to common geospatial formats."""

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # GeoJSON
    # ------------------------------------------------------------------

    def to_geojson(self, points: Sequence[dict], output_path: str | None = None) -> str:
        """
        Export *points* to a GeoJSON FeatureCollection file.

        Returns the path of the written file.
        """
        output_path = output_path or os.path.join(self.output_dir, "output.geojson")
        features = []
        for point in points:
            props = {k: v for k, v in point.items() if k not in ("lat", "lon", "raw")}
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(point["lon"]), float(point["lat"])],
                },
                "properties": props,
            })
        collection = {"type": "FeatureCollection", "features": features}
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(collection, fh, indent=2)
        return output_path

    # ------------------------------------------------------------------
    # KML
    # ------------------------------------------------------------------

    def to_kml(self, points: Sequence[dict], output_path: str | None = None) -> str:
        """
        Export *points* to a KML file (compatible with Google Earth).

        Returns the path of the written file.
        """
        output_path = output_path or os.path.join(self.output_dir, "output.kml")
        placemarks = "\n".join(self._kml_placemark(p) for p in points)
        kml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
            "  <Document>\n"
            f"{placemarks}\n"
            "  </Document>\n"
            "</kml>"
        )
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(kml)
        return output_path

    @staticmethod
    def _kml_placemark(point: dict) -> str:
        name = point.get("address") or point.get("name") or "Point"
        lat, lon = float(point["lat"]), float(point["lon"])
        return (
            "    <Placemark>\n"
            f"      <name>{name}</name>\n"
            "      <Point>\n"
            f"        <coordinates>{lon},{lat},0</coordinates>\n"
            "      </Point>\n"
            "    </Placemark>"
        )

    # ------------------------------------------------------------------
    # CSV
    # ------------------------------------------------------------------

    def to_csv(self, points: Sequence[dict], output_path: str | None = None) -> str:
        """
        Export *points* to a CSV file.

        Returns the path of the written file.
        """
        output_path = output_path or os.path.join(self.output_dir, "output.csv")
        if not points:
            with open(output_path, "w", encoding="utf-8") as fh:
                fh.write("")
            return output_path

        flat_points = [{k: v for k, v in p.items() if k != "raw"} for p in points]
        fieldnames = list(flat_points[0].keys())
        with open(output_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(flat_points)
        return output_path
