---
phase: 01-collector
plan: "04"
subsystem: news-collector
tags: [collector, orchestrator, cron, dedup, dispatch-router]
dependency_graph:
  requires: [01-02, 01-03]
  provides: [collector-orchestrator, source-dispatch-router]
  affects: [01-05]
tech_stack:
  added: []
  patterns: [ESM-createRequire-for-JSON, per-source-try-catch-isolation, SQLite-dedup-pattern]
key_files:
  created:
    - agent-network/server/services/news-collector/sources/index.js
    - agent-network/server/services/news-collector/index.js
  modified: []
decisions:
  - createRequire used for JSON config import (reliable across all Node.js ESM versions)
  - db.close() called at end of each runCollector() invocation to avoid connection leaks
metrics:
  duration: 8min
  completed_date: "2026-03-18"
  tasks_completed: 2
  files_created: 2
  files_modified: 0
---

# Phase 1 Plan 04: Collector Orchestrator Summary

**One-liner:** Wired all 10 sources into a single runCollector() orchestrator with per-source error isolation, SQLite dedup (994 items on first run, 0 new on second), and node-cron scheduling.

## What Was Built

### Task 1 — Source dispatch router (sources/index.js)
Maps all 7 source type strings from config.json to their fetcher functions via a FETCHERS lookup table. Throws a descriptive error for unknown types. Single export: `fetchSource(source)`.

Covered types:
- `rss` → fetchRss
- `hf-papers-api` → fetchHuggingFacePapers
- `hf-models-api` → fetchHuggingFaceModels
- `hn-algolia` → fetchHackerNews
- `github-trending` → fetchGithubTrending
- `github-search` → fetchGithubSearch
- `taaft-scrape` → fetchTaaft

### Task 2 — Collector orchestrator (index.js)
`runCollector()` iterates all enabled sources, calls `fetchSource()` per source inside a try/catch. For each fetched item: `isSeen()` check before `markSeen()`. Returns `{fetched, new, skipped, errors}`. `registerCron()` schedules via `node-cron` using `config.pollIntervalCron`.

## Smoke Test Results

```
First run (fresh DB):  fetched:994 new:994   skipped:0   errors:0  (14.5s)
Second run (dedup):    fetched:994 new:0     skipped:994 errors:0  (4.6s)
```

Dedup confirmed: `r2.new === 0` and `r2.skipped === r1.new`.

## Deviations from Plan

None — plan executed exactly as written.

## Commits

| Hash | Task | Description |
|------|------|-------------|
| 2d15299 | Task 1 | feat(01-04): source dispatch router (sources/index.js) |
| 305694d | Task 2 | feat(01-04): collector orchestrator with runCollector and registerCron |

## Self-Check: PASSED

- sources/index.js: FOUND
- index.js: FOUND
- Commit 2d15299: FOUND
- Commit 305694d: FOUND
