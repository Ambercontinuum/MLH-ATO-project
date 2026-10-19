"""
Solid Waste Services Collection Areas — Viewer
-----------------------------------------------
Fetches polygon collection zone data from the City of Raleigh ArcGIS service
and displays it as a clean, readable table with breakdowns by service day,
collection type, and week schedule.
"""

import requests
import pandas as pd
import json

URL = (
    "https://services.arcgis.com/v400IkDOw1ad7Yad/arcgis/rest/services"
    "/Solid_Waste_Services_Collection_Areas/FeatureServer/0/query"
)
PARAMS = {"where": "1=1", "outFields": "*", "outSR": "4326", "f": "json"}

# ── FETCH ─────────────────────────────────────────────────────────────────────
print("\n📡 Fetching Solid Waste Collection Areas ...")
r = requests.get(URL, params=PARAMS, timeout=30)
r.raise_for_status()
data = r.json()

features = data.get("features", [])
print(f"✅ {len(features):,} zones loaded\n")

# ── BUILD TABLE ───────────────────────────────────────────────────────────────
records = [feat["attributes"] for feat in features]
df = pd.DataFrame(records)

# Friendly column names
df = df.rename(columns={
    "OBJECTID":        "Zone ID",
    "Shape__Area":     "Area (sq ft)",
    "Shape__Length":   "Perimeter (ft)",
    "SERVICEDAY":      "Service Day",
    "RECYCLE":         "Recycling Week",
    "GARBAGE":         "Garbage Pickup",
    "YARDWASTE":       "Yard Waste",
    "SER_WEEK":        "Service Week",
    "SERVICEDAYNEW":   "Service Day (New)",
    "RECYCLINGWEEKNEW":"Recycling Week (New)",
})

pd.set_option("display.max_rows",    40)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 25)
pd.set_option("display.width",       130)

# ── HEADER ────────────────────────────────────────────────────────────────────
print("=" * 80)
print("  SOLID WASTE SERVICES — COLLECTION AREAS  |  City of Raleigh")
print("=" * 80)
print(f"  Zones    : {len(df):,}")
print(f"  Columns  : {list(df.columns)}")
print()

# ── FULL TABLE ────────────────────────────────────────────────────────────────
print("📊 Full Attribute Table:")
print(df.to_string(index=True))

# ── SERVICE DAY BREAKDOWN ─────────────────────────────────────────────────────
print("\n\n📅 Zones by Service Day:")
print("-" * 55)
day_order = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]
counts = df["Service Day"].value_counts()
for day in day_order:
    if day in counts:
        pct = counts[day] / len(df) * 100
        bar = "█" * int(pct / 2)
        print(f"  {day.title():<12} {counts[day]:>4}  {pct:5.1f}%  {bar}")
# Any remaining days not in standard order
for day, count in counts.items():
    if day not in day_order:
        pct = count / len(df) * 100
        print(f"  {str(day).title():<12} {count:>4}  {pct:5.1f}%")

# ── RECYCLING SCHEDULE ────────────────────────────────────────────────────────
print("\n\n♻️  Recycling Week Distribution:")
print("-" * 45)
recycle_counts = df["Service Week"].value_counts().sort_index()
for week, count in recycle_counts.items():
    pct = count / len(df) * 100
    bar = "█" * int(pct / 2)
    print(f"  {str(week):<10} {count:>4}  {pct:5.1f}%  {bar}")

# ── YARD WASTE ────────────────────────────────────────────────────────────────
if "Yard Waste" in df.columns:
    print("\n\n🍂 Yard Waste Service:")
    print("-" * 45)
    yw_counts = df["Yard Waste"].value_counts()
    for val, count in yw_counts.items():
        pct = count / len(df) * 100
        print(f"  {str(val):<20} {count:>4}  {pct:5.1f}%")

# ── AREA STATS ────────────────────────────────────────────────────────────────
print("\n\n📐 Zone Size Stats (sq ft):")
print("-" * 45)
area = df["Area (sq ft)"].dropna()
print(f"  Smallest zone : {area.min():>15,.0f} sq ft")
print(f"  Largest zone  : {area.max():>15,.0f} sq ft")
print(f"  Average zone  : {area.mean():>15,.0f} sq ft")
print(f"  Total coverage: {area.sum():>15,.0f} sq ft  ({area.sum()/27878400:.1f} sq miles)")

print("\n✨ Done!\n")
