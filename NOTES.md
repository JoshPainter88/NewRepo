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
