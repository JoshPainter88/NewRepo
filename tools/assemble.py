#!/usr/bin/env python3
"""Assemble the Cable Desk data file from the research outputs.

  python tools/assemble.py --kb private/kb --plaud private/research/plaud --owner private/owner.json --out private/kb/os_data.json

Inputs (all private, never committed):
  <kb>/projects.json      {"projects": [...]}
  <kb>/people.json        {"people": [...], "vendors": [...], "rhythm": [...]}
  <kb>/reference.json     {"rules_of_thumb": [...], "cable_catalog": [...], ...}
  <kb>/open_loops.json    {"loops": [...]}
  <kb>/design_brief.json  {...}
  <plaud>/B*.json         per-batch recording extractions -> the Calls log
  <owner>                 {"first": "...", "full": "...", "initials": "...", "org_short": "...", "program": "...", "context": "..."}

Personal, career and ambient recordings are dropped from the Calls log so the page stays safe to show a coworker.
"""
import argparse
import glob
import json
import os
import pathlib

WORK_KINDS = {"work_meeting", "work_call", "training", "town_hall"}


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def meetings_from(plaud_dir):
    out, seen, dropped, latest = [], set(), 0, ""
    for path in sorted(glob.glob(os.path.join(plaud_dir, "B*.json"))):
        batch = load(path, {}) or {}
        for r in batch.get("recordings", []):
            rid = r.get("id")
            if not rid or rid in seen:
                continue
            seen.add(rid)
            latest = max(latest, str(r.get("date") or ""))
            if r.get("personal_flag") or r.get("kind") not in WORK_KINDS:
                dropped += 1
                continue
            out.append({
                "id": rid,
                "title": r.get("title"),
                "date": r.get("date"),
                "start_time_utc": r.get("start_time_utc"),
                "duration_min": r.get("duration_min"),
                "kind": r.get("kind"),
                "projects": r.get("projects") or [],
                "people": [{"name": p.get("name"), "role_or_org": p.get("role_or_org")} if isinstance(p, dict) else {"name": p}
                           for p in (r.get("people") or []) if p],
                "summary": r.get("summary"),
                "topics": r.get("topics") or [],
                "decisions": r.get("decisions") or [],
                "action_items": r.get("action_items") or [],
                "facts": (r.get("facts") or [])[:25],
            })
    out.sort(key=lambda m: (str(m.get("date") or ""), str(m.get("start_time_utc") or "")), reverse=True)
    return out, dropped, latest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kb", required=True)
    ap.add_argument("--plaud", required=True)
    ap.add_argument("--owner", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sources", help="optional JSON describing where the data came from (kept in meta.sources)")
    ap.add_argument("--as-of", default=None)
    a = ap.parse_args()

    kb = pathlib.Path(a.kb)
    projects = load(kb / "projects.json", {}) or {}
    people = load(kb / "people.json", {}) or {}
    reference = load(kb / "reference.json", {}) or {}
    loops = load(kb / "open_loops.json", {}) or {}
    brief = load(kb / "design_brief.json", {}) or {}
    owner = load(a.owner, {}) or {}
    meetings, dropped, latest = meetings_from(a.plaud)

    reference = {k: v for k, v in reference.items() if k != "as_of"}
    data = {
        "meta": {
            "as_of": a.as_of or projects.get("as_of") or latest,
            "plaud_through": latest,
            "owner": owner,
            "sources": load(a.sources, {}) if a.sources else {},
            "counts": {"meetings": len(meetings), "personal_or_noise_dropped": dropped},
        },
        "projects": projects.get("projects", []),
        "people": people.get("people", []),
        "vendors": people.get("vendors", []),
        "rhythm": people.get("rhythm", []),
        "reference": reference,
        "loops": loops.get("loops", []),
        "meetings": meetings,
        "brief": brief,
    }
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"wrote {a.out}: {len(data['projects'])} projects, {len(data['people'])} people, {len(data['loops'])} loops, "
          f"{len(meetings)} calls ({dropped} personal/noise dropped), through {latest}")


if __name__ == "__main__":
    main()
