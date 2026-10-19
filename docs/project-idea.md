
# Raleigh CivicPulse
## Hackathon Team Concept Brief — Cross-Department Civic Intelligence

**Event:** Hacktoberfest Hacks @ All Things Open (MLH), Raleigh, NC
**Status:** Team brainstorming / proposed MVP — not a completed or validated product
**Working Title:** Raleigh CivicPulse (name can change)
**Core Theme:** Enterprise workflow + data analysis + AI + open civic data

---

### 1. The Shared Problem

Raleigh publishes information across diverse municipal domains—including transportation, housing, public safety, urban planning, sustainability, and stormwater. Different departments understand their own area, but residents experience the city as one interconnected system.

**Problem Statement:** Municipal data is often organized by department, while real-world problems cross departmental boundaries. This fragmentation makes it hard to discover overlapping risks, reconcile information, assign responsibility, and prioritize coordinated action.

The larger enterprise/workplace version of this problem is the same: people and teams operate with different pieces of information, and no one has an easy way to understand how those pieces affect one another.

**Opportunity:** Build an open-source, AI-assisted tool that brings relevant municipal datasets together, computes cross-system relationships, and translates evidence into usable decision briefs for humans.

**One-sentence concept:** Raleigh CivicPulse connects open city datasets to identify overlapping neighborhood infrastructure concerns and help departments decide what to investigate together.

### 2. What the Raleigh Open Data Categories Have in Common

The Raleigh Open Data portal in our exploration has 10 visible categories (five per row):

| Raleigh Open Data Category | Potential Contribution to a Cross-Department Question |
| :--- | :--- |
| **About Raleigh** | Geography, demographics, neighborhood context, city-wide changes |
| **City Government** | Organizational responsibilities, services, and administrative context |
| **Public Safety** | Emergency response context and safety-related infrastructure |
| **Transportation** | Bus routes, roads, mobility, access to services |
| **Housing & Neighborhoods** | Housing distribution, neighborhoods, and potentially vulnerability indicators |
| **Urban Planning** | Land use, future development, zoning, growth patterns |
| **Parks & Recreation** | Access to parks, green space, and recreation amenities |
| **Sustainability** | Environmental planning, resilience, environmental performance |
| **Stormwater** | Flood-prone areas, drainage systems, watershed infrastructure |
| **Solid Waste Services** | Collection routes, service areas, municipal operations |

**Unifying Theme:** Neighborhood resilience and service accessibility. How do local conditions and public services overlap, and where could an issue in one system affect another?

**Important Qualification:** These are possible analytical uses of the categories, not a promise that every corresponding dataset exists or is available at the same geographic resolution. The team must inspect actual datasets, metadata, licensing, and timestamps.

### 3. Recommended Starting Use Case: Flood Exposure × Transportation Access

**Question to Demo:** Which mapped flood-prone areas overlap important transportation routes or stops, and which locations deserve further human review?

**Why this is a strong first use case:**
*   **Cross-department:** Stormwater + Transportation, with Urban Planning/neighborhoods as optional context.
*   **Spatially testable:** Geographic intersections can be computed reproducibly rather than guessed by a language model.
*   **Visual:** A map makes the problem and evidence understandable in seconds.
*   **Expandable:** Other categories can be added later without rebuilding the concept.
*   **Actionable:** The output can flag areas for planners to inspect, without pretending to predict actual closures or emergency outcomes.

**Example Demonstration (hypothetical):**
1. Load sample flood-prone polygons and transportation routes/stops.
2. Overlay layers and identify intersections or proximity within a defined buffer.
3. Display results on a Raleigh map.
4. Select one flagged location.
5. Show the underlying GIS records and an AI-generated plain-language brief: what intersects, which datasets support the finding, what is uncertain, and which department(s) should verify next.

**Critical Disclaimer:** Do not claim: “This road will flood,” “Bus service is disrupted,” or “Neighborhood X is unsafe.” An intersection is a screening signal, not a validated outcome or prediction.

### 4. Proposed Minimum Viable Product (MVP)

