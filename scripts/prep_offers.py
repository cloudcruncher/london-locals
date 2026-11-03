"""Validate internal/offers_raw.json and write site/data/offers.json (only https source URLs, no personal data)."""
import json, pathlib, re, sys
R = pathlib.Path(__file__).resolve().parent.parent
raw = json.load(open(R / "internal/offers_raw.json"))
keys = ["name","borough","neighbourhood","type","offer_title","offer_detail","conditions","source_url","checked_on"]
ok, seen = [], set()
for o in raw:
    if not all(o.get(k) is not None for k in keys[:5]+["source_url","checked_on"]): continue
    if o["borough"] not in ("Hackney","Lewisham","Lambeth"): continue
    if not re.match(r"^https://", o["source_url"]): continue
    if o.get("confidence") not in ("high","medium"): continue
    k=(o["name"].lower(),o["offer_title"].lower())
    if k in seen: continue
    seen.add(k); ok.append({k2:o.get(k2,"") for k2 in keys})
ok.sort(key=lambda o:(o["borough"],o["name"]))
(R/"site/data/offers.json").write_text(json.dumps({"checked_on":__import__("datetime").date.today().isoformat(),"offers":ok},indent=1,ensure_ascii=False))
print(len(ok),"offers written", file=sys.stderr)
