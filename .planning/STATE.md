---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: completed
stopped_at: Completed 02-03-PLAN.md — Phase 2 Plan 3 complete
last_updated: "2026-03-18T11:21:40.461Z"
last_activity: 2026-03-18 — Plan 02-01 complete — scorer schema + config + test scaffold ready
progress:
  total_phases: 4
  completed_phases: 1
  total_plans: 9
  completed_plans: 8
  percent: 25
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-18)

**Core value:** Adminas gauna svarbias AI/tech naujienas į Telegram ir vienu mygtuko paspaudimu patvirtina jų publikavimą kaip pilnus blog post'us.
**Current focus:** Phase 1 — Collector (ready to plan)

## Current Position

Phase: 2 of 4 (Scorer) — IN PROGRESS
Plan: 1 of N in Phase 2 — 1 complete
Status: Phase 2 started, Plan 02-01 complete (schema + config + test scaffold)
Last activity: 2026-03-18 — Plan 02-01 complete — scorer schema + config + test scaffold ready

Progress: [██████░░░░] 25% (Phase 2 Plan 1/N complete)

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
| Phase 02-scorer P02 | 5 | 2 tasks | 2 files |
| Phase 02-scorer P03 | 2 | 2 tasks | 2 files |

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

### Pending Todos

None yet.

### Blockers/Concerns

- TG bot token needed before Phase 3 can execute (bot shell already created)
- OpenRouter credit ~6€ as of 2026-03-10 — monitor during Phase 4 testing
- GitHub API + HuggingFace API rate limits require rate limiting implementation in Phase 1

## Session Continuity

Last session: 2026-03-18T11:21:40.456Z
Stopped at: Completed 02-03-PLAN.md — Phase 2 Plan 3 complete
Resume file: None
