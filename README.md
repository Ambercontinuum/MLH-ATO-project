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

## 🚀 Getting Started
*(Instructions for setup and running the local demo will be added here)*
