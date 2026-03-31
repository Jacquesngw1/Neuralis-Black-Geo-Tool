"""
cli.py — Command-line interface for Neuralis Black Geo Tool.

Usage:
    python -m neuralis.cli <command> [options]

Commands:
    geocode   Reverse geocode a lat/lon coordinate
    search    Forward geocode an address or place name
    ip        Geolocate an IP address
    query     Radius query around a coordinate
    cluster   Cluster a CSV file of coordinates
"""

from __future__ import annotations

import argparse
import json
import sys

from neuralis.geo.geocoder import Geocoder, GeocoderError


def cmd_geocode(args: argparse.Namespace) -> None:
    gc = Geocoder()
    result = gc.reverse(lat=args.lat, lon=args.lon)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_search(args: argparse.Namespace) -> None:
    gc = Geocoder()
    result = gc.forward(address=args.query)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_ip(args: argparse.Namespace) -> None:
    import urllib.request
    import urllib.parse

    url = f"http://ip-api.com/json/{urllib.parse.quote(args.target)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Neuralis-Black-Geo-Tool/0.1"})
    with urllib.request.urlopen(req, timeout=10) as resp:  # nosec B310
        data = json.loads(resp.read().decode())
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_query(args: argparse.Namespace) -> None:
    from neuralis.geo.query import SpatialQuery

    # Demo: query against an empty dataset (user should load their own data)
    sq = SpatialQuery()
    print(json.dumps({
        "message": "Radius query ready. Load points via the Python API.",
        "center": {"lat": args.lat, "lon": args.lon},
        "radius_km": args.radius,
        "results": sq.radius(args.lat, args.lon, args.radius),
    }, indent=2))


def cmd_cluster(args: argparse.Namespace) -> None:
    import csv
    from neuralis.geo.cluster import KMeansGeo
    from neuralis.export.exporter import Exporter

    with open(args.input, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        points = list(reader)

    kmeans = KMeansGeo(k=args.k)
    labels = kmeans.fit(points)
    for i, point in enumerate(points):
        point["cluster"] = labels[i]

    exporter = Exporter()
    fmt = (args.export or "csv").lower()
    if fmt == "geojson":
        path = exporter.to_geojson(points)
    elif fmt == "kml":
        path = exporter.to_kml(points)
    else:
        path = exporter.to_csv(points)
    print(f"Exported {len(points)} points to: {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="neuralis",
        description="Neuralis Black Geo Tool — Geographic Intelligence Toolkit",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # geocode
    p_gc = sub.add_parser("geocode", help="Reverse geocode a coordinate")
    p_gc.add_argument("--lat", type=float, required=True, help="Latitude")
    p_gc.add_argument("--lon", type=float, required=True, help="Longitude")

    # search
    p_search = sub.add_parser("search", help="Forward geocode an address")
    p_search.add_argument("--query", required=True, help="Place name or address")

    # ip
    p_ip = sub.add_parser("ip", help="Geolocate an IP address")
    p_ip.add_argument("--target", required=True, help="IP address to look up")

    # query
    p_query = sub.add_parser("query", help="Radius query around a coordinate")
    p_query.add_argument("--lat", type=float, required=True)
    p_query.add_argument("--lon", type=float, required=True)
    p_query.add_argument("--radius", type=float, default=10.0, help="Radius in km")

    # cluster
    p_cluster = sub.add_parser("cluster", help="Cluster a CSV of coordinates")
    p_cluster.add_argument("--input", required=True, help="Path to input CSV")
    p_cluster.add_argument("--k", type=int, default=5, help="Number of clusters")
    p_cluster.add_argument("--export", choices=["csv", "geojson", "kml"], default="csv")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    dispatch = {
        "geocode": cmd_geocode,
        "search": cmd_search,
        "ip": cmd_ip,
        "query": cmd_query,
        "cluster": cmd_cluster,
    }
    try:
        dispatch[args.command](args)
    except GeocoderError as exc:
        print(f"[ERROR] Geocoder: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
