import requests
import json
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape

# Configuration
DATA_DIR = "backend/data"
DATASETS = {
    "flood_zones": "https://services1.arcgis.com/aT1T0pU1ZdpuDk1t/ArcGIS/rest/services/Flood_Prone_Areas_WFL1/FeatureServer/0/query?where=1%3D1&outFields=*&f=geojson",
    "bus_routes": "https://data-wake.opendata.arcgis.com/datasets/ral::goraleigh-bus-routes/api" # This is an API portal link, may need specific query
}

def fetch_geojson(url):
    print(f"Fetching data from {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def normalize_dataset(name, data):
    if not data:
        return None
    
    print(f"Normalizing {name}...")
    # Load into GeoPandas for normalization
    gdf = gpd.GeoDataFrame.from_features(data['features'])
    
    # Ensure we are using WGS84 (EPSG:4326) for the frontend
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)
    else:
        gdf = gdf.to_crs(epsg=4326)
    
    # Save as GeoJSON locally
    output_path = os.path.join(DATA_DIR, f"{name}.geojson")
    gdf.to_file(output_path, driver='GeoJSON')
    print(f"Saved normalized {name} to {output_path}")
    return output_path

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    for name, url in DATASETS.items():
        # Special handling for the ArcGIS FeatureServer query
        data = fetch_geojson(url)
        if data:
            normalize_dataset(name, data)
        else:
            print(f"Failed to ingest {name}")

if __name__ == "__main__":
    main()
