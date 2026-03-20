---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: verifying
stopped_at: Completed 07-00-PLAN.md
last_updated: "2026-03-20T11:15:49.482Z"
last_activity: 2026-03-19 — Plan 05-03 complete — hotel admin panel (room CRUD, drag-drop photos, QR) built and verified
progress:
  total_phases: 7
  completed_phases: 6
  total_plans: 27
  completed_plans: 25
  percent: 100
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-18)

**Core value:** Adminas gauna svarbias AI/tech naujienas į Telegram ir vienu mygtuko paspaudimu patvirtina jų publikavimą kaip pilnus blog post'us.
**Current focus:** Phase 1 — Collector (ready to plan)

## Current Position

Phase: 5 of 5 (Hotel Mini-Website) — COMPLETE
Plan: 4 of 4 in Phase 5 — all complete
Status: All 5 phases complete. Phase 5 hotel mini-website verified end-to-end by human — SSR, JSON-LD, admin auth gate, QR generation all confirmed working.
Last activity: 2026-03-19 — Plan 05-03 complete — hotel admin panel (room CRUD, drag-drop photos, QR) built and verified

Progress: [██████████] 100% (All 5 phases complete)

## Performance Metrics

**Velocity:**
- Total plans completed: 4
- Average duration: 12min
- Total execution time: 46min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-collector | 4 | 46min | 12min |
| 02-scorer | 1 | 8min | 8min |

**Recent Trend:**
- Last 5 plans: 01-01 (15min), 01-02 (20min), 01-03 (3min), 01-04 (8min), 02-01 (8min)
- Trend: stable

*Updated after each plan completion*
| Phase 02-scorer P02 | 5 | 2 tasks | 2 files |
| Phase 02-scorer P03 | 2 | 2 tasks | 2 files |
| Phase 02-scorer P04 | 15 | 2 tasks | 1 file |
| Phase 03-telegram-bot P01 | 4 | 2 tasks | 3 files |
| Phase 03-telegram-bot P02 | 8 | 2 tasks | 6 files |
| Phase 03-telegram-bot P03 | 7 | 2 tasks | 3 files |
| Phase 04-writer-publisher P01 | 28 | 3 tasks | 3 files |
| Phase 04-writer-publisher P02 | 3 | 2 tasks | 3 files |
| Phase 05-hotel-mini-website P00 | 3 | 1 tasks | 1 files |
| Phase 05-hotel-mini-website P01 | 68 | 3 tasks | 5 files |
| Phase 05-hotel-mini-website P02 | 11 | 2 tasks | 3 files |
| Phase 05-hotel-mini-website P03 | 15 | 1 task (+ checkpoint) | 2 files |
| Phase 04-writer-publisher P04 | 3 | 2 tasks | 2 files |
| Phase 06-rezervacij-sistema P00 | 4 | 1 tasks | 1 files |
| Phase 06-rezervacij-sistema P01 | 7 | 2 tasks | 2 files |
| Phase 06-rezervacij-sistema P02 | 2 | 1 tasks | 1 files |
| Phase 06-rezervacij-sistema P03 | 30 | 2 tasks | 3 files |
| Phase 07-multi-hotel P00 | 1 | 1 tasks | 1 files |

## Accumulated Context

### Decisions

