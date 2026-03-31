# Neuralis Black Geo Tool

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A powerful geospatial intelligence and analysis tool that combines neural-network-based processing with geographic data visualization and location analytics. **Neuralis Black Geo Tool** is designed for analysts, researchers, and developers who need to process, query, and visualize geographic information with AI-enhanced capabilities.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Modules](#modules)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Neuralis Black Geo Tool is a command-line and API-driven geospatial toolkit that enables:

- **Location Intelligence** — reverse geocoding, coordinate lookup, and place enrichment
- **Geospatial Querying** — bounding box searches, radius queries, and polygon intersection
- **Neural Data Enrichment** — AI-powered classification and tagging of geographic entities
- **Visualization** — map generation, heatmaps, and geographic cluster rendering
- **Data Export** — GeoJSON, KML, CSV, and Shapefile output support

The "Black" edition introduces an enhanced dark-themed interface for terminal/CLI use and includes advanced OSINT (Open Source Intelligence) geo-enrichment pipelines.

---

## Features

| Feature | Description |
|---|---|
| 🌍 Coordinate Lookup | Forward/reverse geocoding using multiple providers |
| 🔍 Location Search | Search and enrich location data by name or coordinates |
| 🧠 Neural Classification | AI-based categorization of geographic points of interest |
| 🗺️ Map Rendering | Generate static or interactive map outputs |
| 📡 IP Geolocation | Resolve IP addresses to geographic locations |
| 📊 Cluster Analysis | DBSCAN/K-Means clustering on geographic data sets |
| 🔒 OSINT Integration | Passive geo-enrichment from open data sources |
| 📁 Multi-format Export | Export results as GeoJSON, KML, CSV, or Shapefile |

---

## Project Structure

```
Neuralis-Black-Geo-Tool/
├── neuralis/                  # Core package
│   ├── __init__.py
│   ├── geo/                   # Geospatial processing modules
│   │   ├── __init__.py
│   │   ├── geocoder.py        # Forward/reverse geocoding
│   │   ├── query.py           # Spatial queries (radius, bbox, polygon)
│   │   └── cluster.py         # Geographic clustering algorithms
│   ├── neural/                # AI/ML enrichment modules
│   │   ├── __init__.py
│   │   └── classifier.py      # Neural classification of geo entities
│   ├── osint/                 # OSINT enrichment pipelines
│   │   ├── __init__.py
│   │   └── enricher.py        # Open-source geo-intelligence enrichment
│   ├── viz/                   # Visualization and map rendering
│   │   ├── __init__.py
│   │   └── renderer.py        # Map and heatmap rendering
│   ├── export/                # Data export utilities
│   │   ├── __init__.py
│   │   └── exporter.py        # GeoJSON, KML, CSV, Shapefile export
│   └── cli.py                 # Command-line interface entry point
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_geocoder.py
│   ├── test_query.py
│   └── test_cluster.py
├── config/
│   └── settings.yaml          # Default configuration
├── requirements.txt           # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### Install from source

```bash
git clone https://github.com/Jacquesngw1/Neuralis-Black-Geo-Tool.git
cd Neuralis-Black-Geo-Tool
pip install -r requirements.txt
```

### Optional: create a virtual environment first

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### Command-Line Interface

```bash
# Reverse geocode a coordinate
python -m neuralis.cli geocode --lat 40.7128 --lon -74.0060

# Search for a location by name
python -m neuralis.cli search --query "Eiffel Tower, Paris"

# Resolve an IP address to a location
python -m neuralis.cli ip --target 8.8.8.8

# Run a radius query (all points within 10 km of a coordinate)
python -m neuralis.cli query --lat 48.8566 --lon 2.3522 --radius 10

# Cluster a CSV file of coordinates and export the result
python -m neuralis.cli cluster --input data/points.csv --export geojson
```

### Python API

```python
from neuralis.geo.geocoder import Geocoder
from neuralis.geo.query import SpatialQuery
from neuralis.export.exporter import Exporter

# Reverse geocode
geocoder = Geocoder()
result = geocoder.reverse(lat=40.7128, lon=-74.0060)
print(result)

# Radius query
query = SpatialQuery()
points = query.radius(lat=48.8566, lon=2.3522, radius_km=5)

# Export to GeoJSON
exporter = Exporter()
exporter.to_geojson(points, output_path="results.geojson")
```

---

## Configuration

Edit `config/settings.yaml` to set your API keys and preferences:

```yaml
geocoding:
  provider: nominatim          # nominatim | google | here
  api_key: ""                  # Required for google/here providers
  timeout: 10

ip_geolocation:
  provider: ip-api              # ip-api | ipinfo
  api_key: ""

neural:
  model: default
  confidence_threshold: 0.75

export:
  default_format: geojson
  output_dir: ./output
```

---

## Modules

### `neuralis.geo.geocoder`
Handles forward and reverse geocoding. Supports Nominatim (OpenStreetMap), Google Maps, and HERE geocoding APIs.

### `neuralis.geo.query`
Performs spatial queries including bounding box searches, radius queries (Haversine formula), and polygon intersection checks.

### `neuralis.geo.cluster`
Implements geographic clustering using DBSCAN and K-Means algorithms. Accepts CSV or GeoJSON inputs.

### `neuralis.neural.classifier`
AI-powered classification of geographic points of interest into categories (e.g., infrastructure, residential, commercial, industrial).

### `neuralis.osint.enricher`
Passive geo-intelligence enrichment using open data sources. Attaches metadata (country info, timezone, language, risk tags) to geographic entities.

### `neuralis.viz.renderer`
Generates static maps (PNG/SVG) and interactive HTML maps using Folium/Leaflet. Supports heatmaps and cluster visualizations.

### `neuralis.export.exporter`
Exports processed geographic data to GeoJSON, KML, CSV, or ESRI Shapefile formats.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

Please ensure all new code includes appropriate tests.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Neuralis Black Geo Tool — Geographic Intelligence, Powered by Neural Processing.*