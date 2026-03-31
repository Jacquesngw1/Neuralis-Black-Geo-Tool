"""Tests for neuralis.export.exporter"""

import json
import os
import tempfile

import pytest

from neuralis.export.exporter import Exporter

SAMPLE = [
    {"lat": 48.8566, "lon": 2.3522, "name": "Paris", "country": "France"},
    {"lat": 51.5074, "lon": -0.1278, "name": "London", "country": "UK"},
]


class TestExporter:
    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.exp = Exporter(output_dir=self.tmpdir)

    def test_geojson_structure(self):
        path = self.exp.to_geojson(SAMPLE)
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        assert data["type"] == "FeatureCollection"
        assert len(data["features"]) == 2
        feat = data["features"][0]
        assert feat["geometry"]["type"] == "Point"
        assert feat["geometry"]["coordinates"] == [2.3522, 48.8566]

    def test_kml_written(self):
        path = self.exp.to_kml(SAMPLE)
        assert os.path.exists(path)
        content = open(path, encoding="utf-8").read()
        assert "Paris" in content
        assert "<kml" in content

    def test_csv_written(self):
        import csv
        path = self.exp.to_csv(SAMPLE)
        assert os.path.exists(path)
        with open(path, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert len(rows) == 2
        assert rows[0]["name"] == "Paris"

    def test_geojson_custom_path(self):
        custom_path = os.path.join(self.tmpdir, "custom.geojson")
        path = self.exp.to_geojson(SAMPLE, output_path=custom_path)
        assert path == custom_path
        assert os.path.exists(custom_path)

    def test_csv_empty(self):
        path = self.exp.to_csv([])
        assert os.path.exists(path)
