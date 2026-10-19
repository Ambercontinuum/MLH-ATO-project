from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import geopandas as gpd
from shapely.geometry import Point
import os
import json

app = FastAPI(title="Raleigh CivicPulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "backend/data"

def load_geojson(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return None
    return gpd.read_file(path)

@app.get("/")
async def root():
    return {"message": "Raleigh CivicPulse API is running"}

@app.get("/api/layers")
async def get_layers():
    layers = {}
    datasets = {
        "flood_zones": "flood_zones.geojson",
        "bus_routes": "bus_routes.geojson"
    }
    for layer_name, filename in datasets.items():
        gdf = load_geojson(filename)
        if gdf is not None:
            layers[layer_name] = json.loads(gdf.to_json())
    return layers

@app.get("/api/query")
async def query_location(lat: float, lon: float, buffer_m: float = 100):
    """
    Perform spatial intersection analysis to find overlapping data layers.
    """
    point = Point(lon, lat)
    # Approximation for buffer (0.001 deg ~ 111m)
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
                
                # Collect record IDs and properties for provenance
                for idx, row in intersecting.iterrows():
                    rec_id = row.get('id', f"{layer_name}-{idx}")
                    results["source_records"].append({
                        "id": rec_id,
                        "layer": layer_name,
                        "properties": row.to_dict()
                    })
                
                # Keep the detailed findings for the frontend
                results["findings"].append({
                    "layer": layer_name,
                    "count": len(intersecting),
                    "data": json.loads(intersecting.to_json())
                })
                
    return results
