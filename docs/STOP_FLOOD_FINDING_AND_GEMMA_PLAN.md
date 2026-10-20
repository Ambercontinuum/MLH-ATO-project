# Proposed demo finding: bus stop and flood-hazard overlap

Status: Team review proposal, 2026-10-19. This document records a reproducible map overlap and a narrow Gemma 4 integration plan. It does not establish observed flooding, service disruption, or a city-approved inspection priority.

## The decision question

Which GoRaleigh stops fall within mapped Special Flood Hazard Areas, and which records should Transit and Stormwater inspect together before making stop-improvement decisions?

## Verified example

The City of Raleigh bus-stop layer lists stop 8099, "Wake Forest Rd at Hodges St (NB)," as active at longitude -78.6261451344051, latitude 35.815159004095. Its record marks GoRaleigh Route 2 and records ADA_Compliant = No. That field is an inventory value, not a current field inspection.

An ArcGIS point-intersection query against the FEMA-derived USA Flood Hazard Areas layer returns one polygon for that coordinate: FLD_AR_ID 37183C_1215, OBJECTID 2910866, FLD_ZONE AE, SFHA_TF T, SOURCE_CIT 37183C_STUDY146. The flood layer's item description identifies a March 3, 2026 FEMA National Flood Hazard Layer snapshot.

Sources:
- City stop dataset: https://data-ral.opendata.arcgis.com/datasets/goraleigh-bus-stops-1/explore
- Stop 8099 GeoJSON: https://services.arcgis.com/v400IkDOw1ad7Yad/arcgis/rest/services/GoRaleigh_BusStops/FeatureServer/0/query?where=Stop_ID%3D8099&outFields=Stop_ID%2CStop_Name%2CR2%2CADA_Compliant%2CStatus%2CEditDate&outSR=4326&f=geojson
- Flood layer item and terms: https://www.arcgis.com/home/item.html?id=ccd29fb4bd5e4b44a2d61638829a5d7e
- Reproducible point query: https://services5.arcgis.com/7weheFjxuNkGGiZi/arcgis/rest/services/USA_Flood_Hazard_Areas_view/FeatureServer/0/query?where=SFHA_TF%3D%27T%27&geometry=-78.6261451344051%2C35.815159004095&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=OBJECTID%2CFLD_AR_ID%2CFLD_ZONE%2CSFHA_TF%2CSOURCE_CIT&returnGeometry=false&f=pjson
- Compact GeoJSON for the demo area (51 hazard polygons when checked): https://services5.arcgis.com/7weheFjxuNkGGiZi/arcgis/rest/services/USA_Flood_Hazard_Areas_view/FeatureServer/0/query?where=SFHA_TF%3D%27T%27&geometry=-78.65%2C35.80%2C-78.60%2C35.83&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=OBJECTID%2CFLD_AR_ID%2CFLD_ZONE%2CSFHA_TF%2CSOURCE_CIT&outSR=4326&f=geojson

The stop data and flood-hazard map represent different dates and purposes. The overlap is a screening result. Staff would need to verify actual drainage, pedestrian access, and improvement relevance on site. The Esri-hosted flood layer carries separate use terms; link to the service and review those terms before bundling a data snapshot in the public repository.

## Implementation boundary

1. Load real stop points and the demo-area hazard polygons as GeoJSON. Do not use the example geometries currently in backend/data as evidence.
2. Compute point-in-polygon deterministically. A map click within a buffer of two independent layers is not the same as a stop-polygon join. Return stop ID, polygon ID, zone, method, source URLs, dataset dates, and limitations.
3. Display the finding and source records in the map panel. Offer a "Draft inspection brief" action only for a verified finding.
4. Send the structured finding from the backend to DigitalOcean Inference using the Chat Completions API, endpoint https://inference.do-ai.run/v1/chat/completions and model gemma-4-31B-it. Keep the access key in a server environment variable. Parse choices[0].message.content.
5. Ask Gemma for a concise Transit–Stormwater handoff: observed overlap, recorded stop context, on-site checks, and explicit uncertainty. Gemma explains the finding; it does not calculate the join or assert that flooding occurred.
6. Show a real model response in the demo. Label or omit any mock response. The current backend's placeholder-key path returns "AI MOCK" and its default API URL/body do not match DigitalOcean Chat Completions.

DigitalOcean API reference: https://docs.digitalocean.com/products/inference/how-to/use-chat-completions-api/

## Video acceptance path

In 60–90 seconds: state the decision question; show stop 8099 and the AE polygon; open both source records and the point-in-polygon result; generate the Gemma brief; close with the field-verification limit. Record the working application and verify the uploaded video link before submission.
