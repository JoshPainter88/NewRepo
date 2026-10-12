# Cable Desk

A personal operating system for running a cable-procurement program: everything you need regularly, everything you need on a moment's notice, and nothing else on screen. Built to be calm and fast for someone with ADD.

![views](https://img.shields.io/badge/views-Today%20%C2%B7%20Projects%20%C2%B7%20People%20%C2%B7%20Loops%20%C2%B7%20Field%20Guide%20%C2%B7%20Calls%20%C2%B7%20Inbox%20%C2%B7%20Ask-a3521d)

## What it does

| View | What you get |
|---|---|
| **Today** | Your one thing (with a focus timer), the next few things you owe, today's recurring meetings with one-click prep, who owes you, the next 14 days, project pulse, quick capture. |
| **Projects** | Every job with status, health, design stage ring, open loops and next milestone. Drill into overview, key numbers, cable scope, risks, loops, timeline of decisions, calls, people, docs, files and notes. |
| **People** | Who they are, how you work together, what you owe each other, every call you had. **Prep sheet** (P) for any person or project, with optional talking points from Claude. |
| **Loops** | Commitments pulled from your calls and desk docs: *You owe* and *Waiting on*, grouped This week / Soon / Later. Check off, undo, add your own. |
| **Field Guide** | Rules of thumb, cable catalog, processes, glossary, key docs, commercial terms, and calculators (reel order quantity; master reel vs cut-to-length). |
| **Calls** | Every recorded work call by week, with decisions, actions and numbers. In the claude.ai version, **New recordings** pulls fresh Plaud calls and briefs you on any of them. |
| **Inbox** | Capture now (C anywhere), sort later, turn captures into loops. |
| **Ask** | Ask Claude about your projects, people, numbers and rules (claude.ai version). |
| **Files** | Search and open anything in your work folder (local version, after running the indexer). |

Everywhere: **Ctrl K** or **/** finds anything (Tab sends the query to Claude), **F** focus mode, **C** capture, **g then t/p/e/l/r/m/i/a** to jump, **?** for all keys.

## Privacy model

This repository is public, so it holds **code and fictional demo data only**.

- Your real data (projects, people, loops, calls) is assembled privately from your recordings and Drive, embedded into a **private** claude.ai artifact, and never committed. `private/`, `dist/` and `cabledesk-files.js` are git-ignored.
- Personal, career and HR recordings are dropped from the data before it is built.
- Check-offs, captures and notes sync through the artifact's private per-user store, or stay in your browser's local storage in the local copy.
- The file indexer records names, folders, dates and sizes only. It never reads file contents, and nothing leaves your PC.

## Use it

**On claude.ai (recommended):** open your private Cable Desk artifact. Sync, Ask and New recordings work there.

**On your PC (offline, with file search):**
1. Put `cable-desk.html`, `tools/Build-FileIndex.ps1` and `tools/Start-CableDesk.cmd` in one folder, e.g. `C:\Work\CableDesk\`.
2. Double-click `Start-CableDesk.cmd`. It indexes `C:\Work` (point it at one folder with `-Root "C:\Work\Your Folder"`) and opens the page.

**Try the demo:** `python tools/build.py --data app/sample-data.json --out dist/demo.html`, then open `dist/demo.html`.

## Build from your own data

```bash
# 1. research outputs -> one data file (see tools/assemble.py for the inputs it expects)
python tools/assemble.py --kb private/kb --plaud private/research/plaud --owner private/owner.json --out private/kb/os_data.json
# 2. data + app -> one HTML file
python tools/build.py --data private/kb/os_data.json --out dist/cable-desk.html             # local copy
python tools/build.py --data private/kb/os_data.json --out dist/artifact.html --artifact    # claude.ai artifact body
```

Keeping it current is described in [docs/REFRESH.md](docs/REFRESH.md).

## Data contract

`window.OS_DATA` is one JSON object:

| Key | Shape |
|---|---|
| `meta` | `as_of`, `plaud_through`, `owner {first, full, initials, org_short, program, context}` |
| `projects[]` | `id, name, aliases, type, client_or_owner, location, status, health, design_stage, my_role, current_focus, status_note, next_milestones[], cable_scope{}, key_numbers[], risks[], decisions[], timeline[], people[], vendors[], drive_links[]` |
| `people[]` | `id, name, aliases, org, role, relationship, projects, topics, last_seen, interaction_count, tips` |
| `vendors[]`, `rhythm[]` | distributors and partners; recurring meetings (`name, cadence, day_time, attendees, purpose`) |
| `reference{}` | `rules_of_thumb, cable_catalog, processes, glossary, formulas, tools, key_docs, pricing_and_commercial` |
| `loops[]` | `id, text, detail, direction (i_owe/owed_to_me/team), counterparty, project, due, status, priority (now/soon/later)` |
| `meetings[]` | `id, title, date, duration_min, kind, projects, people, summary, decisions, action_items, facts` |

`window.OS_FILES` (optional) is written by the indexer: `{root, indexed_at, files: [{p, m, s}]}`.

## Layout

```
app/src/        shell.html, styles.css, app.js (no dependencies)
app/sample-data.json   fictional demo data
tools/build.py         inline app + data into one HTML file
tools/assemble.py      research outputs -> data file
tools/Build-FileIndex.ps1, tools/Start-CableDesk.cmd   Windows file index + launcher
docs/REFRESH.md        how to keep the desk current
NOTES.md               build log
```
