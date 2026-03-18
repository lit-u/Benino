---
phase: 03-telegram-bot
plan: "02"
subsystem: news-collector
tags: [telegraf, telegram, sqlite, markdownv2, dispatcher, tdd, bot]
dependency_graph:
  requires:
    - phase: "03-01"
      provides: tg_status-column, tg_message_id-column, telegram-config, tg-test-scaffold
  provides:
    - telegraf bot instance with graceful no-token fallback (bot.js)
    - MarkdownV2 card formatter with escapeMarkdownV2 (card.js)
    - registerHandlers + handleReject/handleAccept testable exports (handlers.js)
    - runTelegramDispatch(db) with 24h cutoff filter (dispatcher.js)
  affects: [phase-04-writer, news-collector-index]
tech_stack:
  added: [telegraf@4.16.3]
  patterns: [injectable-fetch-for-testing, graceful-no-token-fallback, tg_status-state-machine, tdd-red-green]
key_files:
  created:
    - agent-network/server/services/news-collector/telegram/bot.js
    - agent-network/server/services/news-collector/telegram/card.js
    - agent-network/server/services/news-collector/telegram/handlers.js
    - agent-network/server/services/news-collector/telegram/dispatcher.js
  modified:
    - agent-network/tests/news-collector/tg-handlers.test.mjs
    - agent-network/package.json
key_decisions:
  - "handleReject and handleAccept exported as pure functions (separate from bot.action wiring) — makes unit testing possible without a real Telegraf instance"
  - "handleAccept uses injectable fetchFn parameter (default: global fetch) — allows mock fetch in tests while keeping real fetch in production"
  - "dispatcher sets tg_status='pending' (not 'sent') after send — represents 'in Telegram, awaiting admin decision' state, distinct from accepted/rejected"
  - "dispatchCutoffMs filter (24h) prevents flooding admin with 942-item backlog on first run"
  - "telegraf@4.16.3 pinned — stable release matching plan specification"
requirements-completed: [TG-01, TG-02, TG-03, TG-04]
duration: 8min
completed: "2026-03-18"
---

# Phase 3 Plan 02: Telegram Bot Core Logic

**Telegraf bot with MarkdownV2 card formatter, accept/reject DB handlers, and 24h-filtered dispatch loop — all 4 Telegram module files implemented with 3 passing TDD unit tests.**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-18T12:05:00Z
- **Completed:** 2026-03-18T12:13:00Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments

- Four Telegram module files created covering the full bot lifecycle
- TDD tests pass for TG-03 (reject) and TG-04 (accept + stub + error resilience)
- All modules gracefully handle missing TELEGRAM_BOT_TOKEN — no crash on import
- dispatcher.js correctly filters by `tg_status IS NULL AND scored_at > cutoff` to avoid stale-item flood

## Task Commits

Each task was committed atomically:

1. **Task 1: Create bot.js, card.js, handlers.js — core Telegram logic** - `3d4e441` (feat)
2. **Task 2: Create dispatcher.js — query pending items and send cards** - `303c7d6` (feat)

## Files Created/Modified

- `server/services/news-collector/telegram/bot.js` - Telegraf instance + startBotPolling(), null when no token
- `server/services/news-collector/telegram/card.js` - buildCard() with MarkdownV2 escaping + inline keyboard
- `server/services/news-collector/telegram/handlers.js` - registerHandlers() + exported handleReject/handleAccept for tests
- `server/services/news-collector/telegram/dispatcher.js` - runTelegramDispatch(db) with 24h cutoff, rate limiting, tg_status='pending'
- `tests/news-collector/tg-handlers.test.mjs` - 3 passing tests (TG-03 reject, TG-04 accept, TG-04 fetch-error survival)
- `package.json` / `package-lock.json` - telegraf@4.16.3 added

## Decisions Made

- `handleReject` and `handleAccept` exported as pure DB functions separate from `registerHandlers()` — testable without a real Telegraf context object
- `fetchFn` injectable parameter on `handleAccept` — allows `mockFetch` in tests, global `fetch` in production
- Dispatcher sets `tg_status='pending'` after send (not null, not accepted/rejected) — represents "card is live in Telegram, awaiting admin click"
- `dispatchCutoffMs=86400000` (24h) already established in Plan 01 config — dispatcher respects it to prevent flooding

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - telegraf installed cleanly, all imports worked, TDD cycle passed first time.

## User Setup Required

None for code — but Phase 3 execution requires:
- `TELEGRAM_BOT_TOKEN` env var (bot shell created via @BotFather)
- `TELEGRAM_ADMIN_CHAT_ID` env var (your Telegram chat ID)

Without these, the bot gracefully skips with warning messages (no crash).

## Next Phase Readiness

- All 4 Telegram modules complete and tested
- dispatcher.js ready to be called from news-collector index.js (Phase 3 Plan 03)
- handlers.js ready to be registered on bot startup (Phase 3 Plan 03)
- Phase 4 stub trigger in place at `POST /api/news/accept/:hash` — Phase 4 Writer can implement this endpoint

---
*Phase: 03-telegram-bot*
*Completed: 2026-03-18*
