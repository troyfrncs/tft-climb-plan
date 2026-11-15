#!/usr/bin/env python3
"""Fill data/meta.json "icons" with CommunityDragon image paths.

Run after editing meta.json:  python3 tools/icons.py
Optional: python3 tools/icons.py path/to/en_us.json  (skip the ~25 MB download)

It reads champion names from comps[].board / carry / items[].unit / positioning
and opener positioning, item names from comps[].items[].core, itemTiers and
families[].slamItems, and augment names from comps[].augmentTiers, then looks
each one up in the current set's CDragon data.
Names it can't find are listed at the end and fall back to text on the page.
"""
import json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "data" / "meta.json"
CDRAGON = "https://raw.communitydragon.org/latest/cdragon/tft/en_us.json"
BASE = "https://raw.communitydragon.org/latest/game/"
# Augment tier tags in CDragon data.
RARITY = {"{d11fd6d5}": "Silver", "{ce1fd21c}": "Gold", "{cf1fd3af}": "Prismatic"}


def png(path):
    if not path or path.startswith("{") or "missing" in path:
        return None
    return re.sub(r"\.(tex|dds)$", ".png", path.lower())


def dump(v, ind=0):
    """JSON with short arrays/objects kept on one line, like the hand-written file."""
    flat = json.dumps(v, ensure_ascii=False, separators=(", ", ": "))
    if not isinstance(v, (dict, list)) or len(flat) + ind <= 110:
        return flat.replace("{", "{ ", 1)[:-1] + " }" if isinstance(v, dict) and v else flat
    pad, inner = " " * ind, " " * (ind + 2)
    if isinstance(v, list):
        return "[\n" + ",\n".join(inner + dump(x, ind + 2) for x in v) + "\n" + pad + "]"
    return "{\n" + ",\n".join(f"{inner}{json.dumps(k, ensure_ascii=False)}: {dump(x, ind + 2)}"
                             for k, x in v.items()) + "\n" + pad + "}"


def load_cdragon():
    if len(sys.argv) > 1:
        return json.load(open(sys.argv[1], encoding="utf-8"))
    print("Downloading CommunityDragon data…")
    with urllib.request.urlopen(CDRAGON) as r:
        return json.load(r)


def main():
    meta = json.loads(META.read_text(encoding="utf-8"))
    cd = load_cdragon()
    set_no = int(meta["set"])
    set_champs = cd["sets"][str(set_no)]["champions"]
    set_data = next(s for s in cd["setData"] if s.get("number") == set_no)
    items_by_api = {i["apiName"]: i for i in cd["items"] if i.get("name")}

    # Champions: real shop units only (have traits, cost 1-5).
    champs = {}
    for c in set_champs:
        if c.get("traits") and 1 <= (c.get("cost") or 0) <= 5 and c["name"] not in champs:
            icon = png(c.get("tileIcon")) or png(c.get("squareIcon"))
            if icon:
                champs[c["name"]] = {"icon": icon, "cost": c["cost"]}

    def find(pool_ids, name):
        want = name.lower()
        hits = [items_by_api[a] for a in pool_ids if a in items_by_api
                and items_by_api[a]["name"].lower() == want]
        hits.sort(key=lambda i: (not png(i.get("icon")), not i["apiName"].startswith("TFT"), i["apiName"]))
        return hits[0] if hits else None

    def lookup(pool_ids, name):
        h = find(pool_ids, name)
        return png(h.get("icon")) if h else None

    # Collect names used in the content.
    unit_text, item_names, aug_names = [], set(), set()
    for f in meta.get("families", []):
        item_names.update(f.get("slamItems", []))
    for c in meta["comps"]:
        unit_text += c["board"] + [c["carry"]] + [i["unit"] for i in c["items"]]
        unit_text += [o["board"] for o in c.get("openers", [])]
        unit_text += [u[0] for u in c.get("positioning", {}).get("units", [])]
        unit_text += [u[0] for o in c.get("openers", []) for u in o.get("positioning", [])]
        for i in c["items"]:
            item_names.update(i.get("core", []))
        for tier in c.get("itemTiers", {}).values():
            item_names.update(tier)
        for tier in c.get("augmentTiers", {}).values():
            aug_names.update(tier)

    blob = " | ".join(unit_text)
    used_champs = {n: v for n, v in champs.items()
                   if re.search(r"(?<![\w'])" + re.escape(n) + r"(?![\w'])", blob)}

    icons = {"base": BASE, "champions": dict(sorted(used_champs.items())), "items": {}, "augments": {}}
    missing = []
    for n in sorted(item_names):
        p = lookup(set_data["items"], n) or lookup(items_by_api.keys(), n)
        (icons["items"].__setitem__(n, p) if p else missing.append(("item", n)))
    for n in sorted(aug_names):
        # "Bronze for Life" matches "Bronze For Life I" when there's no exact name.
        h = find(set_data["augments"], n) or find(set_data["augments"], n + " I")
        if not h:
            missing.append(("augment", n))
            continue
        rarity = next((RARITY[t] for t in h.get("tags", []) if t in RARITY), None)
        icons["augments"][n] = {"icon": png(h.get("icon")), "rarity": rarity}
        if not icons["augments"][n]["icon"]:
            missing.append(("augment", n))

    meta["icons"] = icons
    META.write_text(dump(meta) + "\n", encoding="utf-8")
    print(f"Wrote {len(icons['champions'])} champions, {len(icons['items'])} items, "
          f"{len(icons['augments'])} augments to {META.relative_to(ROOT)}")
    for kind, n in missing:
        print(f"  no icon for {kind}: {n} (shows as text)")


if __name__ == "__main__":
    main()
