# Personal OS — build log

Running log so work can resume from any point. **This repo is public**: this file holds
process/progress only. Confidential findings live in `private/` (git-ignored, local only).

## Goal
A personal "OS" dashboard for Josh: everything needed regularly and at a moment's notice,
deep drill-down, ADHD-friendly (low noise, one-thing-at-a-time, fast recall), high aesthetic quality.

## Constraints discovered
- Session runs in a cloud container; `C:\Work\PRIMORIS ACTIVE FOLDER 8.21.26` is NOT reachable
  (Desktop Commander connector timed out). Plan: ship a local Windows indexer script the user runs.
- Data sources reachable: Plaud recordings (transcripts + AI notes), Google Drive (call library).
- Repo is PUBLIC → app code + scripts + sample data only. Real data stays in `private/` and in
  a private claude.ai Artifact.

## Progress
- [x] 2026-10-12 Recon: Plaud has ~50+ recent work recordings (Sep–Oct 2026); Drive has a
      transcript "Call library" with archive/cleanup folders.
- [x] Inventory: ~200 Plaud recordings (Jun→Oct); Drive 'New Primoris folder 8.21.26' mapped (curated
      desk/open-items/meeting-log docs, reel-plan guides, prior HTML dashboard attempts).
      Scope: deep-extract Aug 1 → Oct 12 (current role); earlier = titles only.
- [ ] Extract (workflow fan-out) → `private/research/*.json`
- [ ] Synthesize knowledge base → `private/kb.json`
- [ ] Design + build app (`app/`)
- [ ] Windows indexer for C:\Work folder (`tools/`)
- [ ] Review pass (UX/ADHD, aesthetics, accuracy, bugs) + fixes
- [ ] Publish private Artifact; push code; draft PR

## Design plan (2026-10-12)
**Form:** one self-contained HTML app (vanilla JS, no build deps, works offline). Two deployments:
1. Private claude.ai Artifact (real data embedded; db = synced check-offs/inbox/notes; sample = "Ask"; mcp = live Plaud feed).
2. Local file on the Windows PC (same app; localStorage instead of db; optional C:\Work file index).

**Source layout:** `app/src/{shell.html,styles.css,app.js}` + data → `tools/build.py` inlines → `dist/*.html` (git-ignored when real data).
`app/sample-data.json` = clearly fictional demo data for the public repo.

**Views:** Today (one focus + next 3 + today's meetings + waiting-on + project pulse + capture) · Projects → project detail
(overview, numbers, cable scope, loops, timeline, risks, people, docs, meetings, notes) · People → person + prep sheet ·
Loops (I owe / waiting on) · Field Guide (rules of thumb, cable catalog, processes, glossary, calculators, key docs) ·
Meetings log · Inbox · Ask · Files (local only).
**Global:** command palette (Ctrl+K or /), focus mode with timer (F), quick capture (C), prep sheet (P), g-key navigation.
**ADHD rules:** one primary action per view; summary before detail; top 5 then "show all"; colour only for attention;
consistent positions; calm motion (respects reduced-motion).
**Look:** cool steel neutrals + copper accent (conductor), XLPE blue-black dark theme; condensed display face for labels,
Atkinson Hyperlegible for reading; signature "cable jacket print" strip with footage counter; design-stage reel rings.

**KB contract** (`window.OS_DATA`): meta, projects[], people[], vendors[], rhythm[], reference{rules_of_thumb, cable_catalog,
processes, glossary, formulas, tools, key_docs, pricing_and_commercial}, loops[], meetings[], brief{}, files[] (optional).
