# Autonomous Agents Workflow

## Project Context
For a comprehensive understanding of the system, refer to the following documentation:
- [Project Idea](./docs/project-idea.md): Problem statement and core concept.
- [Architecture](./ARCHITECTURE.md): Technical stack and data flow.
- [Roadmap](./ROADMAP.md): Current development status and priority tasks.
- [README](./README.md): General project overview and setup.

This section defines the roles of specialized agents within the CivicPulse system, primarily responsible for handling complex, non-real-time, or computationally intensive backend tasks that precede the core UI interaction.

## Agent Roles & Responsibilities

### 1. Data Ingestion Agent
*   **Goal:** To standardize, verify, and pre-process heterogeneous raw data from various open data sources.
*   **Inputs:** Raw GeoJSON, CSV, or API endpoints (e.g., Flood Service, Bus Routes API).
*   **Process:**
    1.  **Metadata Extraction:** Systematically logging source metadata (last updated date, license, geometry CRS, coverage area).
    2.  **Normalization:** Transforming all features into a common, unified data model (e.g., standardizing field names, projecting coordinates to a unified CRS like WGS 84).
    3.  **Validation:** Running checks against the verification checklist (see project-idea.md) and flagging inconsistencies.
*   **Output:** Clean, normalized, and structured data layers, ready for spatial analysis.

### 2. Geospatial Analysis Agent
*   **Goal:** To perform reproducible, deterministic spatial computations (non-AI tasks).
*   **Inputs:** Two or more normalized data layers (e.g., `A` and `B`).
*   **Process:**
    1.  **Intersection:** Calculating geometric overlaps (intersection).
    2.  **Proximity:** Calculating buffers or nearest neighbors between designated features (e.g., finding all routes within 500m of a flood zone).
    3.  **Aggregation:** Grouping records based on shared properties and spatial clusters.
*   **Limitations:** This agent *only* performs computation based on the provided geometries and data; it does not infer cause or effect.
*   **Output:** A structured JSON file containing the coordinates of overlaps, the source records (IDs), and the analysis computation method used.

### 3. Interpretation Agent (AI Integration)
*   **Goal:** To translate structured, evidence-backed data (JSON) into concise, human-readable summaries for the end-user.
*   **Inputs:** The structured JSON output from the Geospatial Analysis Agent.
*   **Process:**
    1.  **Citation Grounding:** Strictly limiting output to information and data fields present in the input JSON.
    2.  **Summarization:** Generating plain-language narratives around the findings, highlighting the significance and potential impact (e.g., "This overlap suggests a high risk area requiring a joint review").
    3.  **Transparency:** Explicitly detailing the limitations and uncertainty in the summary, and listing the exact departments/stakeholders who should verify the result.
*   **Model:** Gemma 4 (constrained via API prompt engineering).
*   **Output:** A finalized markdown/string brief for the pop-over panel.

## Implementation Strategy
1.  Start by implementing the **Data Ingestion Agent** using Python/GeoPandas (fastest win).
2.  Next, implement the basic **Geospatial Analysis** (intersection/buffer) using FastAPI endpoints referencing the structured data.
3.  Finally, integrate the **Interpretation Agent** layer, feeding the JSON output to the Gemma 4 API.

**Hackathon Velocity Rules:**
*   **Continuous Integration:** Commit and push all work automatically upon completion of a task or sub-task to prevent data loss and maintain a clear audit trail.
*   **Rapid Deployment:** Automate (re)deployment to DigitalOcean immediately following successful commits to ensure the demo site is always current.
*   **Roadmap Maintenance:** Proactively update `ROADMAP.md` as features are implemented to ensure a real-time source of truth for project progress.
