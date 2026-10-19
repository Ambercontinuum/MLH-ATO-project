"""Raleigh CivicPulse API: deterministic stop–flood-hazard screening."""

import math

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from shapely.geometry import Point, shape

from app.ingest import FLOOD_SOURCE, STOP_SOURCE, load_demo_layers

app = FastAPI(title="Raleigh CivicPulse API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def distance_m(lat1, lon1, lat2, lon2):
    """Great-circle distance between WGS84 coordinates, in metres."""
    radius_m = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * radius_m * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def find_stop_flood_overlaps(lat, lon, buffer_m, layers):
    """Select nearby stop points, then test each point against hazard polygons."""
    results = {
        "finding_id": f"stop-flood-{lat:.6f}-{lon:.6f}",
        "analysis_type": "stop_point_in_flood_polygon",
        "location": {"lat": lat, "lon": lon},
        "buffer_m": buffer_m,
        "layers": [],
        "observations": [],
        "source_records": [],
        "findings": [],
        "source_queries": layers["source_queries"],
        "limitations": (
            "Mapped flood hazard is a screening layer, not observed flooding or "
            "a service-disruption report. Transit and Stormwater must verify "
            "conditions and pedestrian access in the field."
        ),
    }

    nearby_stops = []
    for stop in layers["bus_stops"]["features"]:
        geometry = stop.get("geometry") or {}
        if geometry.get("type") != "Point":
            continue
        stop_lon, stop_lat = geometry["coordinates"][:2]
        metres = distance_m(lat, lon, stop_lat, stop_lon)
        if metres > buffer_m:
            continue

        nearby_stops.append((metres, stop))

    # A click inspects the closest stop; nearby stops may have different context.
    for metres, stop in [min(nearby_stops, key=lambda item: item[0])] if nearby_stops else []:
        stop_lon, stop_lat = stop["geometry"]["coordinates"][:2]

        stop_point = Point(stop_lon, stop_lat)
        stop_props = stop.get("properties") or {}
        for flood in layers["flood_zones"]["features"]:
            flood_geometry = flood.get("geometry")
            if not flood_geometry or not shape(flood_geometry).covers(stop_point):
                continue

            flood_props = flood.get("properties") or {}
            stop_id = stop_props.get("Stop_ID")
            flood_id = flood_props.get("FLD_AR_ID")
            zone = flood_props.get("FLD_ZONE")
            results["findings"].append({
                "layer": "stop_flood_overlap",
                "count": 1,
                "stop_id": stop_id,
                "flood_area_id": flood_id,
                "flood_zone": zone,
                "method": "WGS84 stop point covered by mapped hazard polygon",
                "click_distance_m": round(metres, 1),
            })
            results["observations"].append(
                f"Stop {stop_id} lies within mapped flood-hazard area "
                f"{flood_id} (zone {zone})."
            )
            results["source_records"].extend([
                {
                    "id": stop_id,
                    "layer": "bus_stops",
                    "properties": stop_props,
                    "source_url": STOP_SOURCE,
                },
                {
                    "id": flood_id,
                    "layer": "flood_zones",
                    "properties": flood_props,
                    "source_url": FLOOD_SOURCE,
                },
            ])

    if results["findings"]:
        results["layers"] = ["bus_stops", "flood_zones"]
        results["ai_brief"] = (
            "Verified map overlap. Gemma briefing is pending API integration. "
            + results["limitations"]
        )
    else:
        results["ai_brief"] = (
            f"No mapped stop–flood-hazard overlap found within {buffer_m:g} m "
            "of this click in the demo area."
        )
    return results


def current_layers():
    try:
        return load_demo_layers()
    except (OSError, ValueError, RuntimeError) as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Public GIS source unavailable: {exc}",
        ) from exc


@app.get("/")
async def root():
    return {"message": "Raleigh CivicPulse API is running"}


@app.get("/api/layers")
async def get_layers():
    layers = current_layers()
    return {
        "bus_stops": layers["bus_stops"],
        "flood_zones": layers["flood_zones"],
    }


@app.get("/api/query")
async def query_location(lat: float, lon: float, buffer_m: float = 100):
    if not all(map(math.isfinite, (lat, lon, buffer_m))):
        raise HTTPException(status_code=400, detail="Coordinates and buffer must be finite")
    if not (-90 <= lat <= 90 and -180 <= lon <= 180 and 1 <= buffer_m <= 500):
        raise HTTPException(status_code=400, detail="Invalid coordinates or buffer")
    return find_stop_flood_overlaps(lat, lon, buffer_m, current_layers())
