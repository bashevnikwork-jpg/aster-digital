#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pull SkyBreeze content from a Google Sheet into content/*.json.

Daily Drive -> site bridge. A GitHub Actions workflow runs it, then runs
parts.py + build.py and commits any change, so the live site follows the Sheet
without anyone touching code. See CONTENT-EDITING.md.

Simple by design — NO Google Cloud, NO service account, NO secrets:
the Sheet is shared "anyone with the link can view", and each tab is read
through Google's public CSV export endpoint over plain HTTP (stdlib only).

Principles:
  * Read-only. Never writes to Drive.
  * Merge, not replace. A missing tab/row/cell keeps what's already committed,
    so a half-filled Sheet can never blank the site.

Config (first one found wins):
  env SKYBREEZE_SHEET_ID, or the file content/_sheet_id.txt  (the id from the
  Sheet URL: docs.google.com/spreadsheets/d/<THIS>/edit). Not secret.

Run: python3 sync_drive.py
     python3 sync_drive.py --check   (report changes, write nothing, exit 1 if any)
"""

import csv
import io
import json
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"

# ------------------------------------------------------------------ helpers

def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def dump(name, data):
    (CONTENT / name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def set_path(obj, dotted, value):
    keys = dotted.split(".")
    for k in keys[:-1]:
        obj = obj.setdefault(k, {})
    obj[keys[-1]] = value


def get_list(obj, dotted):
    for k in dotted.split("."):
        obj = obj.get(k, {}) if isinstance(obj, dict) else {}
    return obj if isinstance(obj, list) else []


def lines(cell):
    return [l.strip() for l in str(cell).replace("\r", "").split("\n") if l.strip()]


def truthy(cell):
    return str(cell).strip().lower() in ("1", "true", "так", "yes", "y", "+", "featured")


# ------------------------------------------------------------------ Sheet schema
KV_TABS = ["Settings", "Texts"]
KV_FILES = ("site.json", "sections.json", "services.json", "pricing.json",
            "portfolio.json", "faq.json", "motion.json", "stack.json")


def _services_row(r):
    row = {
        "id": r.get("id", ""), "index": r.get("index", ""), "code": r.get("code", ""),
        "nav": r.get("nav", ""), "navsub": r.get("navsub", ""), "title": r.get("title", ""),
        "tagline": r.get("tagline", ""), "price": r.get("price", ""), "term": r.get("term", ""),
        "what": r.get("what", ""), "why": r.get("why", ""), "gets": lines(r.get("gets", "")),
        "result": r.get("result", ""), "note": r.get("note") or None,
        "cta": r.get("cta", ""), "topic": r.get("topic", ""),
    }
    # 'branches' (the Motion sub-directions) is nested data the flat Sheet does not
    # carry — it is merged back from the committed JSON by id, see apply_table.
    if r.get("extra_price_label"):
        row["extra_price"] = {"label": r.get("extra_price_label", ""),
                              "price": r.get("extra_price_amount", ""),
                              "desc": r.get("extra_price_desc", "")}
    return row


def _pricing_row(r):
    return {
        "featured": truthy(r.get("featured", "")), "badge": r.get("badge") or None,
        "title": r.get("title", ""), "amount": r.get("amount", ""), "term": r.get("term", ""),
        "items": lines(r.get("items", "")), "note": r.get("note") or None,
        "cta": r.get("cta", ""), "topic": r.get("topic", ""),
    }


def _portfolio_row(r):
    return {
        "slug": r.get("slug", ""), "name": r.get("name", ""), "tag": r.get("tag", ""),
        "task": r.get("task", ""), "solution": r.get("solution", ""), "result": r.get("result", ""),
        "loading": r.get("loading", "lazy"), "live": r.get("live") or None, "video": r.get("video") or None,
    }


def _faq_row(r):
    return {"q": r.get("q") or r.get("question", ""), "a": r.get("a") or r.get("answer", "")}


def _step_row(r):
    return {"n": r.get("n", ""), "title": r.get("title", ""), "desc": r.get("desc", "")}


def _adv_row(r):
    return {"title": r.get("title", ""), "desc": r.get("desc", "")}


TABLE_TABS = [
    # (tab, file, dotted_list_path, row_builder, merge_key)
    ("Services", "services.json", "items", _services_row, "id"),
    ("Pricing", "pricing.json", "packages", _pricing_row, None),
    ("Portfolio", "portfolio.json", "cases", _portfolio_row, None),
    ("FAQ", "faq.json", "items", _faq_row, None),
    ("Process", "sections.json", "process.steps", _step_row, None),
    ("Advantages", "sections.json", "advantages.items", _adv_row, None),
    ("Mission", "sections.json", "mission.pillars", _step_row, None),
    ("After", "sections.json", "after.steps", _step_row, None),
]


# ------------------------------------------------------------------ fetch (no auth)

def sheet_id():
    import os
    env = os.environ.get("SKYBREEZE_SHEET_ID", "").strip()
    if env:
        return env
    f = CONTENT / "_sheet_id.txt"
    if f.exists():
        val = f.read_text(encoding="utf-8").strip()
        if val and not val.startswith("#"):
            return val
    sys.exit("No Sheet id — set env SKYBREEZE_SHEET_ID or write content/_sheet_id.txt")


def read_sheet(sid, tab):
    """Read a tab via the public CSV export. Returns list-of-dicts, or None if the
    tab is missing / the Sheet isn't link-viewable."""
    url = ("https://docs.google.com/spreadsheets/d/" + sid +
           "/gviz/tq?tqx=out:csv&sheet=" + urllib.parse.quote(tab))
    req = urllib.request.Request(url, headers={"User-Agent": "skybreeze-sync"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code in (400, 404):
            return None
        raise
    if data.lstrip().startswith("<"):        # HTML = tab not found or not shared
        return None
    rows = list(csv.reader(io.StringIO(data)))
    if not rows:
        return []
    header = [h.strip() for h in rows[0]]
    out = []
    for raw in rows[1:]:
        raw = raw + [""] * (len(header) - len(raw))
        out.append({header[i]: raw[i] for i in range(len(header))})
    return out


# ------------------------------------------------------------------ apply

def apply_kv(rows, files):
    changed = 0
    for r in rows:
        key = (r.get("key") or r.get("Key") or "").strip()
        if not key or ":" not in key:
            continue
        fname, path = key.split(":", 1)
        fname = fname.strip() if fname.strip().endswith(".json") else fname.strip() + ".json"
        if fname not in files:
            continue
        set_path(files[fname], path.strip(), r.get("value", r.get("Value", "")))
        changed += 1
    return changed


def apply_table(rows, obj, dotted, builder, merge_key=None):
    built = [builder(r) for r in rows if any(str(v).strip() for v in r.values())]
    if not built:
        return False
    if merge_key:
        existing = {it.get(merge_key): it for it in get_list(obj, dotted) if isinstance(it, dict)}
        merged = []
        for row in built:
            base = dict(existing.get(row.get(merge_key), {}))
            base.update(row)
            merged.append(base)
        built = merged
    keys = dotted.split(".")
    cur = obj
    for k in keys[:-1]:
        cur = cur.setdefault(k, {})
    cur[keys[-1]] = built
    return True


def main():
    check_only = "--check" in sys.argv
    sid = sheet_id()

    files = {name: load(name) for name in KV_FILES}
    before = {n: json.dumps(d, ensure_ascii=False, sort_keys=True) for n, d in files.items()}

    for tab in KV_TABS:
        rows = read_sheet(sid, tab)
        if rows is None:
            print(f"  · tab '{tab}' not found — skipping")
            continue
        print(f"  · {tab}: {apply_kv(rows, files)} keys")

    for tab, fname, dotted, builder, merge_key in TABLE_TABS:
        rows = read_sheet(sid, tab)
        if rows is None:
            print(f"  · tab '{tab}' not found — skipping")
            continue
        ok = apply_table(rows, files[fname], dotted, builder, merge_key)
        print(f"  · {tab}: {'rebuilt ' + dotted if ok else 'empty — kept existing'}")

    touched = [n for n, d in files.items()
               if json.dumps(d, ensure_ascii=False, sort_keys=True) != before[n]]

    if not touched:
        print("No content changes.")
        return 0

    print("Changed:", ", ".join(touched))
    if check_only:
        return 1
    for name in touched:
        dump(name, files[name])
    print("Wrote", len(touched), "file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
