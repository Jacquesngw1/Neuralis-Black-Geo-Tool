"""
renderer.py — Map and heatmap rendering using Folium (optional dependency).

If Folium is not installed the module degrades gracefully: text-based
coordinate summaries are returned instead of interactive maps.
"""

from __future__ import annotations

import json
import os
from typing import Sequence


def _try_import_folium():
    try:
        import folium  # noqa: F401
        return folium
    except ImportError:
        return None


class MapRenderer:
    """
    Render geographic points as interactive HTML maps or plain summaries.
    """

    def __init__(self, zoom_start: int = 10):
        self.zoom_start = zoom_start

    def render_html(self, points: Sequence[dict], output_path: str) -> str:
        """
        Generate an interactive Folium HTML map and save it to *output_path*.

        Falls back to a JSON summary file if Folium is unavailable.

        Returns the path of the generated file.
        """
        folium = _try_import_folium()
        if folium is None:
            return self._render_json_fallback(points, output_path)

        if not points:
            raise ValueError("No points provided to render.")

        center_lat = sum(float(p["lat"]) for p in points) / len(points)
        center_lon = sum(float(p["lon"]) for p in points) / len(points)

        m = folium.Map(location=[center_lat, center_lon], zoom_start=self.zoom_start, tiles="CartoDB Dark_Matter")
        for point in points:
            popup_text = point.get("address") or point.get("name") or f"{point['lat']}, {point['lon']}"
            folium.CircleMarker(
                location=[float(point["lat"]), float(point["lon"])],
                radius=6,
                color="#00ff99",
                fill=True,
                fill_opacity=0.8,
                popup=popup_text,
            ).add_to(m)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        m.save(output_path)
        return output_path

    def render_heatmap(self, points: Sequence[dict], output_path: str) -> str:
        """
        Generate a heatmap HTML file.

        Returns the path of the generated file.
        """
        folium = _try_import_folium()
        if folium is None:
            return self._render_json_fallback(points, output_path)

        from folium.plugins import HeatMap  # type: ignore[import]
        center_lat = sum(float(p["lat"]) for p in points) / len(points)
        center_lon = sum(float(p["lon"]) for p in points) / len(points)
        m = folium.Map(location=[center_lat, center_lon], zoom_start=self.zoom_start, tiles="CartoDB Dark_Matter")
        heat_data = [[float(p["lat"]), float(p["lon"])] for p in points]
        HeatMap(heat_data).add_to(m)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        m.save(output_path)
        return output_path

    # ------------------------------------------------------------------

    @staticmethod
    def _render_json_fallback(points: Sequence[dict], output_path: str) -> str:
        fallback_path = output_path.replace(".html", ".json")
        os.makedirs(os.path.dirname(os.path.abspath(fallback_path)), exist_ok=True)
        with open(fallback_path, "w", encoding="utf-8") as fh:
            json.dump(list(points), fh, indent=2)
        return fallback_path
