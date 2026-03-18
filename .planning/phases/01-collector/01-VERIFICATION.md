---
phase: 01-collector
verified: 2026-03-18T08:00:00Z
status: passed
score: 5/5 must-haves verified
re_verification: false
---

# Phase 1: Collector Verification Report

**Phase Goal:** The system reliably fetches AI/tech news from all 10 configured sources on a schedule and stores only new items
**Verified:** 2026-03-18
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| #  | Truth                                                                                      | Status     | Evidence                                                                                         |
|----|-------------------------------------------------------------------------------------------|------------|--------------------------------------------------------------------------------------------------|
| 1  | All 10 sources are configured and fetchable                                                | VERIFIED   | config.json has exactly 10 sources; 7 fetcher files cover all 6 distinct source types; checkpoint Run 1: fetched=994, errors=0 |
| 2  | Collection runs automatically every 6 hours (cron scheduled at server startup)             | VERIFIED   | `registerCron()` exports valid cron `"0 */6 * * *"` from index.js; wired into server/index.js line 919 inside `app.listen()` callback; checkpoint confirmed log `[news-collector] Cron scheduled: 0 */6 * * *` |
| 3  | Already-seen items are skipped on subsequent runs (URL-hash deduplication)                 | VERIFIED   | storage/db.js exports `initDb`, `isSeen`, `markSeen` with SHA-256 hash + trailing-slash normalization + `INSERT OR IGNORE`; checkpoint Run 2: new=0, skipped=994 |
| 4  | Source list is config-driven (not hardcoded in fetcher logic)                              | VERIFIED   | config.json is the single source of truth; index.js reads `config.sources.filter(s => s.enabled)`; fetcher dispatch table in sources/index.js is driven by `source.type` from config |
| 5  | System works specifically with the 10 required sources                                      | VERIFIED   | All 10 source IDs present: anthropic, openai, google-ai, github-changelog, huggingface-papers, taaft, hackernews, github-trending, github-search, huggingface-models; each mapped to a real fetcher; checkpoint Run 1: 994 items fetched across all sources |

**Score:** 5/5 truths verified

### Required Artifacts

| Artifact                                                                 | Expected                                      | Status     | Details                                                                                           |
|--------------------------------------------------------------------------|-----------------------------------------------|------------|---------------------------------------------------------------------------------------------------|
| `agent-network/server/services/news-collector/config.json`               | 10 sources, cron expression, config-driven     | VERIFIED   | 10 sources with correct types (rss×4, hf-papers-api×1, taaft-scrape×1, hn-algolia×1, github-trending×1, github-search×1, hf-models-api×1); `"pollIntervalCron": "0 */6 * * *"`; `maxItemsPerSource: 30` |
| `agent-network/server/services/news-collector/storage/db.js`             | SQLite dedup layer: initDb/isSeen/markSeen     | VERIFIED   | All 3 functions exported; `INSERT OR IGNORE` for idempotency; SHA-256 32-char hash; trailing-slash normalization |
| `agent-network/server/services/news-collector/index.js`                  | Orchestrator: registerCron + runCollector      | VERIFIED   | Both functions exported; reads enabled sources from config; per-source error isolation; db open/close lifecycle correct |
| `agent-network/server/services/news-collector/sources/index.js`          | Fetcher dispatch table for all 6 source types  | VERIFIED   | Maps all 7 type keys to fetcher functions; throws on unknown type |
| `agent-network/server/services/news-collector/sources/rss-fetcher.js`   | Real RSS fetch logic                           | VERIFIED   | Uses rss-parser; maps title/url/publishedAt/summary; filters items without URL |
| `agent-network/server/services/news-collector/sources/hn-fetcher.js`    | HN Algolia API fetch                           | VERIFIED   | Real API call to hn.algolia.com; uses time window filter; maps hits to NewsItem shape |
| `agent-network/server/services/news-collector/sources/github-trending-fetcher.js` | GitHub Trending HTML scrape          | VERIFIED   | Uses cheerio; extracts `article.Box-row` elements; returns owner/repo URLs |
| `agent-network/server/services/news-collector/sources/github-search-fetcher.js`   | GitHub Search API fetch              | VERIFIED   | Uses GitHub REST API v3; DATE placeholder substituted at runtime; optional GITHUB_TOKEN header |
| `agent-network/server/services/news-collector/sources/huggingface-fetcher.js`     | HF Papers API + HF Models API        | VERIFIED   | Two distinct export functions; both make real API calls; proper response mapping |
| `agent-network/server/services/news-collector/sources/taaft-fetcher.js`           | TAAFT scrape via cheerio             | VERIFIED   | Fetches `theresanaiforthat.com/recently-added/`; cheerio-based selector; batch dedup by URL |
| `agent-network/server/index.js`                                          | Cron registered at startup                     | VERIFIED   | Import at line 95; `registerNewsCollector()` called at line 919 inside `app.listen()` callback, inside `!isVercelRuntime` block |
| `agent-network/.env.example`                                             | GITHUB_TOKEN documented                        | VERIFIED   | File exists; contains `# GITHUB_TOKEN=ghp_yourTokenHere` |
| `agent-network/.gitignore`                                               | news.db excluded from git                      | VERIFIED   | Line 71: `server/services/news-collector/news.db` |
| `agent-network/package.json`                                             | rss-parser and better-sqlite3 as dependencies  | VERIFIED   | `"better-sqlite3": "^12.8.0"` and `"rss-parser": "^3.13.0"` present |

