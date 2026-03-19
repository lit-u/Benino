---
phase: 04-writer-publisher
plan: "04"
subsystem: news-collector
tags: [config-wiring, telegram-bot, writer-pipeline, gap-closure]
dependency_graph:
  requires: [04-03]
  provides: [WRIT-04, PUBL-01]
  affects: [agent-network/server/routes/news.js, agent-network/server/services/news-collector/telegram/handlers.js]
tech_stack:
  added: []
  patterns: [createRequire config injection, ctx.editMessageText confirmation, MarkdownV2 escaping]
key_files:
  created: []
  modified:
    - agent-network/server/routes/news.js
    - agent-network/server/services/news-collector/telegram/handlers.js
decisions:
  - "cfg loaded via createRequire (not dynamic import) — synchronous, consistent with existing require on line 15"
  - "MarkdownV2 escaping applied to all dynamic text in editMessageText — Telegram rejects unescaped special chars"
  - "handleAccept returns { ok, data } — testable result instead of void, unit tests can assert pipeline outcome"
metrics:
  duration: 3min
  completed: 2026-03-19
  tasks: 2
  files_modified: 2
---

# Phase 4 Plan 4: Config wiring and Telegram confirmation Summary

Config.json writer.model wired into news.js accept route via createRequire; Telegram handler parses accept response and sends draft title + path to admin via ctx.editMessageText.

## Tasks Completed

| # | Task | Commit | Files |
|---|------|--------|-------|
| 1 | Wire config.json into news.js accept route | 8db7915 | server/routes/news.js |
| 2 | Wire Telegram confirmation after accept pipeline | a765f1f | telegram/handlers.js |

## What Was Built

**Task 1 — Config wiring (news.js):**
- Added `const cfg = require('../services/news-collector/config.json');` after the already-declared `const require = createRequire(import.meta.url);`
- Changed `generateNewsPost(item, {})` to `generateNewsPost(item, cfg)` — the single-line bug causing the empty config pass-through
- Result: `writer.model` in config.json now flows through to the LLM call without any code edits required

**Task 2 — Telegram confirmation (handlers.js):**
- Replaced Phase 4 stub block with full response parsing: `await res.json()` called on the fetch response
- On success (`res.ok && data.success`): `ctx.editMessageText` replaces the "Generuojama..." spinner with draft title and path
- On API error: shows the error message from the response body
- On network/parse error: catch block shows generic "Klaida generuojant draft" message
- `handleAccept` export updated: now returns `{ ok, data }` instead of void — unit tests can assert the pipeline result
- All dynamic text escaped for MarkdownV2 (Telegram requirement)
- Removed all stale "Phase 4 stub" and "Phase 4 not yet implemented" comments

## Verification Results

All 6 plan verification checks passed:
1. `generateNewsPost(item, cfg)` present in news.js
2. `generateNewsPost(item, {})` absent from news.js
3. `require('../services/news-collector/config.json')` present in news.js
4. `editMessageText` count = 4 in handlers.js (success + error paths in both bot.action and export)
5. `res.json()` present in handlers.js
6. `Phase 4 stub` absent from handlers.js

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check: PASSED

- SUMMARY.md exists at .planning/phases/04-writer-publisher/04-04-SUMMARY.md
- Commit 8db7915 exists (Task 1: config wiring)
- Commit a765f1f exists (Task 2: Telegram confirmation)
