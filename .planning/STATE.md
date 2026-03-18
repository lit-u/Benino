# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-18)

**Core value:** Adminas gauna svarbias AI/tech naujienas į Telegram ir vienu mygtuko paspaudimu patvirtina jų publikavimą kaip pilnus blog post'us.
**Current focus:** Phase 1 — Collector (ready to plan)

## Current Position

Phase: 1 of 4 (Collector)
Plan: 1 of 6 in current phase
Status: In progress
Last activity: 2026-03-18 — Plan 01-01 complete (Bootstrap: deps, config, storage)

Progress: [█░░░░░░░░░] 4%

## Performance Metrics

**Velocity:**
- Total plans completed: 1
- Average duration: 15min
- Total execution time: 15min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-collector | 1 | 15min | 15min |

**Recent Trend:**
- Last 5 plans: 01-01 (15min)
- Trend: —

*Updated after each plan completion*

## Accumulated Context

### Decisions

- Node.js (not Python) — direct integration with agent-network blog API
- OpenRouter LLM — easy model switching, billing control (default: google/gemini-2.0-flash-001)
- 6h cron interval — balance between freshness and API load
- Publish via agent-network blog API — not direct Supabase writes
- TAAFT source uses taaft-scrape type (RSS URL broken per research)
- HuggingFace Papers uses hf-papers-api type (official API more reliable than blog RSS)
- URL hash is SHA-256 first 32 chars — sufficient collision resistance for news dedup

### Pending Todos

None yet.

### Blockers/Concerns

- TG bot token needed before Phase 3 can execute (bot shell already created)
- OpenRouter credit ~6€ as of 2026-03-10 — monitor during Phase 4 testing
- GitHub API + HuggingFace API rate limits require rate limiting implementation in Phase 1

## Session Continuity

Last session: 2026-03-18
Stopped at: Completed 01-01-PLAN.md (Bootstrap: deps installed, config.json, storage/db.js)
Resume file: None
