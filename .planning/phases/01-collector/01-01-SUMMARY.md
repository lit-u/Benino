---
phase: 01-collector
plan: 01
subsystem: infra
tags: [rss-parser, better-sqlite3, sqlite, news-collector, deduplication]

# Dependency graph
requires: []
provides:
  - rss-parser@3.13.0 and better-sqlite3@12.8.0 installed in agent-network
  - news-collector directory scaffold (sources/, storage/)
  - config.json with 10 AI/tech sources (COLL-04)
  - storage/db.js SQLite deduplication API: initDb, isSeen, markSeen (COLL-03)
  - news.db gitignored
affects:
  - 01-02 (RSS/API fetchers — imports config.json sources)
  - 01-03 (Scrapers — imports config.json sources)
  - 01-04 (Collector orchestrator — imports config.json + storage/db.js)

# Tech tracking
tech-stack:
  added:
    - rss-parser@3.13.0 (RSS feed parsing)
    - better-sqlite3@12.8.0 (synchronous SQLite, native addon)
  patterns:
    - "ESM-only: all imports use import/export (no require()), matching project type:module"
    - "Synchronous SQLite API via better-sqlite3 (no async/await needed for DB ops)"
    - "URL deduplication via SHA-256 hash (first 32 chars), trailing-slash normalized"

key-files:
  created:
    - agent-network/server/services/news-collector/config.json
    - agent-network/server/services/news-collector/storage/db.js
    - agent-network/server/services/news-collector/sources/.gitkeep
  modified:
    - agent-network/package.json
    - agent-network/package-lock.json
    - agent-network/.gitignore

key-decisions:
  - "TAAFT source uses type taaft-scrape (RSS URL broken per research)"
  - "HuggingFace Papers uses hf-papers-api type (official API more reliable than blog RSS)"
  - "URL hash is SHA-256, first 32 chars - sufficient collision resistance for news dedup"
  - "INSERT OR IGNORE used for idempotency — markSeen called twice is safe"

patterns-established:
  - "Pattern 1: Source config schema — id/name/type/url/enabled fields; type drives which fetcher handles it"
  - "Pattern 2: DB dedup API — initDb() returns db handle; isSeen/markSeen accept db as first arg"

requirements-completed: [COLL-03, COLL-04]

# Metrics
duration: 15min
completed: 2026-03-18
---

# Phase 1 Plan 01: Bootstrap News Collector Foundation Summary

**rss-parser + better-sqlite3 installed, 10-source config.json and SQLite dedup layer (initDb/isSeen/markSeen) bootstrapping the news-collector module**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-03-18T06:45:00Z
- **Completed:** 2026-03-18T06:59:50Z
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments
- Installed rss-parser@3.13.0 and better-sqlite3@12.8.0 with ESM imports verified
- Created news-collector directory scaffold (sources/, storage/) and gitignored news.db
- Authored config.json with exactly 10 AI/tech sources, correct types (taaft-scrape, hf-papers-api), and 6h cron
- Implemented storage/db.js with initDb/isSeen/markSeen, SHA-256 dedup, trailing-slash normalization, INSERT OR IGNORE idempotency — smoke test PASSED

## Task Commits

Each task was committed atomically:

1. **Task 1: Install dependencies and create directory scaffold** - `44662b0` (chore)
2. **Task 2: Write config.json with all 10 sources (COLL-04)** - `514377b` (feat)
3. **Task 3: Implement SQLite deduplication layer (COLL-03)** - `a075385` (feat)

**Plan metadata:** (created after this summary)

## Files Created/Modified
- `agent-network/server/services/news-collector/config.json` - 10-source config with pollIntervalCron, maxItemsPerSource, typed sources
- `agent-network/server/services/news-collector/storage/db.js` - SQLite dedup layer (initDb/isSeen/markSeen)
- `agent-network/server/services/news-collector/sources/.gitkeep` - Placeholder for sources directory
- `agent-network/package.json` - Added rss-parser@3.13.0 and better-sqlite3@12.8.0
- `agent-network/package-lock.json` - Updated lockfile
- `agent-network/.gitignore` - Added news.db ignore rule

## Decisions Made
- TAAFT source type set to `taaft-scrape` (RSS URL non-functional per research Pitfall 1)
- HuggingFace Papers set to `hf-papers-api` (official API more reliable than blog RSS)
- Node v24 uses `with {type: 'json'}` import attribute (not `assert`) — verified against v24.13.0

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Node v24.13.0 vs project engine spec `22.x`: generated a warning during npm install (not a blocker, no functionality impact). The `import ... assert {type:'json'}` syntax used in plan's verify command needed to be updated to `with {type:'json'}` for Node v24 compatibility — caught during verification, no code change required (db.js and config.json import correctly from application code).

## User Setup Required
None - no external service configuration required.

## Self-Check: PASSED

All required files verified on disk. All 3 task commits confirmed in git log.

## Next Phase Readiness
- Foundation complete: dependencies installed, config schema established, dedup storage API available
- Plan 02 (RSS/API fetchers) and Plan 03 (scrapers) can now proceed — they import config.json for source definitions
- Plan 04 (collector orchestrator) depends on both config.json and storage/db.js — both ready
- No blockers for Phase 1 continuation

---
*Phase: 01-collector*
*Completed: 2026-03-18*
