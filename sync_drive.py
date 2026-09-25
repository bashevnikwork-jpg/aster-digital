#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pull SkyBreeze content from a Google Sheet on Drive into content/*.json.

This is the daily Drive -> site bridge. A GitHub Actions workflow runs it, then
runs parts.py + build.py and commits any change, so the live site follows the
Sheet without anyone touching code. See CONTENT-EDITING.md for setup.

Design notes:
  * Read-only. It never writes to Drive.
  * Merge, not replace. A missing tab/row/cell keeps the value already committed,
    so a half-filled Sheet can never blank the site.
  * The Sheet is the source of truth for the fields it defines; everything else
    stays as-is in content/*.json.

Env:
  GOOGLE_SERVICE_ACCOUNT_JSON  service-account key (raw JSON or base64)
  SKYBREEZE_SHEET_ID           the spreadsheet id (from its URL)

Run: python3 sync_drive.py            (uses env)
     python3 sync_drive.py --check    (report changes, exit 1 if any, write nothing)
"""

import base64
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"

# ------------------------------------------------------------------ helpers

def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def dump(name, data):
    (CONTENT / name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def set_path(obj, dotted, value):
    """Set a nested key like 'hero.title' on a dict, creating dicts as needed."""
    keys = dotted.split(".")
    for k in keys[:-1]:
        obj = obj.setdefault(k, {})
    obj[keys[-1]] = value


def lines(cell):
    """Split a multi-line cell into a clean list (for checklist-style fields)."""
    return [l.strip() for l in str(cell).replace("\r", "").split("\n") if l.strip()]


def truthy(cell):
    return str(cell).strip().lower() in ("1", "true", "так", "yes", "y", "+", "featured")


# ------------------------------------------------------------------ Sheet schema
# Each key/value tab writes dotted paths into a target JSON file.
# Each table tab rebuilds a list. Columns are matched by header name (row 1).

# Key/value tabs. Each row's key is "file:dotted.path" (e.g. "sections:hero.title",
# "site:phone", "services:title"). The exporter fills these in; the editor only
# ever touches the value column, so the format stays out of their way.
KV_TABS = ["Settings", "Texts"]
KV_FILES = ("site.json", "sections.json", "services.json", "pricing.json",
            "portfolio.json", "faq.json", "motion.json", "stack.json")

# Tables: tab -> (file, json_path_to_list, row_builder)
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
    # merge_key: when set, each Sheet row is merged onto the committed item with the
    # same key, so nested fields the Sheet can't express (e.g. Motion branches) survive.
    ("Services", "services.json", "items", _services_row, "id"),
    ("Pricing", "pricing.json", "packages", _pricing_row, None),
    ("Portfolio", "portfolio.json", "cases", _portfolio_row, None),
    ("FAQ", "faq.json", "items", _faq_row, None),
    ("Process", "sections.json", "process.steps", _step_row, None),
    ("Advantages", "sections.json", "advantages.items", _adv_row, None),
    ("Mission", "sections.json", "mission.pillars", _step_row, None),
    ("After", "sections.json", "after.steps", _step_row, None),
]


def get_list(obj, dotted):
    for k in dotted.split("."):
        obj = obj.get(k, {}) if isinstance(obj, dict) else {}
    return obj if isinstance(obj, list) else []


# ------------------------------------------------------------------ Google API

def credentials():
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        sys.exit("GOOGLE_SERVICE_ACCOUNT_JSON is not set.")
    if not raw.lstrip().startswith("{"):
        raw = base64.b64decode(raw).decode("utf-8")
    info = json.loads(raw)
    from google.oauth2.service_account import Credentials
    return Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])


def read_sheet(svc, sheet_id, tab):
    """Return list-of-dicts (header row = keys) or None if the tab is absent."""
    try:
        res = svc.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=f"'{tab}'!A1:Z2000").execute()
    except Exception as e:
        if "Unable to parse range" in str(e) or "not found" in str(e).lower():
            return None
        raise
    values = res.get("values", [])
    if not values:
        return []
    header = [h.strip() for h in values[0]]
    rows = []
    for raw in values[1:]:
        raw = raw + [""] * (len(header) - len(raw))
        rows.append({header[i]: raw[i] for i in range(len(header))})
    return rows


# ------------------------------------------------------------------ main

def apply_kv(rows, files):
    """Key/value tab: 'file:dotted.path' -> value, routed to the right JSON file."""
    changed = 0
    for r in rows:
        key = (r.get("key") or r.get("Key") or "").strip()
        if not key or ":" not in key:
            continue
        fname, path = key.split(":", 1)
        fname = fname.strip() if fname.strip().endswith(".json") else fname.strip() + ".json"
        if fname not in files:
            continue
        val = r.get("value", r.get("Value", ""))
        set_path(files[fname], path.strip(), val)
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
            base.update(row)          # Sheet values win; unspecified nested fields survive
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
    sheet_id = os.environ.get("SKYBREEZE_SHEET_ID", "").strip()
    if not sheet_id:
        sys.exit("SKYBREEZE_SHEET_ID is not set.")

    from googleapiclient.discovery import build as gbuild
    svc = gbuild("sheets", "v4", credentials=credentials(), cache_discovery=False)

    # snapshot current files so we can diff / merge
    files = {name: load(name) for name in KV_FILES}
    before = {n: json.dumps(d, ensure_ascii=False, sort_keys=True) for n, d in files.items()}

    touched = []

    for tab in KV_TABS:
        rows = read_sheet(svc, sheet_id, tab)
        if rows is None:
            print(f"  · tab '{tab}' not found — skipping")
            continue
        n = apply_kv(rows, files)
        print(f"  · {tab}: {n} keys")

    for tab, fname, dotted, builder, merge_key in TABLE_TABS:
        rows = read_sheet(svc, sheet_id, tab)
        if rows is None:
            print(f"  · tab '{tab}' not found — skipping")
            continue
        ok = apply_table(rows, files[fname], dotted, builder, merge_key)
        print(f"  · {tab}: {'rebuilt ' + dotted if ok else 'empty — kept existing'}")

    for name, data in files.items():
        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if after != before[name]:
            touched.append(name)

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
