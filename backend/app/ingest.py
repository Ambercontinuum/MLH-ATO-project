"""Fetch the two public GeoJSON layers used for the Raleigh demo area."""

from functools import lru_cache

import requests

STOP_SERVICE = (
    "https://services.arcgis.com/v400IkDOw1ad7Yad/arcgis/rest/services/"
    "GoRaleigh_BusStops/FeatureServer/0/query"
)
FLOOD_SERVICE = (
    "https://services5.arcgis.com/7weheFjxuNkGGiZi/arcgis/rest/services/"
    "USA_Flood_Hazard_Areas_view/FeatureServer/0/query"
)
STOP_SOURCE = "https://data-ral.opendata.arcgis.com/datasets/goraleigh-bus-stops-1/explore"
FLOOD_SOURCE = "https://www.arcgis.com/home/item.html?id=ccd29fb4bd5e4b44a2d61638829a5d7e"

# Compact area around the verified stop 8099. Expand only after checking service limits.
DEMO_BBOX = "-78.65,35.80,-78.60,35.83"
COMMON_PARAMS = {
    "geometry": DEMO_BBOX,
    "geometryType": "esriGeometryEnvelope",
    "inSR": 4326,
    "spatialRel": "esriSpatialRelIntersects",
    "outSR": 4326,
    "f": "geojson",
}


def fetch_layer(service, *, where, fields):
    params = {**COMMON_PARAMS, "where": where, "outFields": fields}
    response = requests.get(service, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    if data.get("type") != "FeatureCollection" or not isinstance(data.get("features"), list):
        raise ValueError(f"Expected GeoJSON FeatureCollection from {service}")
    if not data["features"]:
        raise ValueError(f"Source returned no features: {response.url}")
    return data, response.url


@lru_cache(maxsize=1)
def load_demo_layers():
    """Cache source data per process; never substitute the synthetic repo fixtures."""
    stops, stop_query = fetch_layer(
        STOP_SERVICE,
        where="1=1",
        fields="Stop_ID,Stop_Name,R2,ADA_Compliant,Status,EditDate",
    )
    flood, flood_query = fetch_layer(
        FLOOD_SERVICE,
        where="SFHA_TF='T'",
        fields="OBJECTID,FLD_AR_ID,FLD_ZONE,SFHA_TF,SOURCE_CIT",
    )
    return {
        "bus_stops": stops,
        "flood_zones": flood,
        "source_queries": {"bus_stops": stop_query, "flood_zones": flood_query},
    }
