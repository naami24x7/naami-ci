import json, os
res = json.load(open("gallery_result.json"))
hot = {r["asin"]: r for r in json.load(open("hot.json"))["hot"]}
gal = res.get("results", {})
picked = []
for a, urls in gal.items():
    r = hot.get(a)
    if not r or len(urls) < 3:
        continue
    picked.append({
        "asin": a, "title": r["name"], "price": r["now"], "list_price": r["was"], "discount_percent": r["pct"],
        "rating": r.get("rating"), "reviews": r.get("reviews") or 0, "image": urls[0], "images": json.dumps(urls[:4]),
        "category": "deals", "link": r["link"], "bullets": (res.get("facts", {}).get(a) or {}).get("bullets", []),
    })
    if len(picked) == 3:
        break
print("gallery counts:", {a: len(u) for a, u in gal.items()}, "blocked:", res.get("blocked"))
print("picked:", [(p["asin"], len(json.loads(p["images"]))) for p in picked])
if len(picked) < 3:
    raise SystemExit("need 3 products with >=3 photos, got %d" % len(picked))
json.dump({"products": picked, "reel_id": "sample_photo_only", "style": "kenburns", "section": "discount",
           "audio_mode": None, "voice_gender": None, "whoosh": False}, open("payload.json", "w"))
