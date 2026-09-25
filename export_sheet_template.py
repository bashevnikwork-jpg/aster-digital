#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write content/sheet-template/*.csv from the current content/*.json.

Run once to seed the Google Sheet: import each CSV into a tab of the same name
(File -> Import -> Upload -> "Insert new sheet"). After that the Sheet is the
source of truth and sync_drive.py pulls from it. See CONTENT-EDITING.md.

    python3 export_sheet_template.py
"""

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
OUT = CONTENT / "sheet-template"
OUT.mkdir(exist_ok=True)


def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def flatten_scalars(obj, prefix=""):
    """Yield (dotted_path, value) for every string leaf, skipping lists."""
    out = []
    for k, v in obj.items():
        path = f"{prefix}{k}"
        if isinstance(v, str):
            out.append((path, v))
        elif isinstance(v, dict):
            out.extend(flatten_scalars(v, path + "."))
        # lists are handled by table tabs — skip
    return out


def write_kv(name, pairs):
    with (OUT / f"{name}.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "value"])
        for k, v in pairs:
            w.writerow([k, v])
    print("  sheet-template/" + name + ".csv")


def write_table(name, cols, rows):
    with (OUT / f"{name}.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([r.get(c, "") for c in cols])
    print("  sheet-template/" + name + ".csv")


NL = "\n"

# ---- Settings tab: site.json scalars ----
site = load("site.json")
site_pairs = [(f"site:{p}", v) for p, v in flatten_scalars(site)]
write_kv("Settings", site_pairs)

# ---- Texts tab: prose scalars from every other file ----
text_pairs = []
for fname in ("sections.json", "services.json", "pricing.json", "portfolio.json",
              "faq.json", "motion.json", "stack.json"):
    stem = fname[:-5]
    text_pairs += [(f"{stem}:{p}", v) for p, v in flatten_scalars(load(fname))]
write_kv("Texts", text_pairs)

# ---- Services ----
sv = load("services.json")
srows = []
for s in sv["items"]:
    row = {k: s.get(k, "") for k in ("id", "index", "code", "nav", "navsub", "title",
                                      "tagline", "price", "term", "what", "why", "result",
                                      "note", "cta", "topic")}
    row["gets"] = NL.join(s.get("gets", []))
    ep = s.get("extra_price")
    if ep:
        row["extra_price_label"] = ep.get("label", "")
        row["extra_price_amount"] = ep.get("price", "")
        row["extra_price_desc"] = ep.get("desc", "")
    srows.append(row)
write_table("Services", ["id", "index", "code", "nav", "navsub", "title", "tagline",
                         "price", "term", "what", "why", "gets", "result", "note",
                         "cta", "topic", "extra_price_label", "extra_price_amount",
                         "extra_price_desc"], srows)

# ---- Pricing ----
pc = load("pricing.json")
prows = []
for p in pc["packages"]:
    prows.append({"featured": "true" if p.get("featured") else "", "badge": p.get("badge") or "",
                  "title": p.get("title", ""), "amount": p.get("amount", ""), "term": p.get("term", ""),
                  "items": NL.join(p.get("items", [])), "note": p.get("note") or "",
                  "cta": p.get("cta", ""), "topic": p.get("topic", "")})
write_table("Pricing", ["featured", "badge", "title", "amount", "term", "items", "note", "cta", "topic"], prows)

# ---- Portfolio ----
pf = load("portfolio.json")
write_table("Portfolio", ["slug", "name", "tag", "task", "solution", "result", "loading", "live", "video"],
            [{k: (c.get(k) or "") for k in ("slug", "name", "tag", "task", "solution", "result", "loading", "live", "video")}
             for c in pf["cases"]])

# ---- FAQ ----
fq = load("faq.json")
write_table("FAQ", ["q", "a"], [{"q": i["q"], "a": i["a"]} for i in fq["items"]])

# ---- Process / Advantages / Mission / After (from sections.json) ----
sec = load("sections.json")
write_table("Process", ["n", "title", "desc"], sec["process"]["steps"])
write_table("Advantages", ["title", "desc"], sec["advantages"]["items"])
write_table("Mission", ["n", "title", "desc"], sec["mission"]["pillars"])
write_table("After", ["n", "title", "desc"], sec["after"]["steps"])

print("done —", OUT)
