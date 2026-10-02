#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared content loader with code-level overrides.

`load(name)` reads content/<name> and then applies content/_overrides.json on
top — so anything set there is fixed IN CODE and the Google-Sheet sync can never
revert it. This is the "do it purely in code" fallback: edit _overrides.json,
commit, done; the value wins over whatever the Sheet says.

content/_overrides.json shape — per file, dotted paths (numbers index lists):

    {
      "services.json": { "items.1.price": "4 999 ₴" },
      "site.json":     { "phone": "+380 00 000 00 00" },
      "faq.json":      { "items.5.a": "..." }
    }

(Here items.1 is the 2nd service, items.5 the 6th FAQ — zero-based.)
"""

import json
import pathlib

CONTENT = pathlib.Path(__file__).parent / "content"


def _set_path(obj, dotted, value):
    keys = dotted.split(".")
    for k in keys[:-1]:
        obj = obj[int(k)] if isinstance(obj, list) else obj.setdefault(k, {})
    last = keys[-1]
    if isinstance(obj, list):
        obj[int(last)] = value
    else:
        obj[last] = value


def _overrides():
    f = CONTENT / "_overrides.json"
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load(name):
    data = json.loads((CONTENT / name).read_text(encoding="utf-8"))
    for path, value in (_overrides().get(name) or {}).items():
        try:
            _set_path(data, path, value)
        except Exception:
            pass  # a stale/bad override must never break the build
    return data
