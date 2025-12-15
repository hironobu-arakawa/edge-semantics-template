#!/usr/bin/env python3
"""
Edge Semantics Resolver (Slim PoC)

Purpose:
- Demonstrate SAFE behavior when connection/schema changes are detected.
- Be readable without domain knowledge.

This PoC:
- compares schema_hash in Facts with a baseline
- outputs Resolution with state=degraded if changed
- never auto-fixes meanings
"""

import json, argparse
from datetime import datetime, timezone

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def key(site, endpoint, tag):
    return f"{site}|{endpoint}|{tag}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--facts", required=True)
    ap.add_argument("--hypotheses", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    facts = load_jsonl(args.facts)
    hyps  = load_jsonl(args.hypotheses)
    baseline = json.load(open(args.baseline, encoding="utf-8"))

    resolutions = []

    for h in hyps:
        sel = h["fact_ref"]["selector"]
        k = key(sel.get("site",""), sel.get("endpoint",""), sel["tag_raw"])

        latest = next((f for f in facts if f["signal"]["tag_raw"]==sel["tag_raw"]), None)
        if not latest:
            continue

        schema_hash = latest.get("fingerprint",{}).get("schema_hash")
        base_hash   = baseline.get(k,{}).get("schema_hash")

        state = "active" if schema_hash == base_hash else "degraded"

        resolutions.append({
            "resolution_id": "demo",
            "scope": "example",
            "selector": sel,
            "resolved": {
                "attribute": h["proposal"]["value"]
            },
            "state": state,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "diagnostics": {
                "schema_hash": schema_hash,
                "baseline": base_hash
            }
        })

    with open(args.out, "w", encoding="utf-8") as f:
        for r in resolutions:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
