# Raleigh CivicPulse

A web application designed to connect disparate open municipal datasets to reveal overlapping neighborhood infrastructure concerns. CivicPulse computes cross-system relationships and presents actionable, evidence-backed briefs for human review, moving beyond simple document retrieval.

## 🗺️ Core Concept
The user interacts with an interactive map (e.g., OpenStreetMap) centered on Raleigh, NC. By panning and zooming, users can discover overlapping data patterns. Clicking on a specific location triggers a pop-over panel that displays detailed insights derived from multiple configured GIS datasets.

## 🛠️ Architecture & Stack
The system utilizes a modern full-stack approach for maximum scalability and performance:
- **Frontend:** React Web Application.
- **Backend:** Python FastAPI.
- **Database/Services:** Interaction with multiple open GIS services and data sources.
- **Deployment:** DigitalOcean.
- **AI:** Gemma 4 (open-weight model) for constrained, evidence-grounded summarization, running on DigitalOcean serverless inference.

## ✨ Features (MVP Focus)
*   **Interactive Map Viewer:** Displaying multiple geo-layers (e.g., transit routes, flood zones, solid waste) with distinct color-coding.
*   **Data Intersection Analysis:** Calculating and visualizing spatial overlaps between different datasets.
*   **Evidence Panel:** Presenting the exact source records, dataset metadata, and computational method used for every finding.
*   **AI Briefing:** Generating an easily digestible, plain-language summary of technical findings, clearly stating limitations and recommended human verification steps.


## 📁 Documentation
- [Project Idea](./docs/project-idea.md): Details the problem statement and intended use cases.
- [Architecture](./ARCHITECTURE.md): Defines the technical stack and data flow.
- [Agent Workflow](./agents.md): Describes the role of autonomous agents in data preprocessing and analysis.
- [Roadmap](./ROADMAP.md): Future enhancements and goals.



## 📘 Project Structure
This project is organized as a monorepo. The primary components are housed in:
*   `frontend/`: The React web application responsible for the map interface and UI.
*   `backend/`: The FastAPI service handling API requests, GIS processing, and AI calls.
*   `docker-compose.yml`: Defines the services and networking for running the entire stack locally.

## 🚀 Getting Started

For a live AI brief, set `GEMMA_API_KEY` to a DigitalOcean Inference **model access key** in the shell running Docker Compose. Keep the key out of Git. Then run `docker compose up --build` and open `http://localhost:3000`. Clicking near stop 8099 requests a brief only after the deterministic stop–hazard join succeeds. If the key or inference service is unavailable, the UI says so rather than displaying a mock answer.

The backend calls DigitalOcean Chat Completions with `gemma-4-31B-it`. See [DigitalOcean's model documentation](https://docs.digitalocean.com/products/inference/details/models/) and [Google's Gemma 4 model information](https://ai.google.dev/gemma/docs/core). The app is MIT licensed; the model has its own [Apache 2.0 terms](https://www.apache.org/licenses/LICENSE-2.0).
1. Build and run the entire stack using Docker Compose:
   \`docker-compose up --build\`
2. Navigate to the respective directories to work on the code.
3. All development and testing should be conducted within Docker containers for environment consistency.

### ☁️ Deployment
To deploy the latest changes to the DigitalOcean App Platform, ensure `doctl` is installed and authenticated, then run:
\`./deploy.sh\`
