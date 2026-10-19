"""
GoRaleigh Bus Routes — Viewer
------------------------------
Fetches route data from the City of Raleigh ArcGIS FeatureServer
and displays it as a clean, readable table with breakdowns by
direction, line, and service frequency.
"""

import requests
import pandas as pd

URL = (
    "https://services.arcgis.com/v400IkDOw1ad7Yad/arcgis/rest/services"
    "/GoRaleigh_Routes/FeatureServer/0/query"
)
PARAMS = {"where": "1=1", "outFields": "*", "outSR": "4326", "f": "json"}

# ── FETCH ─────────────────────────────────────────────────────────────────────
print("\n📡 Fetching GoRaleigh Bus Routes ...")
r = requests.get(URL, params=PARAMS, timeout=20)
r.raise_for_status()
features = r.json().get("features", [])
print(f"✅ {len(features):,} routes loaded\n")

# ── BUILD TABLE ───────────────────────────────────────────────────────────────
records = [feat["attributes"] for feat in features]
df = pd.DataFrame(records)

df = df.rename(columns={
    "OBJECTID":   "Route ID",
    "full_name":  "Full Name",
    "dir_id":     "Direction ID",
    "dir_name":   "Direction",
    "pattern":    "Pattern",
    "line_name":  "Line Name",
    "map_name":   "Map Version",
    "GlobalID":   "Global ID",
    "Frequency":  "Frequency (min)",
})

pd.set_option("display.max_rows",    None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 45)
pd.set_option("display.width",       140)

# ── HEADER ────────────────────────────────────────────────────────────────────
print("=" * 80)
print("  GORALEIGH BUS ROUTES  |  City of Raleigh Transit")
print("=" * 80)
print(f"  Total routes : {len(df)}")
print(f"  Columns      : {list(df.columns)}")
print()

# ── FULL TABLE ────────────────────────────────────────────────────────────────
print("📊 Full Route Table:")
print(df[["Route ID", "Full Name", "Direction", "Line Name", "Frequency (min)"]].to_string(index=True))

# ── BREAKDOWN BY DIRECTION ────────────────────────────────────────────────────
print("\n\n🧭 Routes by Direction:")
print("-" * 50)
dir_counts = df["Direction"].value_counts()
for direction, count in dir_counts.items():
    pct = count / len(df) * 100
    bar = "█" * int(pct / 2)
    print(f"  {str(direction):<12} {count:>4}  {pct:5.1f}%  {bar}")

# ── TOP LINES BY ROUTE COUNT ──────────────────────────────────────────────────
print("\n\n🚌 Routes per Line:")
print("-" * 65)
line_counts = (
    df.groupby("Line Name")["Frequency (min)"]
      .agg(Routes="count", Avg_Freq="mean")
      .sort_values("Routes", ascending=False)
)
line_counts["Avg_Freq"] = line_counts["Avg_Freq"].round(1)
line_counts.columns = ["# Routes", "Avg Freq (min)"]
print(line_counts.to_string())

# ── FREQUENCY BREAKDOWN ───────────────────────────────────────────────────────
print("\n\n⏱️  Service Frequency Distribution:")
print("-" * 50)
freq_counts = df["Frequency (min)"].value_counts().sort_index()
for freq, count in freq_counts.items():
    pct = count / len(df) * 100
    bar = "█" * int(pct / 2)
    print(f"  Every {str(int(freq)) + ' min':<10} {count:>4} routes  {pct:5.1f}%  {bar}")

# ── SUMMARY STATS ─────────────────────────────────────────────────────────────
print("\n\n📈 Frequency Stats:")
print("-" * 40)
print(df["Frequency (min)"].describe().round(1).to_string())

print("\n✨ Done!\n")