- Node.js (not Python) — direct integration with agent-network blog API
- OpenRouter LLM — easy model switching, billing control (default: google/gemini-2.0-flash-001)
- 6h cron interval — balance between freshness and API load
- Publish via agent-network blog API — not direct Supabase writes
- TAAFT source uses taaft-scrape type (RSS URL broken per research)
- HuggingFace Papers uses hf-papers-api type (official API more reliable than blog RSS)
- URL hash is SHA-256 first 32 chars — sufficient collision resistance for news dedup
- rss-fetcher reuses DEFAULT_PARSER; creates new Parser instance only when source.headers is set
- GitHub Trending uses article.Box-row + h2.h3.lh-condensed a selectors (confirmed 2026-03-18)
- HN fetcher uses search_by_date endpoint (not search) for recency-sorted 6h window
- TAAFT selector: li.li (page is static HTML, 14 tools, no puppeteer needed)
- HuggingFace Models: sort=createdAt (camelCase) — created_at causes HTTP 400
- [Phase 01-collector]: createRequire used for JSON config import (reliable across all Node.js ESM versions)
- [Phase 01-collector]: db.close() called at end of each runCollector() to avoid SQLite connection leaks
- [Phase 01-collector]: registerNewsCollector() placed inside app.listen callback — server must be up before cron starts; Vercel guard inherited from enclosing if(!isVercelRuntime) block
- [Phase 02-scorer]: addIfMissing() uses try/catch on ALTER TABLE — SQLite has no IF NOT EXISTS for column additions
- [Phase 02-scorer]: scorer/test-scorer.js import paths use relative-to-file paths (../config.json, ./heuristics.js) not root-relative
- [Phase 02-scorer]: scoreByHeuristics: all KEYWORD_RULES boosts additive, highest-magnitude rule wins type — avoids confusion on multi-signal titles
- [Phase 02-scorer]: applyMultiSourceBoost uses greedy O(n^2) Jaccard grouping (not transitive closure) — simpler, correct for batch sizes <= 50
- [Phase 02-scorer]: SOURCE_BASELINES base scores higher than research doc (openai: 60 not 55) — ensures top-tier sources clear threshold without keyword match
- [Phase 02-scorer]: scoreByHeuristics: all KEYWORD_RULES boosts additive, highest-magnitude rule wins type — avoids confusion on multi-signal titles
- [Phase 02-scorer]: applyMultiSourceBoost uses greedy O(n^2) Jaccard grouping (not transitive closure) — simpler, correct for batch sizes <= 50
- [Phase 02-scorer]: scoreBatchWithLLM returns [] when OPENROUTER_API_KEY absent — heuristics used as-is (graceful fallback)
- [Phase 02-scorer]: runScorer uses db.transaction() for batch UPDATE — atomic write, no partial state on crash
- [Phase 02-scorer]: LLM only called for ambiguous range (30-70) — clear items skip LLM entirely, saving API calls
- [Phase 02-scorer P04]: runScorer gets fresh db2 connection after runCollector closes db — prevents SQLite busy/locked conflict
- [Phase 02-scorer P04]: try/finally wraps scorerDb.close() — guaranteed cleanup even if runScorer() throws
- [Phase 03-telegram-bot]: WAL pragma added immediately after Database() constructor to prevent SQLITE_BUSY when bot and collector share DB file
- [Phase 03-telegram-bot]: telegram.batchDelayMs=1000ms for safe Telegram rate limiting; dispatchCutoffMs=86400000 prevents sending stale items on first run
- [Phase 03-telegram-bot]: handleReject and handleAccept exported as pure functions — testable without real Telegraf instance
- [Phase 03-telegram-bot]: handleAccept uses injectable fetchFn parameter — mock in tests, global fetch in production
- [Phase 03-telegram-bot]: dispatcher sets tg_status='pending' after send — distinct from accepted/rejected, means card is live in Telegram
- [Phase 03-telegram-bot]: runTelegramDispatch(tgDb) uses fresh db3 connection — same fresh-connection pattern as scorer, prevents SQLite busy conflict
- [Phase 03-telegram-bot]: startBotPolling() inside app.listen (Vercel-guarded by parent block); TELEGRAM_BOT_TOKEN never logged
- [Phase 04-writer-publisher]: OPENROUTER_API_KEY absent throws immediately in writer — no silent fallback unlike scorer
- [Phase 04-writer-publisher]: Three LLM calls (mokslius, oldboy, tags) run in parallel via Promise.all — minimizes latency
- [Phase 04-writer-publisher]: item_type override (breakthrough→AI Valdymas, research→Mokslas) takes precedence over source_id in detectCategory
- [Phase 04-writer-publisher]: USER OVERRIDE: Draft-to-disk instead of Supabase publish — user reviews drafts/<hash>.json manually before publishing
- [Phase 04-writer-publisher]: writer_status='draft' (not 'published') — clean semantic distinction between written and live
- [Phase 04-writer-publisher]: drafts/ dir gitignored — generated content should not be committed
- [Phase 05-hotel-mini-website]: Wave-0 pattern: test.skip() stubs created before backend, so spec compiles without server dependency
- [Phase 05-hotel-mini-website]: owner_id is TEXT (not UUID FK) in hotels table — avoids FK constraint failures during dual-auth system transition
- [Phase 05-hotel-mini-website]: HotelImageService extends ImageUploadService — thin subclass overrides bucketName and watermarkPath, reuses all compression logic
- [Phase 05-hotel-mini-website]: injectMeta extended with optional ogImage parameter (backward-compatible — existing callers unaffected)
- [Phase 05-hotel-mini-website]: hotel.phone used as mailto recipient — no separate email column in hotels table
- [Phase 05-hotel-mini-website]: requireUser imported at module top-level — ES module import must be static, not inline
- [Phase 05-hotel-mini-website P03]: Window-view type toggle tries /type endpoint first, falls back to sort-order reorder (sort_order=0 = window_view)
- [Phase 05-hotel-mini-website P03]: Session key is agent_session_id (not sessionId) — matches soc-module.js pattern
- [Phase 04-writer-publisher]: cfg loaded via createRequire in news.js — synchronous, consistent with existing require declaration
- [Phase 04-writer-publisher]: handleAccept returns { ok, data } instead of void — unit tests can assert pipeline outcome
- [Phase 06-rezervacij-sistema]: Wave-0 pattern reused from Phase 05 — test.skip() stubs compile without server dependency, serving as executable spec
- [Phase 06-rezervacij-sistema]: Non-throwing email method: sendReservationNotification() returns { success: false } on error — fire-and-forget, consistent with sendWelcomeEmail pattern
- [Phase 06-rezervacij-sistema]: Public POST reservation route: no requireUser — anonymous guests submit without session, service role key bypasses RLS
- [Phase 06-rezervacij-sistema]: Inline style block inside formEl.innerHTML for component-scoped CSS without external stylesheet changes
- [Phase 06-rezervacij-sistema]: Replace formEl.innerHTML on success — prevents re-submit and cleanly removes all form DOM
- [Phase 06-rezervacij-sistema]: loadReservations() independent from refreshHotel() — separate data lifecycle, room saves do not re-fetch reservations
- [Phase 06-rezervacij-sistema]: owner-email save handler uses _wired flag to prevent duplicate listeners on re-render
- [Phase 06-rezervacij-sistema]: loadReservations() independent from refreshHotel() — separate data lifecycle, room saves do not re-fetch reservations
- [Phase 06-rezervacij-sistema]: owner-email save handler uses _wired flag to prevent duplicate listeners on re-render
- [Phase 07-multi-hotel]: Wave-0 test.skip stubs for MH-01 through MH-06 created before implementation — API stubs (07-01), page stubs (07-02)

### Roadmap Evolution

- Phase 5 added: Hotel Mini-Website — Pajūrio Namelis tipo mini svetainė mažiems apgyvendinimo objektams
- Phase 6 added: Rezervacijų Sistema — tikros rezervacijos į DB, savininkas gauna el. laišką ir WhatsApp pranešimą apie kiekvieną rezervaciją
- Phase 7 added: Multi-Hotel — L2 vartotojai gali kurti savo viešbučius per savitarnos panelę

### Pending Todos

None yet.

### Blockers/Concerns

- TG bot token needed before Phase 3 can execute (bot shell already created)
- OpenRouter credit ~6€ as of 2026-03-10 — monitor during Phase 4 testing
- GitHub API + HuggingFace API rate limits require rate limiting implementation in Phase 1

## Session Continuity

Last session: 2026-03-20T11:15:49.475Z
Stopped at: Completed 07-00-PLAN.md
Resume file: None
