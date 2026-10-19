from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import geopandas as gpd
from shapely.geometry import Point
import os
import json

app = FastAPI(title="Raleigh CivicPulse API")

# Enable CORS for the React frontend
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
    """
    Returns all available GeoJSON layers for frontend rendering.
    """
    layers = {}
    datasets = {
        "flood_zones": "flood_zones.geojson",
        "bus_routes": "bus_routes.geojson"
    }
    
    for layer_name, filename in datasets.items():
        gdf = load_geojson(filename)
        if gdf is not None:
            # Convert GeoDataFrame to GeoJSON dict
            layers[layer_name] = json.loads(gdf.to_json())
            
    return layers

@app.get("/api/query")
async def query_location(lat: float, lon: float, buffer_m: float = 100):
    """
    Query location for intersecting GIS data.
    """
    point = Point(lon, lat)
    # Rough approximation: 0.001 deg ~ 111m
    buffer_deg = buffer_m / 111000.0
    search_area = point.buffer(buffer_deg)
    
    results = {
        "location": {"lat": lat, "lon": lon},
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
                results["findings"].append({
                    "layer": layer_name,
                    "count": len(intersecting),
                    "data": json.loads(intersecting.to_json())
                })
                
    return results
