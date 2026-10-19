# Project Roadmap: Raleigh CivicPulse

This roadmap serves as a checklist for developing CivicPulse, guiding both infrastructure tasks and feature implementation. Each major phase builds upon the complexity of the previous one.

## 🌟 Phase 0: Foundation & Infrastructure (Current Status)
**Goal:** Establish a functional, containerized environment capable of handling basic data flow from source to endpoint.
**Status:** ✅ Complete

*   [x] Monorepo structure established (frontend, backend).
*   [x] Backend FastAPI wrapper defined and containerized (Docker/docker-compose).
*   [x] Frontend React structure and base build pipeline defined.
*   [x] CI/CD target set (DigitalOcean deployment structure understood).

---

## 🏗️ Phase 1: Minimum Viable Product (MVP) - Core Plumbing
**Goal:** Prove the critical data pipeline: Raw Data $\rightarrow$ Structured JSON $\rightarrow$ Map Display.
**Target Outcome:** A functional map that displays two intersecting datasets and shows raw IDs on click.

### Infrastructure & Data (Tasks owner: Data / GIS)
*   [x] **Source Data Acquisition:** Secure initial two working datasets (e.g., Flood Zones, Bus Routes) and verify their live access and schema.
*   [x] **Data Ingestion Pipeline:** Implement the `Data Ingestion Agent` (Python/GeoPandas) to normalize, validate, and store raw data.
*   [x] **Backend Basic API:** Create the basic FastAPI endpoint (`/api/query`) that accepts coordinates and returns *raw, unprocessed* search results.
*   [ ] **Testing:** Write unit tests for data normalization and coordinate projection.

### Feature Implementation (Tasks owner: App / Frontend)
*   [x] **Frontend Map Skeleton:** Implement the base React component using Leaflet/MapLibre, capable of loading a background OSM layer.
*   [x] **MapInteraction:** Implement the click handler that coordinates coordinates to the Backend API.
*   [x] **Initial Map Overlay:** Display the first dataset (e.g., Flood Zones) as a static layer based on the API response.

---

## 🧠 Phase 2: Core Intelligence & Evidence (The "AHA" Moment)
**Goal:** Implement the cross-domain analysis and AI interpretation layers.
**Target Outcome:** A map query triggers a fully generated, evidence-backed brief.

### Backend & Analysis (Tasks owner: AI / Backend)
*   [x] **Spatial Join Logic:** Implement the `Geospatial Analysis Agent` to perform deterministic intersections/buffers between the two source datasets (e.g., Flood $\cap$ Bus Route).
*   [x] **Structured Output:** Modify the backend to format the computed intersections into the required JSON schema.
*   [x] **API Endpoint Expansion:** Update the API to accept the JSON and pass it to the LLM.
*   [x] **Prompt Engineering:** Finalize the prompt template for Gemma 4, enforcing constraint and citation rules.

### Frontend & UX (Tasks owner: App / Frontend)
*   [x] **Evidence Panel:** Build the pop-over component to display raw source records, links, and method.
*   [x] **AI Brief Display:** Integrate the LLM-generated brief into the UI, making it legible, and placing high visibility on the limitations section.
*   [ ] **Demo Flow:** Rehearse the core 90-second demo flow using the functional MVP.

---

## 🚀 Phase 3: Polish, Scale & Submission
**Goal:** Harden the solution, add polish, and prepare for the hackathon.
**Status:** In Progress

*   [ ] **Expansion (Optional):** Integrate a third data layer and/or introduce the visualization of a second screening layer (per project-idea.md).
*   [ ] **Robust Error Handling:** Implement comprehensive client/server-side error logging and user feedback.
*   [ ] **Optimization:** Optimize image serving and state transitions for mobile/slow networks.
*   [ ] **Documentation:** Finalize the `README.md` and create pitch materials/slides.
*   [ ] **Final Test:** Run full integration tests with a mockup set of data.

---

## 🚀 Post-MVP Goals
- **Snowflake Integration:** Explore adding Snowflake for enhanced data warehousing and analytics (primarily for hackathon bingo). This should be prioritized only after a stable MVP is achieved.
