---
phase: 03-telegram-bot
plan: "01"
subsystem: news-collector
tags: [sqlite, schema-migration, wal, telegram, config, tdd-scaffold]
dependency_graph:
  requires: []
  provides: [tg_status-column, tg_message_id-column, telegram-config, tg-test-scaffold]
  affects: [news-collector/storage/db.js, news-collector/config.json, tests/news-collector]
tech_stack:
  added: []
  patterns: [addIfMissing-migration, WAL-pragma]
key_files:
  created:
    - agent-network/tests/news-collector/tg-handlers.test.mjs
  modified:
    - agent-network/server/services/news-collector/storage/db.js
    - agent-network/server/services/news-collector/config.json
decisions:
  - WAL pragma added immediately after Database() constructor — prevents SQLITE_BUSY when bot and collector share the DB file
  - telegram.batchDelayMs=1000ms chosen for safe Telegram rate limiting (30/sec limit, 1/sec conservative)
  - Test scaffold uses in-memory SQLite with full schema — no filesystem artifacts, fast, Wave 2 ready
metrics:
  duration: 4min
  completed_date: "2026-03-18"
  tasks_completed: 2
  files_modified: 3
---

# Phase 3 Plan 01: SQLite Schema Migration and Telegram Config Scaffold

SQLite schema extended with tg_status/tg_message_id columns and WAL mode, config.json has telegram dispatch block, TDD test scaffold ready for Wave 2 handlers.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Add tg_status and tg_message_id columns to db.js schema migration | a43975a | storage/db.js |
| 2 | Add telegram block to config.json and create test scaffold | 49a5bb5 | config.json, tests/news-collector/tg-handlers.test.mjs |

## What Was Built

**Task 1 — db.js Schema Migration:**
- Added `db.pragma('journal_mode = WAL')` immediately after `new Database(DB_PATH)` — prevents `SQLITE_BUSY` errors when the Telegram bot's persistent connection writes concurrently with the collector
- Added `addIfMissing('tg_status', 'TEXT')` — tracks dispatch state per item (null / 'pending' / 'accepted' / 'rejected')
- Added `addIfMissing('tg_message_id', 'INTEGER')` — stores Telegram message ID for callback_query routing in Wave 2
- Migration is idempotent (try/catch on ALTER TABLE, same as existing columns)

**Task 2 — Config and Test Scaffold:**
- `config.json` telegram block: `batchSize=10`, `batchDelayMs=1000ms`, `dispatchCutoffMs=86400000` (24h cutoff prevents sending old items on first run)
- Test scaffold at `tests/news-collector/tg-handlers.test.mjs`:
  - `createTestDb()` creates in-memory DB with complete seen_urls schema including tg columns
  - Inserts one test row with realistic data (score=75, item_type='release', threshold_pass=1)
  - Two TODO placeholder functions ready for Wave 2 handler imports
  - Runs without errors and prints "Scaffold loaded OK"

## Verification Results

```
["url_hash","url","title","source_id","seen_at","score","item_type","threshold_pass","scored_at","tg_status","tg_message_id"]
```
Both columns present in live news.db. Test scaffold exits 0.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED

- agent-network/server/services/news-collector/storage/db.js — FOUND, contains tg_status, tg_message_id, journal_mode = WAL
- agent-network/server/services/news-collector/config.json — FOUND, contains telegram block
- agent-network/tests/news-collector/tg-handlers.test.mjs — FOUND, runs cleanly
- Commit a43975a — FOUND
- Commit 49a5bb5 — FOUND
