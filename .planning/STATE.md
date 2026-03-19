---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: verifying
stopped_at: Completed 05-02-PLAN.md
last_updated: "2026-03-19T14:56:38.537Z"
last_activity: 2026-03-18 — Plan 02-04 complete — runScorer() wired into runCollector(), E2E verified
progress:
  total_phases: 5
  completed_phases: 3
  total_plans: 19
  completed_plans: 17
  percent: 50
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-18)

**Core value:** Adminas gauna svarbias AI/tech naujienas į Telegram ir vienu mygtuko paspaudimu patvirtina jų publikavimą kaip pilnus blog post'us.
**Current focus:** Phase 1 — Collector (ready to plan)

## Current Position

Phase: 2 of 4 (Scorer) — COMPLETE
Plan: 4 of 4 in Phase 2 — all complete
Status: Phase 2 fully complete. All 5 SCOR requirements verified with 1001/1001 items scored in live DB.
Last activity: 2026-03-18 — Plan 02-04 complete — runScorer() wired into runCollector(), E2E verified

Progress: [████████░░] 50% (Phase 2 complete — 2/4 phases done)

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

### Roadmap Evolution

- Phase 5 added: Hotel Mini-Website — Pajūrio Namelis tipo mini svetainė mažiems apgyvendinimo objektams

### Pending Todos

None yet.

### Blockers/Concerns

- TG bot token needed before Phase 3 can execute (bot shell already created)
- OpenRouter credit ~6€ as of 2026-03-10 — monitor during Phase 4 testing
- GitHub API + HuggingFace API rate limits require rate limiting implementation in Phase 1

## Session Continuity

Last session: 2026-03-19T14:56:38.532Z
Stopped at: Completed 05-02-PLAN.md
Resume file: None