**Must have for the hackathon:**
*   **Data ingestion:** Load two real, accessible Raleigh-area datasets (ideally flood-related GIS features plus GoRaleigh routes or stops).
*   **Deterministic spatial analysis:** Compute geometry intersections/buffers and basic counts or distances.
*   **Map interface:** Show both layers and highlight locations requiring review.
*   **Evidence panel:** Show the actual contributing records, dataset links, update dates (if supplied), and relevant analysis criteria.
*   **AI interpretation:** Use an open-weight model (Gemma if appropriate under the event rules) to convert verified analysis results into a concise human-readable briefing with limitations.
*   **Reproducible demo:** Public repository, setup instructions, sample data or download instructions, and one complete example.

**If time permits (Stretch Goals):**
*   Neighborhood boundaries and a second screening layer.
*   Priority scoring with explicit, explainable weights.
*   Department routing or human acknowledgement/resolution workflow.
*   CSV or PDF export.
*   Cloud deployment (e.g., DigitalOcean), if feasible and eligible for an event prize.

**Deliberately Out of Scope for a One-Day Prototype:**
*   Integrating every category in the portal.
*   Live municipal operational feeds or private enterprise systems.
*   Automated dispatch, operational decisions, or official hazard forecasts.
*   Claiming the system determines which neighborhood should receive funding.

### 5. Suggested Architecture

This section outlines the process flow:

**Raleigh Open Data / ArcGIS Services**
$\downarrow$
**Data Ingestion / Normalization**
$\downarrow$
**Geospatial Operations** (intersect, buffer, group)
$\downarrow$
**Evidence-backed findings (JSON)**
$\begin{array}{c|c}
\downarrow & \searrow \\
\text{Interactive Map} & \text{Open-weight LLM} \\
\downarrow & \downarrow \\
\text{Human-readable brief} & \text{Human verification}
\end{array}$

**Critical Design Rule:** The geospatial/data layer establishes the findings; the AI explains those findings. The model should not invent affected routes, numeric measurements, hazards, or source records.

**Possible Implementation Choices (Options, not mandatory):**
*   **Data:** GeoJSON / ArcGIS REST / CSV, Python, GeoPandas or Shapely.
*   **Backend:** FastAPI or a lightweight Python service.
*   **Frontend:** Streamlit for speed, or React with Leaflet/MapLibre for a richer map.
*   **LLM:** Gemma or another qualifying open-weight model to summarize structured output only.
*   **Deployment:** Local demo first; cloud deployment second.

**Example Analysis Output Schema:**
```json
{
  "finding_id": "demo-001",
  "analysis_type": "spatial_overlap",
  "location_label": "Example corridor (placeholder)",
  "layers": ["flood_prone_areas", "bus_routes"],
  "observation": "Mapped features overlap under the selected spatial test",
  "source_records": ["feature-id-1", "feature-id-2"],
  "method": "geometry intersection; projected coordinate system checked",
  "limitations": [
    "Map layers may represent different dates",
    "Overlap does not establish an active flood or service disruption"
  ],
  "recommended_human_check": "Ask stormwater and transit staff to verify operational relevance"
}
```

### 6. Data Starting Points

*   **Raleigh Open Data portal:** https://data-ral.opendata.arcgis.com/
*   **Hackathon event page:** https://www.mlh.com/events/hacktoberfest-hacks-all-things-open/
*   **Wake County / regional open data portal:** https://data-wake.opendata.arcgis.com/

**Candidate GIS Services (Verification Required):**
*   **Flood-prone areas:** https://services1.arcgis.com/aT1T0pU1ZdpuDk1t/ArcGIS/rest/services/Flood_Prone_Areas_WFL1/FeatureServer
*   **GoRaleigh bus routes:** https://data-wake.opendata.arcgis.com/datasets/ral::goraleigh-bus-routes/api
*   **Raleigh solid waste service:** https://cityworksgisprd.raleighnc.gov/arcgis/rest/services/cityworks/SOLID_WASTE_SERVICES/FeatureServer

