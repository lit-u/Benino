---
phase: 04-writer-publisher
plan: "01"
subsystem: api
tags: [openrouter, openai-sdk, cheerio, sqlite, news-writer, llm, blog-generation]

# Dependency graph
requires:
  - phase: 03-telegram-bot
    provides: seen_urls table with tg_status/tg_message_id, addIfMissing migration pattern

provides:
  - generateNewsPost(item, cfg) in news-writer.js returning dual-style blog post
  - writer_status column in seen_urls for writer lifecycle tracking
  - setWriterStatus(db, urlHash, status) helper for state transitions
  - config.json writer block with model and token settings
  - detectCategory(sourceId, itemType) exported for reuse in publisher

affects:
  - 04-02 (publisher will import generateNewsPost and setWriterStatus to wire into accept flow)

# Tech tracking
tech-stack:
  added: []  # openai SDK and cheerio already in package.json
  patterns:
    - "Parallel LLM calls via Promise.all (3 concurrent: mokslius + oldboy + tags)"
    - "item_type override takes precedence over source_id in category detection"
    - "Adaptive token budget: wordCount < threshold → shortMaxTokens, else fullMaxTokens"
    - "Cheerio p-tag scraping with 8s AbortSignal.timeout + fallback to item.description"

key-files:
  created:
    - agent-network/server/services/news-collector/writer/news-writer.js
  modified:
    - agent-network/server/services/news-collector/storage/db.js
    - agent-network/server/services/news-collector/config.json

key-decisions:
  - "OPENROUTER_API_KEY absent throws immediately — writer cannot produce post without LLM (no silent fallback)"
  - "Three LLM calls (mokslius, oldboy, tags) run in parallel via Promise.all to minimize latency"
  - "item_type override checked before source_id lookup — breakthrough/research override any source"
  - "detectCategory exported as named export — publisher can call directly without reimplementing"
  - "Adaptive token budget based on source content word count, not character count"

patterns-established:
  - "Pattern: writer state machine — null / writing / published / failed tracked per url_hash"
  - "Pattern: LLM content generation follows scorer's OpenAI-SDK-over-OpenRouter pattern"

requirements-completed: [WRIT-01, WRIT-02, WRIT-03, WRIT-04, WRIT-05]

# Metrics
duration: 28min
completed: 2026-03-18
---

# Phase 4 Plan 01: Writer Module Summary

**LLM writer module using OpenRouter (gemini-2.0-flash) that fetches source articles via cheerio, generates dual Mokslius+OldBoy Lithuanian blog posts in parallel, auto-tags with 3-5 keywords, and maps source_id/item_type to category**

## Performance

- **Duration:** 28 min
- **Started:** 2026-03-18T16:53:17Z
- **Completed:** 2026-03-18T17:21:00Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments
- `writer_status` column added to `seen_urls` via safe addIfMissing migration — null / writing / published / failed lifecycle
- `config.json` extended with writer block (model, token budgets, threshold) — model changeable without code edits
- `news-writer.js` created with `generateNewsPost()` running 3 concurrent LLM calls for Mokslius (technical) + OldBoy (narrative) bodies + auto-tags
- `detectCategory()` exported separately for reuse; item_type override (breakthrough/research) takes precedence over source_id lookup
- Cheerio scraper with 8s timeout + fallback to item.description; adaptive token budget based on content word count

## Task Commits

Each task was committed atomically:

1. **Task 1: DB migration — writer_status column + setWriterStatus() helper** - `6384509` (feat)
2. **Task 2: config.json — add writer block** - `e6cae3c` (feat)
3. **Task 3: news-writer.js — content fetch + dual LLM generation** - `c9f11c9` (feat)

## Files Created/Modified
- `server/services/news-collector/writer/news-writer.js` - Main writer module; exports generateNewsPost() and detectCategory()
- `server/services/news-collector/storage/db.js` - Added writer_status addIfMissing + setWriterStatus() export
- `server/services/news-collector/config.json` - Added writer block between telegram and sources

## Decisions Made
- OPENROUTER_API_KEY absent throws immediately — writer cannot produce post without LLM (no silent fallback, unlike scorer's graceful degradation)
- Three LLM calls run via Promise.all to minimize wall-clock latency (~3x speedup over sequential)
- item_type override checked before source_id lookup — breakthrough/research classify correctly regardless of source
- detectCategory exported as named export so publisher can reuse without re-implementing the map
- Token budget uses word count (not character count) for word-aligned content length decisions

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Shell `!` character caused syntax error in inline `node -e` verification command. Fixed by using temporary `.mjs` script files for verification (cleaner pattern anyway).

## User Setup Required
None - no external service configuration required. OPENROUTER_API_KEY must already be set in environment (documented in MEMORY.md).

## Next Phase Readiness
- `generateNewsPost(item, cfg)` is ready for the publisher (04-02) to import
- `setWriterStatus(db, urlHash, status)` ready for publisher to call at writing/published/failed transitions
- `detectCategory` available for publisher if needed separately
- Phase 04-02 can wire generateNewsPost into the Telegram accept flow immediately

## Self-Check: PASSED

- FOUND: server/services/news-collector/writer/news-writer.js
- FOUND: server/services/news-collector/storage/db.js (writer_status column)
- FOUND: server/services/news-collector/config.json (writer block)
- FOUND: .planning/phases/04-writer-publisher/04-01-SUMMARY.md
- COMMIT 6384509: feat(04-01): DB migration — writer_status column + setWriterStatus() helper
- COMMIT e6cae3c: feat(04-01): config.json — add writer block with model and token settings
- COMMIT c9f11c9: feat(04-01): news-writer.js — content fetch + dual LLM generation

---
*Phase: 04-writer-publisher*
*Completed: 2026-03-18*
