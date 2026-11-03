"""Build site data from london-pulse (FSA food-hygiene register, OGL v3.0)."""
import json, struct, csv, pathlib
SRC = pathlib.Path(__file__).resolve().parent.parent.parent / "london-pulse/site/api/v1"
OUT = pathlib.Path(__file__).resolve().parent.parent
v = json.load(open(SRC / "venues.json"))
types, ratings, boroughs = v["types"], v["ratings"], v["boroughs"]
rows = v["venues"]  # [lng, lat, type, rating, borough, name, postcode, id, flag]
# points.bin: per venue uint16 lng, uint16 lat (quantised to bbox), uint8 borough
LNG0, LNG1, LAT0, LAT1 = -0.52, 0.34, 51.28, 51.70
buf = bytearray()
stats = {b: {"venues": 0, "restaurants": 0, "takeaways": 0, "pubs": 0, "other": 0, "five_star": 0} for b in boroughs}
for lng, lat, t, r, b, name, pc, i, f in rows:
    x = int((min(max(lng, LNG0), LNG1) - LNG0) / (LNG1 - LNG0) * 65535)
    y = int((min(max(lat, LAT0), LAT1) - LAT0) / (LAT1 - LAT0) * 65535)
    buf += struct.pack("<HHB", x, y, b)
    s = stats[boroughs[b]]
    s["venues"] += 1
    s[["restaurants", "takeaways", "pubs", "other"][t]] += 1
    if ratings[r] == "5": s["five_star"] += 1
(OUT / "site/data/points.bin").write_bytes(bytes(buf))
meta = json.load(open(SRC / "boroughs.json"))
pop = {"Croydon": 409342, "Wandsworth": 337655, "Lambeth": 316920, "Lewisham": 301255, "Hackney": 266758, "Camden": 216943}
out = {"as_of": meta["as_of"], "source": "Food Standards Agency hygiene register via london-pulse (OGL v3.0)",
       "bbox": [LNG0, LNG1, LAT0, LAT1], "total_venues": len(rows), "boroughs": []}
for i, name in enumerate(boroughs):
    s = stats[name]; s["name"] = name; s["idx"] = i; s["pop_2024"] = pop.get(name)
    out["boroughs"].append(s)
json.dump(out, open(OUT / "site/data/boroughs.json", "w"), separators=(",", ":"))
# INTERNAL outreach list (never published): 5-star independents in launch boroughs
launch = {"Hackney", "Lewisham", "Lambeth"}
chains = ("mcdonald", "kfc", "subway", "starbucks", "costa", "pret", "greggs", "domino", "nando", "wetherspoon", "burger king", "pizza hut", "tesco", "sainsbury")
with open(OUT / "internal/outreach_prospects.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["borough", "type", "name", "postcode", "fsa_id"])
    n = 0
    for lng, lat, t, r, b, name, pc, i, f in rows:
        if boroughs[b] in launch and ratings[r] == "5" and not any(c in name.lower() for c in chains):
            w.writerow([boroughs[b], types[t], name, pc, i]); n += 1
print("points", len(rows), "bytes", len(buf), "prospects", n)
