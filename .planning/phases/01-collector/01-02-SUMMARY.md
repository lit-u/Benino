---
phase: 01-collector
plan: 02
subsystem: api
tags: [rss-parser, node-fetch, cheerio, news-collector, rss, hackernews, github-trending]

# Dependency graph
requires:
  - phase: 01-collector plan 01
    provides: "news-collector directory, config.json, storage/db.js, deps installed (rss-parser, node-fetch, cheerio)"
provides:
  - "rss-fetcher.js: generic RSS/Atom parser for anthropic, openai, google-ai, github-changelog sources"
  - "hn-fetcher.js: HackerNews Algolia API fetcher with null-URL fallback"
  - "github-trending-fetcher.js: GitHub Trending HTML scraper via cheerio"
affects: [01-03, 01-04, sources/index.js]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "All fetchers export a single named async function: export async function fetchX(source)"
    - "All fetchers return NewsItem[] with shape: url, title, publishedAt, source, summary, raw"
    - "URL filter: .filter(i => i.url) applied after map to drop items with no canonical link"
    - "summary capped at 500 chars via .substring(0, 500)"
    - "Per-source headers support in rss-fetcher via source.headers config field"

key-files:
  created:
    - agent-network/server/services/news-collector/sources/rss-fetcher.js
    - agent-network/server/services/news-collector/sources/hn-fetcher.js
    - agent-network/server/services/news-collector/sources/github-trending-fetcher.js
  modified: []

key-decisions:
  - "rss-fetcher creates new Parser instance per-source only when source.headers is set, reusing DEFAULT_PARSER otherwise (avoids object churn)"
  - "HN fetcher uses search_by_date endpoint (not search) for recency-sorted results matching 6h lookback window"
  - "GitHub Trending article.Box-row + h2.h3.lh-condensed a selectors confirmed working as of 2026-03-18"

patterns-established:
  - "Fetcher pattern: single named export, takes source config object, returns NewsItem[]"
  - "Error isolation: each fetcher throws on fatal errors; caller (index.js) wraps in try/catch per source"
  - "Sponsor filter: check href.includes('/sponsors/') before processing GitHub Trending rows"

requirements-completed: [COLL-01, COLL-05]

# Metrics
duration: 20min
completed: 2026-03-18
---

# Phase 1 Plan 02: Source Fetchers (RSS, HackerNews, GitHub Trending) Summary

**Three source fetchers implementing NewsItem[] contracts: rss-parser-based RSS/Atom for 4 sources, HN Algolia search_by_date with null-URL fallback, and cheerio-based GitHub Trending scraper with sponsor filtering**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-03-18T10:22:52Z
- **Completed:** 2026-03-18T10:42:00Z
- **Tasks:** 3
- **Files modified:** 3 created

## Accomplishments
- RSS fetcher handles 4 configured sources (anthropic, openai, google-ai, github-changelog) with per-source header override support
- HN Algolia fetcher uses correct search_by_date endpoint with 6-hour lookback; Ask/Show HN null-URL posts get HN item URL as fallback
- GitHub Trending scraper parses article.Box-row elements, filters /sponsors/ entries, returns owner/repo-formatted titles

## Task Commits

Each task was committed atomically:

1. **Task 1: RSS fetcher for 4 RSS-type sources** - `1e81f2d` (feat)
2. **Task 2: HackerNews Algolia API fetcher** - `a684e35` (feat)
3. **Task 3: GitHub Trending HTML scraper** - `7eb623a` (feat)

**Plan metadata:** (docs commit — see final commit)

## Files Created/Modified
- `agent-network/server/services/news-collector/sources/rss-fetcher.js` - Generic RSS/Atom fetcher using rss-parser; custom headers per source; URL filter; 500-char summary cap
- `agent-network/server/services/news-collector/sources/hn-fetcher.js` - HN Algolia search_by_date; 6h window; null URL fallback to HN item URL
- `agent-network/server/services/news-collector/sources/github-trending-fetcher.js` - cheerio HTML scraper; article.Box-row selector; sponsor filter; github.com URL construction

## Decisions Made
- Reuse `DEFAULT_PARSER` for sources without custom headers; create new Parser instance only when `source.headers` is defined
- GitHub Trending returns 6 items today (page has fewer repos listed than usual) — selectors confirmed working; count will vary daily

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None. All three live smoke tests passed on first run. GitHub Trending returned 6 items (selector `article.Box-row` working correctly as of 2026-03-18).

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All three fetchers ready for integration into sources/index.js (Plan 04)
- github-search-fetcher.js and huggingface-fetcher.js already present from Plan 01 (created earlier)
- sources/ directory now contains all 5 planned fetcher files
- Blocker: none for Plans 03-04

---
*Phase: 01-collector*
*Completed: 2026-03-18*
