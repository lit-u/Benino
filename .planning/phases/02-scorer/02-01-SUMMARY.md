---
phase: 02-scorer
plan: "01"
subsystem: news-collector/scorer
tags: [sqlite, schema-migration, config, test-scaffold]
dependency_graph:
  requires: []
  provides: [scorer-schema, scorer-config, scorer-test-scaffold]
  affects: [news-collector/storage/db.js, news-collector/config.json, news-collector/scorer/test-scorer.js]
tech_stack:
  added: []
  patterns: [addIfMissing-migration, try-catch-ALTER-TABLE, createRequire-ESM-JSON]
key_files:
  created:
    - agent-network/server/services/news-collector/scorer/test-scorer.js
  modified:
    - agent-network/server/services/news-collector/storage/db.js
    - agent-network/server/services/news-collector/config.json
    - agent-network/.env.example
decisions:
  - Import paths in scorer/test-scorer.js use relative paths from scorer/ directory (../config.json, ./heuristics.js)
  - addIfMissing() wraps ALTER TABLE in try/catch — SQLite silently ignores duplicate columns via exception
metrics:
  duration: "~8min"
  completed: "2026-03-18T08:22:06Z"
  tasks_completed: 2
  files_modified: 4
---

# Phase 2 Plan 01: Scorer Schema + Config + Test Scaffold Summary

**One-liner:** SQLite schema extended with 4 scorer columns via try/catch ALTER TABLE, scoring config block added (threshold=50, llmModel=gemini-2.0-flash), and test-scorer.js scaffold created with SCOR-01..05 stubs.

## Tasks Completed

| # | Task | Commit | Files |
|---|------|--------|-------|
| 1 | Extend initDb() with scorer columns + index | 4772481 | storage/db.js |
| 2 | config.json scoring block + .env.example + test-scorer.js | 40c3cef | config.json, .env.example, scorer/test-scorer.js |

## Decisions Made

1. **addIfMissing pattern** — ALTER TABLE wrapped in try/catch since SQLite does not support IF NOT EXISTS on column additions. Existing databases migrate safely; new databases get columns from CREATE TABLE.

2. **Relative import paths in scorer/test-scorer.js** — File lives inside scorer/ subdirectory, so config.json is at `../config.json` and sibling modules are at `./heuristics.js`, `./index.js`. Plan specified `./scorer/heuristics.js` (written from the news-collector root perspective), but that would fail when the file runs from its own location — auto-fixed as Rule 1.

3. **idx_threshold composite index** — (threshold_pass, scored_at) prepared for Phase 3 query pattern: "items that passed threshold not yet sent."

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Import paths in test-scorer.js corrected for file location**
- **Found during:** Task 2 verification
- **Issue:** Plan specified `./scorer/heuristics.js` and `./scorer/index.js` for dynamic imports, and `./config.json` for require(). These paths are correct from the news-collector root but wrong when the file itself runs from inside scorer/.
- **Fix:** Changed to `../config.json`, `./heuristics.js`, `./index.js`
- **Files modified:** scorer/test-scorer.js
- **Commit:** 40c3cef

## Verification Results

```
PENDING: scorer/heuristics.js not yet created
PENDING: scorer/index.js not yet created
PASS SCOR-05: threshold=50

Test scaffold ready. Re-run after each wave to check PASS/PENDING counts.
```

- config.scoring.threshold = 50 (confirmed)
- config.scoring.llmModel = "google/gemini-2.0-flash-001" (confirmed)
- All 4 columns (score, item_type, threshold_pass, scored_at) present in seen_urls
- idx_threshold index present

## Self-Check: PASSED

Files exist:
- FOUND: agent-network/server/services/news-collector/storage/db.js
- FOUND: agent-network/server/services/news-collector/config.json
- FOUND: agent-network/server/services/news-collector/scorer/test-scorer.js
- FOUND: agent-network/.env.example

Commits exist:
- FOUND: 4772481
- FOUND: 40c3cef
