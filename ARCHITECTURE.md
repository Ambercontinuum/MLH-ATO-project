# Software Architecture

## Core Components

**Frontend (React):**
*   Responsible for the map-centric user experience. Utilizes Leaflet or MapLibre to display interactive OpenStreetMap layers.
*   Handles all frontend state management, managing the visible layers, handling user interactions (panning, zooming, clicking locations), and rendering the pop-over Data Insight panel.

**Backend (FastAPI / Python):**
*   The core API endpoint for the application. It acts as the orchestrator, receiving map coordinates or data requests from the frontend.
*   Manages interactions with external GIS services, performing spatial joins, buffering, and data aggregation.
*   Normalizes disparate data formats into a unified Python/JSON structure, ensuring consistency for the AI layer.

**Workflow:**
1.  **Map Interaction:** User clicks (Lat/Lon) on the Map.
2.  **Backend Query:** FastAPI receives the coordinates and calls relevant downstream services (e.g., Flood Service, Bus Routes Service).
3.  **Data Aggregation:** The backend performs spatial joins (Intersect/Buffer) to aggregate raw records.
4.  **Structured Output:** Raw results are formatted into a JSON schema (as defined in project-idea.md).
5.  **AI Interpretation:** The structured JSON is passed to the LLM API (Gemma 4) for constrained summarization and brief generation.
6.  **Presentation:** The resulting brief, along with the source records, is returned to the frontend for display in the pop-over panel.

## Deployment & AI
*   **Cloud:** DigitalOcean.
*   **Containerization:** Docker/Docker Compose for local development and deployment.
*   **AI Integration:** Gemma 4 will be used via a DigitalOcean Serverless Inference endpoint. This ensures that LLM calls are separated from the core FastAPI logic, maintaining reliability and cost-efficiency.

***
*Note: This structure follows the pattern: GIS/Data Layer $\rightarrow$ Backend Processing $\rightarrow$ LLM Interpretation.*
