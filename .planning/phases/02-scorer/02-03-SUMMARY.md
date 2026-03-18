---
phase: 02-scorer
plan: 03
subsystem: api
tags: [llm, openrouter, openai-sdk, sqlite, scorer, news-collector]

# Dependency graph
requires:
  - phase: 02-scorer/02-01
    provides: seen_urls schema with score/item_type/threshold_pass/scored_at columns + config.json scoring block
  - phase: 02-scorer/02-02
    provides: scorer/heuristics.js (scoreByHeuristics) and scorer/multi-source.js (applyMultiSourceBoost)
provides:
  - scorer/llm-scorer.js — scoreBatchWithLLM(items, scoringCfg) via OpenRouter + openai SDK
  - scorer/index.js — runScorer(db) full pipeline orchestrator (heuristics → LLM → multi-source boost → persist)
affects: [03-telegram, 04-publisher]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - openai SDK baseURL override for OpenRouter (no new dependency needed)
    - db.transaction() batch UPDATE for atomicity and performance
    - createRequire for JSON config import in ESM (consistent with Phase 1)
    - Graceful LLM fallback: absent key or API error → heuristic scores preserved

key-files:
  created:
    - agent-network/server/services/news-collector/scorer/llm-scorer.js
    - agent-network/server/services/news-collector/scorer/index.js
  modified: []

key-decisions:
  - "scoreBatchWithLLM returns [] (not throws) when OPENROUTER_API_KEY absent — heuristics used as-is"
  - "JSON parse errors caught per-batch via try/catch continue — partial LLM results preserved"
  - "runScorer uses db.transaction() for batch UPDATE — atomic write, no partial state"
  - "item.type (in-memory) maps to item_type (DB column) — field naming clarified in code comment"
  - "LLM only called for ambiguous range (30-70 by default) — clear items skip LLM entirely"

patterns-established:
  - "Graceful degradation: LLM failure falls back to heuristic scores, not crash"
  - "Pipeline stages: query → heuristics → LLM → multi-source boost → db.transaction persist"
  - "Score clamping: Math.max(0, Math.min(100, score)) in LLM scorer for out-of-range values"

requirements-completed: [SCOR-01, SCOR-02, SCOR-03, SCOR-04, SCOR-05]

# Metrics
duration: 2min
completed: 2026-03-18
---

# Phase 2 Plan 03: Scorer Summary

**runScorer() pipeline orchestrating heuristics + OpenRouter LLM batch scoring + multi-source boost, with graceful fallback when API key absent**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-18T11:18:29Z
- **Completed:** 2026-03-18T11:20:28Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- scorer/llm-scorer.js: batch LLM scoring via OpenRouter (openai SDK baseURL override), processes in configurable batch sizes, returns [] gracefully when key absent or API fails
- scorer/index.js: runScorer(db) full pipeline — queries WHERE score IS NULL, heuristics on all, LLM for ambiguous range, multi-source boost, db.transaction() batch persist
- All SCOR requirements satisfied: SCOR-01+02 (score/type), SCOR-03 (GPT-5 >= 70), SCOR-04 (noted as integration, Wave 3), SCOR-05 (threshold config)

## Task Commits

Each task was committed atomically:

1. **Task 1: scorer/llm-scorer.js — OpenRouter batch scoring with graceful fallback** - `4a35a35` (feat)
2. **Task 2: scorer/index.js — runScorer() pipeline orchestrator** - `7170bca` (feat)

**Plan metadata:** (docs commit below)

## Files Created/Modified

- `agent-network/server/services/news-collector/scorer/llm-scorer.js` — scoreBatchWithLLM() calling OpenRouter via openai SDK, per-batch JSON parse error handling, type normalization
- `agent-network/server/services/news-collector/scorer/index.js` — runScorer(db) orchestrating all scoring stages with db.transaction() persist

## Decisions Made

- Used openai SDK baseURL override for OpenRouter — no new dependency, consistent with existing openai install
- LLM only invoked for ambiguous range (30-70) — clear items (high or low) skip LLM entirely, saving API calls
- db.transaction() wraps all UPDATE statements — one atomic write, faster and no partial state on crash
- In-memory field name `type` maps to DB column `item_type` — comment clarifies this in index.js
- scoreBatchWithLLM returns [] on any failure — upstream runScorer treats empty array as "no overrides", heuristics remain

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None — scoring pipeline works in heuristics-only mode when OPENROUTER_API_KEY is absent.

## Next Phase Readiness

- All 5 SCOR requirements pass in test-scorer.js
- runScorer(db) is the entry point for Phase 3 (Telegram bot) to trigger after each collector run
- Phase 3 requires TG bot token (noted blocker in STATE.md)

---
*Phase: 02-scorer*
*Completed: 2026-03-18*