### Key Link Verification

| From                          | To                                    | Via                                                                        | Status  | Details                                                                          |
|-------------------------------|---------------------------------------|----------------------------------------------------------------------------|---------|----------------------------------------------------------------------------------|
| `config.json`                 | `news-collector/index.js`             | `createRequire` + `require('./config.json')`                               | WIRED   | index.js line 8: `const config = require('./config.json')` via createRequire ESM shim |
| `storage/db.js`               | `news-collector/index.js`             | `import { initDb, isSeen, markSeen } from './storage/db.js'`               | WIRED   | index.js line 4: all 3 functions imported and called in `runCollector()`         |
| `sources/index.js`            | `news-collector/index.js`             | `import { fetchSource } from './sources/index.js'`                         | WIRED   | index.js line 3; `fetchSource(source)` called inside the enabled-sources loop   |
| `news-collector/index.js`     | `server/index.js`                     | `import { registerCron as registerNewsCollector } from './services/news-collector/index.js'` | WIRED   | server/index.js line 95 import; line 919 call inside `app.listen()` callback; guarded by enclosing `!isVercelRuntime` block (line 846) |

### Requirements Coverage

| Requirement | Source Plan | Description                                                                           | Status    | Evidence                                                                                    |
|-------------|-------------|--------------------------------------------------------------------------------------|-----------|---------------------------------------------------------------------------------------------|
| COLL-01     | 01-05       | System collects from 10 pre-configured sources (RSS + API)                           | SATISFIED | 10 sources in config.json; 7 fetcher files covering all required source types; checkpoint fetched=994 from all 10 |
| COLL-02     | 01-05       | Collection runs automatically every 6 hours (cron job)                               | SATISFIED | `registerCron()` schedules `"0 */6 * * *"`; wired into server startup; checkpoint log confirmed |
| COLL-03     | 01-01       | No repetition — already-seen URLs (by hash) are skipped                              | SATISFIED | `isSeen`/`markSeen` with SHA-256 hash + `INSERT OR IGNORE`; checkpoint Run 2: new=0, skipped=994 |
| COLL-04     | 01-01       | Source list configurable via config file (not hardcoded)                             | SATISFIED | config.json is the single source of truth; index.js filters `config.sources` at runtime |
| COLL-05     | 01-05       | Works with: Anthropic Blog, OpenAI Blog, Google AI Blog, GitHub Changelog, HackerNews, GitHub Trending, GitHub Search, HuggingFace Papers, HuggingFace Models, TAAFT | SATISFIED | All 10 source IDs present in config; each mapped to a real fetcher function; checkpoint confirmed all 10 produced items |

All 5 Phase 1 requirements accounted for. No orphaned requirements — SCOR/TG/WRIT/PUBL IDs are explicitly mapped to Phases 2-4 in REQUIREMENTS.md.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `sources/taaft-fetcher.js` | 4 | `// NOTE: TAAFT page may be JS-rendered; if 0 items, upgrade to puppeteer in Phase 2` | Info | Known limitation acknowledged; TAAFT returned items in checkpoint run (fetched=994 with 0 errors); no functional blocker |

No stubs, no empty implementations, no TODO/FIXME blockers found across any of the 9 source files, storage layer, orchestrator, or server wiring.

### Human Verification Required

Human checkpoint was performed during plan 01-05 execution and is documented in `01-05-SUMMARY.md`. The results are treated as verified evidence:

1. **Run 1 (COLL-01, COLL-05):** `fetched=994, new=994, errors=0` — all 10 sources operational
2. **Run 2 (COLL-03):** `fetched=994, new=0, skipped=994` — deduplication confirmed working
3. **Server startup (COLL-02):** Log line `[news-collector] Cron scheduled: 0 */6 * * *` confirmed

No further human verification is required for this phase.

### Summary

Phase 1 goal is fully achieved. The news-collector service:

- Fetches from all 10 configured AI/tech sources using dedicated fetchers for each source type (RSS, HN Algolia, GitHub Trending HTML, GitHub Search API, HuggingFace Papers API, HuggingFace Models API, TAAFT HTML scrape)
- Stores items to SQLite `seen_urls` table via SHA-256 URL hashing with trailing-slash normalization
- Skips already-seen URLs on subsequent runs using `INSERT OR IGNORE` semantics
- Is entirely config-driven: enabling/disabling sources requires only a config.json change
- Registers a 6-hour cron on server startup, guarded to skip execution in Vercel serverless environments
- Produced 994 real items across all 10 sources in the human checkpoint run with zero errors and zero duplicates

All 5 COLL requirements are satisfied. The system is ready for Phase 2 (Scorer).

---

_Verified: 2026-03-18T08:00:00Z_
_Verifier: Claude (gsd-verifier)_
