"""Raleigh CivicPulse API: deterministic stop–flood-hazard screening."""

import json
import math
import os

import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from shapely.geometry import Point, shape

from app.ingest import FLOOD_SOURCE, STOP_SOURCE, load_demo_layers

GEMMA_URL = "https://inference.do-ai.run/v1/chat/completions"
GEMMA_MODEL = "gemma-4-31B-it"

app = FastAPI(title="Raleigh CivicPulse API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
DATA_DIR = "data"
# Configuration for DigitalOcean Serverless Inference
GEMMA_API_URL = os.getenv("GEMMA_API_URL", "https://api.digitalocean.com/v1/inference/gemma4")
GEMMA_API_KEY = os.getenv("GEMMA_API_KEY", "placeholder_key")
=======
>>>>>>> c482dd050660ff645084c23f82df7714c8dc9f8f

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


def generate_gemma_brief(result):
    """Interpret a verified join; the model never computes the spatial result."""
    if not result["findings"]:
        return result["ai_brief"]
    key = os.getenv("GEMMA_API_KEY")
    if not key:
        return "Gemma unavailable: set the server's GEMMA_API_KEY model access key."

    evidence = {
        "findings": result["findings"],
        "source_records": result["source_records"],
        "limitations": result["limitations"],
    }
    try:
        response = requests.post(
            GEMMA_URL,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": GEMMA_MODEL,
                "messages": [
                    {"role": "system", "content": (
                        "Draft a concise Transit–Stormwater inspection handoff using only "
                        "the supplied evidence. Cite stop and flood-area IDs. Distinguish "
                        "mapped hazard from observed flooding. Do not invent service impact "
                        "or current field conditions. State what staff should verify on site. "
                        "Keep the brief under 130 words."
                    )},
                    {"role": "user", "content": json.dumps(evidence)},
                ],
                "temperature": 0.1,
                "max_completion_tokens": 250,
            },
            timeout=25,
        )
        response.raise_for_status()
        brief = response.json()["choices"][0]["message"]["content"]
        if not isinstance(brief, str) or not brief.strip():
            raise ValueError("empty model response")
        return brief.strip()
    except (requests.RequestException, KeyError, IndexError, ValueError):
        return "Gemma unavailable: inference request failed; spatial evidence remains valid."


@app.get("/")
async def root():
    return {"message": "Raleigh CivicPulse API is running"}

<<<<<<< HEAD
@app.get("/layers")
=======

@app.get("/api/layers")
>>>>>>> c482dd050660ff645084c23f82df7714c8dc9f8f
async def get_layers():
    layers = current_layers()
    return {
        "bus_stops": layers["bus_stops"],
        "flood_zones": layers["flood_zones"],
    }


@app.get("/query")
async def query_location(lat: float, lon: float, buffer_m: float = 100):
<<<<<<< HEAD
    point = Point(lon, lat)
    buffer_deg = buffer_m / 111000.0
    search_area = point.buffer(buffer_deg)
    
    results = {
        "finding_id": f"find-{int(lat*1000)}-{int(lon*1000)}",
        "analysis_type": "spatial_overlap",
        "location": {"lat": lat, "lon": lon},
        "layers": [],
        "observations": [],
        "source_records": [],
        "findings": []
    }
    
    datasets = {
        "flood_zones": "flood_zones.geojson",
        "bus_routes": "bus_routes.geojson"
    }
    
    for layer_name, filename in datasets.items():
        gdf = load_geojson(filename)
        if gdf is not None:
            intersecting = gdf[gdf.intersects(search_area)]
            if not intersecting.empty:
                results["layers"].append(layer_name)
                results["observations"].append(f"Found {len(intersecting)} features in {layer_name} within {buffer_m}m.")
                    for idx, row in intersecting.iterrows():
                        rec_id = row.get('id', f"{layer_name}-{idx}")
                        # Convert geometry to WKT or JSON to avoid serialization errors
                        props = row.to_dict()
                        if 'geometry' in props:
                            props['geometry'] = props['geometry'].wkt if hasattr(props['geometry'], 'wkt') else str(props['geometry'])
                        
                        results["source_records"].append({
                            "id": rec_id,
                            "layer": layer_name,
                            "properties": props
                        })
                results["findings"].append({
                    "layer": layer_name,
                    "count": len(intersecting),
                    "data": json.loads(intersecting.to_json())
                })
                
    # Integrate Interpretation Agent
    results["ai_brief"] = await generate_ai_brief(results)
                
    return results
=======
    if not all(map(math.isfinite, (lat, lon, buffer_m))):
        raise HTTPException(status_code=400, detail="Coordinates and buffer must be finite")
    if not (-90 <= lat <= 90 and -180 <= lon <= 180 and 1 <= buffer_m <= 500):
        raise HTTPException(status_code=400, detail="Invalid coordinates or buffer")
    result = find_stop_flood_overlaps(lat, lon, buffer_m, current_layers())
    result["ai_brief"] = generate_gemma_brief(result)
    result["ai_model"] = GEMMA_MODEL if result["findings"] else None
    return result
>>>>>>> c482dd050660ff645084c23f82df7714c8dc9f8f