**First Data Verification Checklist:**
[ ] Both chosen layers are publicly accessible and permit intended reuse.
[ ] Coverage includes Raleigh / the same geographic area.
[ ] Geometry and coordinate reference systems are compatible.
[ ] Date of update and feature definitions are documented.
[ ] At least one meaningful overlap appears in actual test data.
[ ] Record IDs or source links can be exposed in the UI.
[ ] A fallback dataset or static data snapshot is saved for the demo (subject to licensing).

### 7. What Differentiates This from “Chat with Your Documents”

A generic chatbot retrieves and summarizes text. **CivicPulse** computes cross-dataset relationships first and then uses AI to make those evidence-backed relationships legible to humans.

**The Important Difference Is:**
1.  **Discovery:** Find related records across municipal silos.
2.  **Analysis:** Perform reproducible geographic or data joins.
3.  **Provenance:** Show exactly which records support a finding.
4.  **Interpretation:** Explain the implications and uncertainty in plain English.
5.  **Coordination:** Identify which departments or humans should review the result.

That architecture could later apply to corporate operations, supply chains, IT service management, healthcare administration, or other multi-team workplaces—but the hackathon demo stays firmly scoped to Raleigh open data.

### 8. Prize Alignment (Confirm Event-Specific Rules)

*   **Primary Design Target:** Best Open-Source AI Project (Requires genuine open-weight AI, public, demonstrable, and reproducible).
*   **Possible Secondary Opportunities:**
    *   **Gemma model category:** Use Gemma meaningfully for evidence-grounded summarization.
    *   **DigitalOcean category:** Deploy a working service if the track rewards a valid implementation and time permits.
    *   **Other sponsor/data/UX categories:** Check the official Raleigh challenge page; do not assume eligibility.

**Team Action:** Open each event-specific challenge page and record judging criteria, required technology, restrictions on pre-existing work, eligibility, submission links, and deadlines. Design to win one category well before adding complexity for additional categories.

### 9. Suggested Division of Labor

| Role | Deliverable |
| :--- | :--- |
| **Data / GIS** | Validated datasets, spatial intersection, results JSON |
| **App / Frontend** | Map, layers, finding detail panel |
| **AI / Backend** | Constrained summarization using structured results; guardrails and citations |
| **Product / Demo** | Problem statement, UX path, judges' pitch, README and submission |

*Adjust to team size and skills. Two people can combine roles; nobody needs to own a full production stack.*

**Suggested Short Build Sequence:**
1. Agree on one real question and choose two datasets.
2. Prove the data join before spending time on the UI or prompts.
3. Create one complete finding, with traceable evidence.
4. Make it visible on a simple map.
5. Add AI explanation, constrained to the finding JSON.
6. Rehearse the demo and test it offline or with a reliable fallback.

**Suggested 90-Second Demo Flow:**
*   **0–15 sec:** "City information is organized by department, but problems cross departmental lines.”
*   **15–35 sec:** Show two datasets displayed separately, then overlay them.
*   **35–55 sec:** Click a computed intersection and show the real records that produced it.
*   **55–75 sec:** Generate a grounded cross-department briefing with limitations and suggested verification.
*   **75–90 sec:** Explain how this can scale to more municipal datasets and enterprise workflows.

### 10. Team Pitch (Copy/Paste)

What if city departments could see how problems in one system affect another? Raleigh already makes public data available across transportation, stormwater, housing, public safety, planning, and other services. But the datasets are separated by category while real problems overlap. We propose **CivicPulse**, an open-source, AI-assisted civic intelligence tool. Our MVP will cross-reference flood-prone areas with transportation infrastructure, compute and visualize where they intersect, and produce transparent, evidence-backed briefs to help humans identify where further coordination is needed. We are not trying to predict disasters or replace experts. We are making fragmented city data easier to use together.

### 11. Team Decisions Needed Now

1.  Is flood exposure × transportation access the most interesting and technically feasible use case given the datasets we can actually access?
2.  Which two datasets load cleanly right now?
3.  Are we targeting open-source AI first, with other sponsor tracks as bonuses?
4.  What is the team's fastest reliable stack and who owns each component?
5.  Who will verify the event's exact submission and prize requirements?

**Success Criterion:** A judge can point to one highlighted location, inspect the actual supporting city records, understand the computed relationship, and see the AI explain it without inventing facts.
"