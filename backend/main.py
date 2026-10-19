from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/api/query")
async def query_location(lat: float, lon: float, buffer_m: float = 100):
    """
    Query location for intersecting GIS data.
    lat: Latitude
    lon: Longitude
    buffer_m: Search buffer in meters (default 100m)
    """
    # Create a point for the query location
    # Note: GeoPandas uses (lon, lat) for Point
    point = Point(lon, lat)
    
    # We use a simple distance check. For real meters, we'd need to project to a UTM CRS.
    # For this skeleton, we'll use a rough degree approximation or a small buffer.
    # 0.001 degrees is roughly 111 meters.
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
            # Find features that intersect the search area
            intersecting = gdf[gdf.intersects(search_area)]
            if not intersecting.empty:
                # Convert GeoDataFrame to a list of dictionaries
                features = intersecting.to_json()
                results["findings"].append({
                    "layer": layer_name,
                    "count": len(intersecting),
                    "data": json.loads(features)
                })
                
    return results
