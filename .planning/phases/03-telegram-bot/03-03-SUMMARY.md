---
phase: 03-telegram-bot
plan: "03"
subsystem: news-collector
tags: [telegraf, telegram, integration, express, dispatcher, bot-polling]
dependency_graph:
  requires:
    - phase: "03-02"
      provides: runTelegramDispatch, startBotPolling, bot.js, dispatcher.js, handlers.js, card.js
  provides:
    - runTelegramDispatch wired into runCollector() 3-stage pipeline
    - POST /api/news/accept/:hash stub route returning 501
    - startBotPolling() called on server boot inside !isVercelRuntime block
  affects: [phase-04-writer, server-index]
tech_stack:
  added: []
  patterns: [fresh-db-connection-per-stage, vercel-guard-inherited, route-stub-501]
key_files:
  modified:
    - agent-network/server/services/news-collector/index.js
    - agent-network/server/index.js
  created:
    - agent-network/server/routes/news.js
key_decisions:
  - "runTelegramDispatch(tgDb) uses fresh db3 connection — same fresh-connection pattern as runScorer; prevents SQLite busy/locked conflict"
  - "startBotPolling() is inside app.listen which is inside !isVercelRuntime guard — no extra guard needed"
  - "TELEGRAM_BOT_TOKEN not added to startup logs — per Phase 3 research pitfall 5 (bot token must never appear in logs)"
  - "news route mounted next to other bot integration routes (/api/moderation, /api/bot) for logical grouping"
requirements-completed: [TG-01, TG-02, TG-03, TG-04, TG-05]
duration: 7min
completed: "2026-03-18"
---

# Phase 3 Plan 03: Integration & Server Wiring Summary

**Full Phase 3 Telegram integration wired into Express server: 3-stage pipeline (collect → score → dispatch), bot polling on startup, and Phase 4 accept stub route in place.**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-18T12:01:00Z
- **Completed:** 2026-03-18T12:08:06Z
- **Tasks:** 2 (+ 1 human-verify checkpoint)
- **Files modified:** 3

## Accomplishments

- `runCollector()` now runs a 3-stage pipeline: collect → score → dispatch, each with its own fresh SQLite connection
- `runTelegramDispatch(tgDb)` called at the end of every collector run with a fresh db3 connection
- `server/routes/news.js` created with POST `/api/news/accept/:hash` stub returning 501 (Phase 4 ready)
- `server/index.js` imports and mounts `newsRoutes` at `/api/news`
- `startBotPolling()` called inside `app.listen` callback — Vercel-guarded by the enclosing `if (!isVercelRuntime)` block
- Bot token never appears in server startup logs
- All 3 TDD tests from Plan 02 still pass after wiring

## Task Commits

Each task was committed atomically:

1. **Task 1: Wire runTelegramDispatch + create stub news route** - `a1c7cbb` (feat)
2. **Task 2: Register bot polling and news route in server/index.js** - `ceb7597` (feat)

## Files Created/Modified

- `server/services/news-collector/index.js` — Added `runTelegramDispatch` import; added 3rd pipeline stage with `tgDb` fresh connection
- `server/routes/news.js` (NEW) — POST `/api/news/accept/:hash` stub returning 501 with JSON body
- `server/index.js` — Added `startBotPolling` + `newsRoutes` imports; mounted `/api/news`; added `startBotPolling()` call in `app.listen`

## Decisions Made

- `runTelegramDispatch(tgDb)` uses a fresh `db3` connection — same pattern established in Phase 2 for scorer; prevents SQLite BUSY/LOCKED conflict when stages are chained
- `startBotPolling()` is placed inside `app.listen` callback, which is already inside `if (!isVercelRuntime)` — no additional guard needed
- `TELEGRAM_BOT_TOKEN` deliberately omitted from startup env-var logging block (pitfall 5 from Phase 3 research)
- `newsRoutes` mounted adjacent to other bot-related routes (`/api/moderation`, `/api/bot`) for logical grouping

## Deviations from Plan

None - plan executed exactly as written.

## Checkpoint: Human Verify Required

This plan has a `checkpoint:human-verify` gate. The two automated tasks are complete and committed. Human verification of the live Telegram flow is required before Phase 3 can be marked complete.

**Verification steps are in the checkpoint message below.**

## Self-Check: PASSED

- `a1c7cbb` commit — FOUND
- `ceb7597` commit — FOUND
- `server/services/news-collector/index.js` contains `runTelegramDispatch` — VERIFIED
- `server/services/news-collector/index.js` contains `tgDb` — VERIFIED
- `server/routes/news.js` exists — FOUND
- `server/routes/news.js` contains `501` — VERIFIED
- `server/index.js` contains `startBotPolling` (import + call) — VERIFIED
- `server/index.js` contains `newsRoutes` (import + use) — VERIFIED
- `server/index.js` does NOT contain `TELEGRAM_BOT_TOKEN` — VERIFIED
- TDD tests (`tg-handlers.test.mjs`): 3/3 PASS — VERIFIED

---
*Phase: 03-telegram-bot*
*Completed: 2026-03-18*
