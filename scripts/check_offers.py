"""Check every offer source URL still loads and still mentions the venue. Exit 1 if any fail."""
import json, pathlib, sys, urllib.request
R = pathlib.Path(__file__).resolve().parent.parent
offers = json.load(open(R / "site/data/offers.json"))["offers"]
bad = []
for u in sorted({o["source_url"] for o in offers}):
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (offer-link-check; contact: see site)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read(400000).decode("utf-8", "ignore").lower()
        names = [o["name"].split(" (")[0].lower() for o in offers if o["source_url"] == u]
        if not any(n.split()[0] in body for n in names):
            bad.append((u, "venue name not found on page"))
    except Exception as e:
        bad.append((u, str(e)[:60]))
for u, why in bad:
    print("CHECK:", u, "-", why)
print(f"{len(bad)} of {len({o['source_url'] for o in offers})} source pages need a look")
sys.exit(1 if bad else 0)
