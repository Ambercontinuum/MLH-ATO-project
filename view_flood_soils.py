"""
Flood Prone Soils - GeoJSON Viewer
-----------------------------------
Reads Flood_Prone_Soils.geojson and displays the attribute table
as a clean, readable DataFrame — no geometry clutter.
"""

import json
import pandas as pd

FILE = "Flood_Prone_Soils.geojson"

# ── LOAD ──────────────────────────────────────────────────────────────────────
print(f"\n📂 Loading {FILE} ...")

with open(FILE) as f:
    data = json.load(f)

features = data["features"]
print(f"✅ {len(features):,} features loaded\n")

# ── BUILD TABLE ───────────────────────────────────────────────────────────────
records = [feat["properties"] for feat in features]
df = pd.DataFrame(records)

# Clean up column names → title case, readable
df.columns = [c.replace("_", " ").title() for c in df.columns]

# Rename verbose columns for clarity
df = df.rename(columns={
    "Wake Floodsoils Area": "Area (sq ft)",
    "Dsl Name":             "Soil Code",
    "Hydric":               "Hydric Rating",
    "Description":          "Soil Description",
    "Fldsoils ":            "Flood Soil ID",
    "Fldsoils I":           "Flood Soil Index",
})

pd.set_option("display.max_rows",    30)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 55)
pd.set_option("display.width",       130)

# ── SUMMARY ───────────────────────────────────────────────────────────────────
print("=" * 80)
print("  FLOOD PRONE SOILS — WAKE COUNTY")
print("=" * 80)
print(f"  Rows    : {len(df):,}")
print(f"  Columns : {list(df.columns)}")
print()

# ── ATTRIBUTE TABLE ───────────────────────────────────────────────────────────
print("📊 Attribute Table (first 30 rows):")
print(df.head(30).to_string(index=True))

# ── HYDRIC RATING BREAKDOWN ───────────────────────────────────────────────────
print("\n\n📋 Hydric Rating Breakdown:")
print("-" * 45)
hydric_map = {
    "A": "All hydric",
    "D": "Partially hydric (some components)",
    "N": "Not hydric",
}
counts = df["Hydric Rating"].value_counts()
for code, count in counts.items():
    label = hydric_map.get(code, "Unknown")
    pct   = count / len(df) * 100
    bar   = "█" * int(pct / 2)
    print(f"  {code} ({label:<38}) {count:>5,}  {pct:5.1f}%  {bar}")

# ── TOP SOIL TYPES ────────────────────────────────────────────────────────────
print("\n\n🌱 Top 15 Soil Types (by code):")
print("-" * 70)
top_soils = (
    df.groupby(["Soil Code", "Soil Description"])
      .size()
      .reset_index(name="Count")
      .sort_values("Count", ascending=False)
      .head(15)
)
top_soils.index = range(1, len(top_soils) + 1)
print(top_soils.to_string())

# ── NUMERIC STATS ─────────────────────────────────────────────────────────────
print("\n\n📈 Numeric Column Stats:")
print("-" * 45)
print(df.select_dtypes(include="number").describe().round(2).to_string())

print("\n✨ Done!\n")
