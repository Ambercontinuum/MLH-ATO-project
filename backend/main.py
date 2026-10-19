from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import geopandas as gpd
from shapely.geometry import Point
import os
import json
import requests

app = FastAPI(title="Raleigh CivicPulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "backend/data"
# Configuration for DigitalOcean Serverless Inference
GEMMA_API_URL = os.getenv("GEMMA_API_URL", "https://api.digitalocean.com/v1/inference/gemma4")
GEMMA_API_KEY = os.getenv("GEMMA_API_KEY", "placeholder_key")

def load_geojson(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return None
    return gpd.read_file(path)

async def generate_ai_brief(structured_findings):
    """
    Calls the Gemma 4 model to transform structured findings into a human-readable brief.
    """
    if not structured_findings["layers"]:
        return "No significant overlapping infrastructure concerns found at this location."

    prompt = f"""
    You are a municipal intelligence assistant for the city of Raleigh.
    Based on the following technical spatial analysis findings, provide a concise, evidence-grounded brief for city planners.
    
    FINDINGS:
    - Location: {structured_findings['location']}
    - Intersecting Layers: {', '.join(structured_findings['layers'])}
    - Observations: {structured_findings['observations']}
    - Source Evidence: {json.dumps(structured_findings['source_records'])}
    
    RULES:
    1. DO NOT invent data, route names, or hazard levels not present in the evidence.
    2. Focus on the intersection of services.
    3. Clearly state that these are screening signals, not validated outcomes.
    4. Recommend which departments should verify this (e.g., Stormwater and Transit).
    5. Keep it under 150 words.
    
    BRIEF:
    """
    
    try:
        # Mocking the API call for skeleton functionality
        # In production, this uses the DigitalOcean Serverless Inference endpoint
        if GEMMA_API_KEY == "placeholder_key":
            return f"AI MOCK: The location at {structured_findings['location']} shows an overlap between {', '.join(structured_findings['layers'])}. This suggests a potential infrastructure conflict that requires joint review by the relevant departments. This is a screening signal based on GIS data and requires field verification."
        
        response = requests.post(
            GEMMA_API_URL,
            headers={"Authorization": f"Bearer {GEMMA_API_KEY}", "Content-Type": "application/json"},
            json={"prompt": prompt, "max_tokens": 200, "temperature": 0.1},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("text", "AI failed to generate a brief.")
    except Exception as e:
        return f"AI Briefing unavailable: {str(e)}"

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
                    results["source_records"].append({
                        "id": rec_id,
                        "layer": layer_name,
                        "properties": row.to_dict()
                    })
                results["findings"].append({
                    "layer": layer_name,
                    "count": len(intersecting),
                    "data": json.loads(intersecting.to_json())
                })
                
    # Integrate Interpretation Agent
    results["ai_brief"] = await generate_ai_brief(results)
                
    return results
