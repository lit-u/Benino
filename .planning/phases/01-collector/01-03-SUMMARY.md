---
phase: 01-collector
plan: 03
subsystem: api
tags: [node-fetch, cheerio, github-api, huggingface-api, web-scraping, news-collector]

# Dependency graph
requires:
  - phase: 01-01
    provides: news-collector directory structure, config.json with all 10 source definitions, storage/db.js

provides:
  - github-search-fetcher.js: GitHub Search REST API with optional PAT, rate limit guard
  - huggingface-fetcher.js: HuggingFace Papers API + Models API (two exports)
  - taaft-fetcher.js: TAAFT recently-added page scraper via cheerio (li.li selector)

affects:
  - 01-04 (sources/index.js must import these three fetchers)
  - 01-05 (collector orchestrator consumes all sources)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "TAAFT scraping: li.li selector with data-name attribute for tool name, .ai_link anchor for URL"
    - "HuggingFace: sort=createdAt (camelCase) is required — created_at returns HTTP 400"
    - "GitHub Search: replace DATE placeholder with yesterday ISO date; rate limit guard via X-RateLimit-Remaining header"

key-files:
  created:
    - agent-network/server/services/news-collector/sources/github-search-fetcher.js
    - agent-network/server/services/news-collector/sources/huggingface-fetcher.js
    - agent-network/server/services/news-collector/sources/taaft-fetcher.js
  modified: []

key-decisions:
  - "TAAFT selector: li.li (not .ai-tool-card or article) — each li has data-name and .ai_link anchor pointing to /ai/<slug>/"
  - "TAAFT returns 14 items from static HTML — no puppeteer needed (page is server-rendered)"
  - "HF Models: URLSearchParams used to construct query string ensuring correct camelCase sort param"

patterns-established:
  - "All fetchers return NewsItem[] with {url, title, publishedAt, source, summary, raw}"
  - "Fetchers never throw on empty results — only throw on HTTP errors (non-2xx)"
  - "TAAFT deduplicates by URL within batch using Set"

requirements-completed: [COLL-01, COLL-05]

# Metrics
duration: 3min
completed: 2026-03-18
---

# Phase 1 Plan 03: Source Fetchers (GitHub Search, HuggingFace, TAAFT) Summary

**Three complex API/scrape fetchers: GitHub Search with optional PAT + rate guard, HuggingFace Papers+Models with camelCase sort param, TAAFT cheerio scraper using li.li selector returning 14 live tools**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-03-18T07:02:50Z
- **Completed:** 2026-03-18T07:05:21Z
- **Tasks:** 3
- **Files modified:** 3 created

## Accomplishments
- GitHub Search fetcher with optional GITHUB_TOKEN auth, rate limit logging, and descriptive 403/429 errors
- HuggingFace fetcher with two exports: Papers API (daily_papers endpoint) and Models API (sort=createdAt camelCase)
- TAAFT scraper using li.li selector discovered via Step 1 HTML inspection — returns 14 real tool entries from static HTML

## Task Commits

Each task was committed atomically:

1. **Task 1: GitHub Search API fetcher** - `9585443` (feat)
2. **Task 2: HuggingFace Papers and Models API fetchers** - `db369e5` (feat)
3. **Task 3: TAAFT recently-added scraper** - `d551d51` (feat)

## Files Created/Modified
- `agent-network/server/services/news-collector/sources/github-search-fetcher.js` - GitHub Search REST API fetcher with optional PAT, rate limit guard, safe items fallback
- `agent-network/server/services/news-collector/sources/huggingface-fetcher.js` - HuggingFace Papers and Models API fetchers; sort=createdAt (camelCase)
- `agent-network/server/services/news-collector/sources/taaft-fetcher.js` - TAAFT scraper using li.li selector, returns 14 items from static HTML

## Decisions Made
- TAAFT selector `li.li` discovered via live HTML inspection — page is server-rendered (not SPA), so cheerio suffices
- TAAFT `data-name` attribute used for tool title (cleaner than parsing inner text)
- HuggingFace Models uses `URLSearchParams` to ensure the `sort` key is always sent as `createdAt` (string key, never mangled)
- GitHub: `data.items || []` safe fallback ensures no crash if GitHub returns unexpected shape during rate limit partial response

## Deviations from Plan

None - plan executed exactly as written. TAAFT selector discovery (Step 1) worked as planned and confirmed the page is static HTML.

## Issues Encountered
None — all three smoke tests passed on first run:
- GitHub Search: 3 items returned (no GITHUB_TOKEN, unauthenticated tier)
- HuggingFace Papers: 3 items, HuggingFace Models: 3 items
- TAAFT: 14 items, all with non-empty url and title

## User Setup Required
None - no external service configuration required. GITHUB_TOKEN is optional (improves rate limits from 60 to 5000 req/hour if set in .env).

## Next Phase Readiness
- All 3 complex fetchers complete; combined with plan 02 fetchers (RSS, HN, GitHub Trending), the full set of 10 source fetchers is ready
- Plan 04 (sources/index.js) can now import and re-export all fetchers
- Plan 05 (collector orchestrator) can consume sources/index.js

---
*Phase: 01-collector*
*Completed: 2026-03-18*
