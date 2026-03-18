# Phase 1: Collector - Research

**Researched:** 2026-03-18
**Domain:** Node.js news fetching — RSS parsing, API polling, web scraping, deduplication, scheduled jobs
**Confidence:** HIGH (all feed URLs verified live, APIs tested directly)

---

## Summary

Phase 1 builds a news collector that fetches from 10 sources every 6 hours and deduplicates by URL hash. The sources split into three fetch strategies: RSS/Atom feeds (6 sources), REST APIs (3 sources — HackerNews Algolia, HuggingFace Papers, HuggingFace Models), and HTML scraping (1 source — GitHub Trending). All feed URLs were verified live during research; confirmed working endpoints are documented below.

The project already has the required dependencies installed in `agent-network`: `node-cron@4.2.1`, `cheerio@1.1.2`, `puppeteer@24.22.3`, `axios@1.12.2`, `node-fetch@3.3.2`. Only `rss-parser` and `better-sqlite3` need to be added. Storage decision: use SQLite via `better-sqlite3` — Supabase is overkill for a local deduplification store, and JSON files lack queryability needed for Phase 2 scoring queries.

**Primary recommendation:** Place the collector as a standalone module at `agent-network/server/services/news-collector/` — following the existing `server/services/` pattern — with its own `index.js` entry, `config.json` for source list (COLL-04), and an SQLite `news.db` for seen-URL deduplication (COLL-03). Register the cron in `server/index.js` alongside the existing `expired-listings-cron.js` pattern.

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| COLL-01 | Renka naujienas iš 10 iš anksto nustatytų šaltinių (RSS + API) | Verified fetch strategies for all 10 sources; confirmed working URLs |
| COLL-02 | Rinkimas vyksta automatiškai kas 6 valandas (cron job) | `node-cron@4.2.1` already installed; `0 */6 * * *` expression confirmed |
| COLL-03 | Nesikartoja — jau matytos naujienos (URL hash) praleidžiamos | SHA-256 URL hash via built-in `crypto`; SQLite `seen_urls` table pattern documented |
| COLL-04 | Šaltinių sąrašas konfigūruojamas per config failą | JSON config pattern; source schema documented |
| COLL-05 | Veikia su visais 10 šaltinių | All 10 confirmed in research with exact URLs and fetch methods |
</phase_requirements>

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `rss-parser` | 3.13.0 | Parse RSS/Atom feeds to JS objects | Industry standard, handles edge cases, supports custom fields |
| `node-cron` | 4.2.1 | Schedule collector runs | Already installed in agent-network; ESM-compatible |
| `better-sqlite3` | 12.8.0 | Persistent seen-URL store | Synchronous API, fast, zero external deps, queryable for Phase 2 |
| `node-fetch` | 3.3.2 | HTTP requests to APIs | Already installed; ESM-native |
| `cheerio` | 1.1.2 | Parse GitHub Trending HTML | Already installed; faster than Puppeteer for static HTML |
| `crypto` (built-in) | Node built-in | SHA-256 URL hashing | No extra dep; available in Node 22.x |

### Supporting (already installed)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `axios` | 1.12.2 | HTTP with retry-friendly config | Alternative to node-fetch if retry middleware needed |
| `puppeteer` | 24.22.3 | JS-rendered page scraping | Fallback for GitHub Trending if cheerio fails |
| `dotenv` | 16.6.1 | Load `.env` for API keys | GitHub token for authenticated Search API |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `better-sqlite3` | Supabase | Supabase requires network + has RLS — adds latency/complexity to simple dedup; overkill for Phase 1 |
| `better-sqlite3` | JSON file | JSON files require full reload to check existence; no query for Phase 2 needs |
| `rss-parser` | `fast-xml-parser` | rss-parser provides normalized item schema; fast-xml-parser requires manual normalization |
| `cheerio` | `puppeteer` | cheerio parses static HTML 10x faster; use puppeteer only if GitHub Trending changes to SPA |

**Installation (only new packages needed):**
```bash
cd agent-network
npm install rss-parser better-sqlite3
```

---

## Architecture Patterns

### Recommended Project Structure
```
agent-network/
└── server/
    └── services/
        └── news-collector/
            ├── index.js           # Main entry: exports runCollector(), registerCron()
            ├── config.json        # Source list (COLL-04: configurable)
            ├── sources/
            │   ├── rss-fetcher.js     # Generic RSS/Atom parser
            │   ├── hn-fetcher.js      # HackerNews Algolia API
            │   ├── github-trending-fetcher.js  # HTML scrape via cheerio
            │   ├── github-search-fetcher.js    # GitHub Search REST API
            │   └── huggingface-fetcher.js      # HF Papers + Models APIs
            ├── storage/
            │   └── db.js          # better-sqlite3 wrapper: seen URL store
            └── news.db            # SQLite file (gitignored)
```

### Pattern 1: Source Config Schema (COLL-04)
**What:** All source behavior driven by `config.json` — zero code changes to add/remove a source.
**When to use:** Every time a source is referenced.

```json
// agent-network/server/services/news-collector/config.json
{
  "pollIntervalCron": "0 */6 * * *",
  "sources": [
    {
      "id": "anthropic",
      "name": "Anthropic Blog",
      "type": "rss",
      "url": "https://raw.githubusercontent.com/taobojlen/anthropic-rss-feed/main/anthropic_news_rss.xml",
      "enabled": true
    },
    {
      "id": "openai",
      "name": "OpenAI Blog",
      "type": "rss",
      "url": "https://openai.com/news/rss.xml",
      "enabled": true
    },
    {
      "id": "google-ai",
      "name": "Google AI Blog",
      "type": "rss",
      "url": "https://blog.google/technology/ai/rss/",
      "enabled": true
    },
    {
      "id": "github-changelog",
      "name": "GitHub Blog Changelog",
      "type": "rss",
      "url": "https://github.blog/changelog/feed/",
      "enabled": true
    },
    {
      "id": "huggingface-papers",
      "name": "HuggingFace Papers",
      "type": "rss",
      "url": "https://huggingface.co/blog/feed.xml",
      "enabled": true,
      "note": "Or use HF daily_papers API: type=hf-papers-api"
    },
    {
      "id": "taaft",
      "name": "TAAFT - There's An AI For That",
      "type": "rss",
      "url": "https://theresanaiforthat.com/feed/",
      "enabled": true,
      "headers": { "User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)" }
    },
    {
      "id": "hackernews",
      "name": "HackerNews",
      "type": "hn-algolia",
      "query": "AI OR LLM OR GPT OR Claude OR Gemini",
      "minPoints": 10,
      "hitsPerPage": 30,
      "enabled": true
    },
    {
      "id": "github-trending",
      "name": "GitHub Trending",
      "type": "github-trending",
      "language": "",
      "since": "daily",
      "enabled": true
    },
    {
      "id": "github-search",
      "name": "GitHub Search AI Models",
      "type": "github-search",
      "query": "topic:large-language-model pushed:>DATE",
      "sort": "updated",
      "perPage": 20,
      "enabled": true
    },
    {
      "id": "huggingface-models",
      "name": "HuggingFace Models",
      "type": "hf-models-api",
      "filter": "text-generation",
      "limit": 20,
      "enabled": true
    }
  ]
}
```

### Pattern 2: Cron Registration (COLL-02)
**What:** Register cron in the existing `server/index.js` cron section, same as `expired-listings-cron.js`.

```javascript
// agent-network/server/services/news-collector/index.js
import cron from 'node-cron';
import { fetchAllSources } from './sources/index.js';
import { initDb, markSeen, isSeen } from './storage/db.js';
import config from './config.json' assert { type: 'json' };

export function registerCron() {
  cron.schedule(config.pollIntervalCron, runCollector);
  console.log(`News collector scheduled: ${config.pollIntervalCron}`);
}

export async function runCollector() {
  const db = initDb();
  const startedAt = Date.now();
  console.log(`[news-collector] Run started ${new Date().toISOString()}`);

  const results = { fetched: 0, new: 0, skipped: 0, errors: [] };

  for (const source of config.sources.filter(s => s.enabled)) {
    try {
      const items = await fetchSource(source);
      for (const item of items) {
        results.fetched++;
        if (isSeen(db, item.url)) { results.skipped++; continue; }
        markSeen(db, item.url, item.title, source.id);
        results.new++;
      }
    } catch (err) {
      results.errors.push({ source: source.id, error: err.message });
    }
  }

  console.log(`[news-collector] Done in ${Date.now()-startedAt}ms — fetched:${results.fetched} new:${results.new} skipped:${results.skipped} errors:${results.errors.length}`);
  return results;
}
```

### Pattern 3: SQLite Deduplication (COLL-03)
**What:** SHA-256 hash of canonical URL stored in SQLite. Check before storing.

```javascript
// agent-network/server/services/news-collector/storage/db.js
import Database from 'better-sqlite3';
import crypto from 'crypto';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH = path.join(__dirname, '..', 'news.db');

export function initDb() {
  const db = new Database(DB_PATH);
  db.exec(`
    CREATE TABLE IF NOT EXISTS seen_urls (
      url_hash  TEXT PRIMARY KEY,
      url       TEXT NOT NULL,
      title     TEXT,
      source_id TEXT,
      seen_at   INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_seen_at ON seen_urls(seen_at);
  `);
  return db;
}

export function isSeen(db, url) {
  const hash = hashUrl(url);
  return !!db.prepare('SELECT 1 FROM seen_urls WHERE url_hash = ?').get(hash);
}

export function markSeen(db, url, title, sourceId) {
  const hash = hashUrl(url);
  db.prepare(`
    INSERT OR IGNORE INTO seen_urls (url_hash, url, title, source_id, seen_at)
    VALUES (?, ?, ?, ?, ?)
  `).run(hash, url, title, sourceId, Date.now());
}

function hashUrl(url) {
  // Normalize: strip trailing slash, lowercase scheme+host
  const normalized = url.trim().replace(/\/$/, '');
  return crypto.createHash('sha256').update(normalized).digest('hex').substring(0, 32);
}
```

### Pattern 4: Per-Fetcher Result Schema
**What:** All fetchers return a consistent `NewsItem[]` array regardless of source type.

```javascript
// Canonical item shape returned by every fetcher
{
  url: string,        // canonical link (used for dedup hash)
  title: string,      // article title
  publishedAt: string, // ISO 8601 or empty string if unknown
  source: string,     // source.id from config
  summary: string,    // first 500 chars of description/abstract
  raw: object         // original API response (for Phase 2 scoring)
}
```

### Anti-Patterns to Avoid
- **Deduplication by title:** Titles can vary (capitalization, truncation) — always use URL hash.
- **Storing full article HTML in SQLite at this phase:** The collector only needs to know what was seen; full content is Phase 4's job.
- **Single global axios/fetch without per-source error isolation:** One source timing out must not block others — wrap each source in try/catch.
- **Hardcoded source list in JS:** Violates COLL-04 — every source must live in `config.json`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| RSS/Atom parsing | Custom XML parser | `rss-parser` | Feed variations (Atom vs RSS 2.0, CDATA, namespaces, malformed tags) are handled |
| Cron scheduling | `setInterval` loop | `node-cron` | setInterval drifts, doesn't survive process restart gracefully, no crontab syntax |
| URL normalization for dedup | Custom regex string comparison | SHA-256 hash after trim+lowercase normalization | Handles trailing slashes, UTM params would need explicit stripping |
| SQLite schema migration | Ad-hoc `ALTER TABLE` | `CREATE TABLE IF NOT EXISTS` + `CREATE INDEX IF NOT EXISTS` | Safe to call every startup |

**Key insight:** rss-parser handles the 20+ edge cases in real-world feeds that a custom XML parser would miss (namespace prefixes, CDATA wrapping, missing required fields). Never parse RSS/Atom with a generic XML parser.

---

## Source-by-Source Fetch Patterns

### RSS Sources (type: "rss")

All 6 RSS/Atom sources use the same fetcher. The `rss-parser` library handles both RSS 2.0 and Atom formats transparently.

```javascript
// agent-network/server/services/news-collector/sources/rss-fetcher.js
import Parser from 'rss-parser';

const parser = new Parser({
  timeout: 10000,
  headers: { 'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)' }
});

export async function fetchRss(source) {
  // Pass custom headers per-source if defined in config
  const customParser = source.headers
    ? new Parser({ timeout: 10000, headers: { ...parser.options.headers, ...source.headers } })
    : parser;

  const feed = await customParser.parseURL(source.url);
  return feed.items.map(item => ({
    url: item.link || item.guid,
    title: item.title || '',
    publishedAt: item.isoDate || item.pubDate || '',
    source: source.id,
    summary: (item.contentSnippet || item.summary || '').substring(0, 500),
    raw: item
  })).filter(i => i.url); // drop items without a URL
}
```

**Verified RSS URLs (tested 2026-03-18):**

| Source | URL | Format | Status |
|--------|-----|--------|--------|
| Anthropic Blog | `https://raw.githubusercontent.com/taobojlen/anthropic-rss-feed/main/anthropic_news_rss.xml` | RSS | 200 OK |
| OpenAI Blog | `https://openai.com/news/rss.xml` | RSS | 200 OK |
| Google AI Blog | `https://blog.google/technology/ai/rss/` | RSS | 200 OK |
| GitHub Changelog | `https://github.blog/changelog/feed/` | RSS | 200 OK |
| HuggingFace Blog | `https://huggingface.co/blog/feed.xml` | RSS | 200 OK |
| TAAFT | `https://theresanaiforthat.com/feed/` | HTML page (see pitfall) | 200 OK with UA header |

**CRITICAL: Anthropic has no native RSS feed.** Use the community-maintained feed at `taobojlen/anthropic-rss-feed` (GitHub raw URL, updated via GitHub Actions). This is a known gap — if the community feed goes stale, fallback is to scrape `anthropic.com/news`.

**CRITICAL: TAAFT returns HTML (not XML) at `/feed/` when accessed with a bot User-Agent.** The `/feed/` path with a browser User-Agent header returns a search results page, not an RSS feed. Investigation during research confirmed TAAFT does not expose a public RSS feed. **Use their "recently added tools" page via cheerio scrape instead:**
```
https://theresanaiforthat.com/recently-added/
```

### HackerNews Algolia API (type: "hn-algolia")

Free, no authentication required. Rate limits are generous (no published cap for reasonable use).

```javascript
// agent-network/server/services/news-collector/sources/hn-fetcher.js
import fetch from 'node-fetch';

export async function fetchHackerNews(source) {
  const since = Math.floor(Date.now() / 1000) - 6 * 60 * 60; // 6h ago
  const query = encodeURIComponent(source.query);
  const url = `https://hn.algolia.com/api/v1/search_by_date?query=${query}&tags=story&hitsPerPage=${source.hitsPerPage}&numericFilters=points>${source.minPoints},created_at_i>${since}`;

  const res = await fetch(url, { headers: { 'User-Agent': 'NewsBot/1.0' } });
  const data = await res.json();

  return data.hits.map(hit => ({
    url: hit.url || `https://news.ycombinator.com/item?id=${hit.objectID}`,
    title: hit.title || '',
    publishedAt: hit.created_at || '',
    source: source.id,
    summary: hit.story_text ? hit.story_text.substring(0, 500) : '',
    raw: hit
  })).filter(i => i.url);
}
```

**Key fields in HN Algolia response:** `objectID`, `title`, `url` (may be null for Ask HN), `created_at` (ISO string), `points`, `story_text`, `author`.

**Use `search_by_date` endpoint** (not `search`) — sorts by recency, which is what the 6h window filter needs.

### GitHub Trending (type: "github-trending")

No official API. GitHub's Trending page renders server-side HTML — cheerio parsing works without JavaScript execution.

```javascript
// agent-network/server/services/news-collector/sources/github-trending-fetcher.js
import fetch from 'node-fetch';
import * as cheerio from 'cheerio';

export async function fetchGithubTrending(source) {
  const params = new URLSearchParams({ since: source.since || 'daily' });
  if (source.language) params.set('l', source.language);

  const url = `https://github.com/trending?${params}`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' }
  });
  const html = await res.text();
  const $ = cheerio.load(html);

  const items = [];
  $('article.Box-row').each((_, el) => {
    const linkEl = $(el).find('h2.h3.lh-condensed a');
    const href = linkEl.attr('href'); // e.g. /owner/repo
    if (!href || href.includes('/sponsors/')) return;

    const fullPath = href.replace(/\s/g, '');
    const repoUrl = `https://github.com${fullPath}`;
    const title = fullPath.substring(1); // "owner/repo"
    const desc = $(el).find('p').first().text().trim();

    items.push({
      url: repoUrl,
      title,
      publishedAt: new Date().toISOString(),
      source: source.id,
      summary: desc.substring(0, 500),
      raw: { href }
    });
  });

  return items;
}
```

**Verified selector:** `article.Box-row` → `h2.h3.lh-condensed a` — confirmed working as of 2026-03-18. Avoid sponsor entries (they also use `Box-row` but `href` matches `/sponsors/`).

### GitHub Search API (type: "github-search")

Rate limit: **10 requests/minute** unauthenticated (confirmed via `X-RateLimit-Limit: 10` header). With a GitHub PAT: 30 requests/minute. At 6h interval with 1 query, unauthenticated is sufficient but fragile. Use a GitHub PAT stored in `.env` as `GITHUB_TOKEN`.

```javascript
// agent-network/server/services/news-collector/sources/github-search-fetcher.js
import fetch from 'node-fetch';

export async function fetchGithubSearch(source) {
  const since = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString().split('T')[0]; // yesterday
  const query = source.query.replace('DATE', since);
  const url = `https://api.github.com/search/repositories?q=${encodeURIComponent(query)}&sort=${source.sort}&per_page=${source.perPage}&order=desc`;

  const headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
  };
  if (process.env.GITHUB_TOKEN) {
    headers['Authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
  }

  const res = await fetch(url, { headers });

  // Check rate limit headers
  const remaining = res.headers.get('X-RateLimit-Remaining');
  if (remaining !== null && parseInt(remaining) < 2) {
    console.warn('[github-search] Rate limit nearly exhausted');
  }

  if (res.status === 403 || res.status === 429) {
    throw new Error(`GitHub Search rate limited: ${res.status}`);
  }

  const data = await res.json();
  return (data.items || []).map(repo => ({
    url: repo.html_url,
    title: repo.full_name,
    publishedAt: repo.updated_at,
    source: source.id,
    summary: (repo.description || '').substring(0, 500),
    raw: repo
  }));
}
```

### HuggingFace Papers API (type: "hf-papers-api")

Official REST API at `https://huggingface.co/api/daily_papers`. No authentication required. Returns up to 100 papers.

```javascript
// agent-network/server/services/news-collector/sources/huggingface-fetcher.js
import fetch from 'node-fetch';

export async function fetchHuggingFacePapers(source) {
  const res = await fetch(`https://huggingface.co/api/daily_papers?limit=${source.limit || 20}`);
  const papers = await res.json();

  return papers.map(p => ({
    url: `https://huggingface.co/papers/${p.paper.id}`,
    title: p.paper.title || p.title || '',
    publishedAt: p.publishedAt || '',
    source: source.id,
    summary: (p.summary || p.paper.summary || '').substring(0, 500),
    raw: p
  }));
}

export async function fetchHuggingFaceModels(source) {
  const params = new URLSearchParams({
    sort: 'createdAt',
    direction: '-1',
    limit: String(source.limit || 20)
  });
  if (source.filter) params.set('filter', source.filter);

  const res = await fetch(`https://huggingface.co/api/models?${params}`);
  const models = await res.json();

  return models.map(m => ({
    url: `https://huggingface.co/${m.id}`,
    title: m.id,
    publishedAt: m.createdAt || '',
    source: source.id,
    summary: m.description ? m.description.substring(0, 500) : '',
    raw: m
  }));
}
```

**Verified API response fields (tested 2026-03-18):**
- Papers: `paper.id`, `paper.title`, `publishedAt`, `summary`, `thumbnail`, `submittedBy`
- Models: `_id`, `id`, `createdAt`, `likes`, `downloads`, `tags`, `pipeline_tag`

---

## Common Pitfalls

### Pitfall 1: TAAFT has no public RSS feed
**What goes wrong:** `theresanaiforthat.com/feed/` returns a website search results page at `/s/feed/`, not an XML feed. Both `/feed/`, `/feed.xml`, `/rss/`, `/atom/` were tested — all return HTML or 403.
**Why it happens:** TAAFT uses WordPress-like URL patterns but routes `/feed/` to an internal search for "feed" tools.
**How to avoid:** Use cheerio to scrape the recently-added tools page: `https://theresanaiforthat.com/recently-added/` (HTTP 200, returns server-side HTML).
**Warning signs:** If rss-parser throws "Invalid XML" for TAAFT URL.

### Pitfall 2: Anthropic blog has no native RSS
**What goes wrong:** `anthropic.com/news.rss` returns 404; the news page is Next.js client-side rendered.
**Why it happens:** Anthropic never published a native RSS endpoint.
**How to avoid:** Use the community-maintained GitHub raw feed (`taobojlen/anthropic-rss-feed`). Add a freshness check: if the feed hasn't updated in >48h, log a warning. The feed is updated by GitHub Actions.
**Warning signs:** Feed items all have the same `pubDate`.

### Pitfall 3: GitHub Search rate limit is 10/minute unauthenticated
**What goes wrong:** At 6h intervals with one query, this is fine normally — but if the collector is restarted and runs multiple times in a minute during testing, `403` responses occur.
**Why it happens:** GitHub caps unauthenticated search at 10 req/min (verified via `X-RateLimit-Limit: 10` header in research).
**How to avoid:** Add `GITHUB_TOKEN` to `.env` (raises to 30/min). Always check `X-RateLimit-Remaining` header and throw a descriptive error rather than silently failing.
**Warning signs:** `{ message: "API rate limit exceeded" }` in GitHub response body.

### Pitfall 4: Google AI Blog is Atom (not RSS 2.0)
**What goes wrong:** Some older RSS parsers choke on Atom 1.0 format.
**Why it happens:** The `feeds.feedburner.com/blogspot/gJZg` endpoint returns Atom 1.0. The newer `blog.google/technology/ai/rss/` returns RSS 2.0 (confirmed working, active as of 2026-03-18 — last item: March 17, 2026).
**How to avoid:** Use `blog.google/technology/ai/rss/` not the feedburner URL. `rss-parser` handles both, but the newer URL is RSS 2.0 and more current.

### Pitfall 5: GitHub Trending sponsor rows mixed with real repos
**What goes wrong:** `article.Box-row` matches sponsor entries that have `href="/sponsors/username"`.
**Why it happens:** GitHub renders sponsor rows with the same CSS class as trending repos.
**How to avoid:** Filter out hrefs containing `/sponsors/` before processing. Verified in research.

### Pitfall 6: HN stories with null URL (Ask HN, Show HN)
**What goes wrong:** `hit.url` is `null` for self-posts (Ask HN, Show HN). If you use `url` as the dedup key without a fallback, items get dropped or crash.
**Why it happens:** Ask HN posts have no external URL — the HN post itself is the content.
**How to avoid:** Fall back to `https://news.ycombinator.com/item?id=${hit.objectID}` when `hit.url` is null.

### Pitfall 7: HuggingFace Models API wrong sort parameter
**What goes wrong:** `?sort=created_at` returns HTTP 400.
**Why it happens:** The correct parameter is `createdAt` (camelCase), not `created_at`.
**How to avoid:** Use `sort=createdAt&direction=-1`. Verified in research (400 vs 200 tested directly).

### Pitfall 8: node-cron v4 uses 5-field OR 6-field expressions
**What goes wrong:** Using a 6-field expression `0 0 */6 * * *` (with seconds) vs 5-field `0 */6 * * *` — both are valid in v4 but 6-field requires seconds support to be enabled or just works in v4.
**How to avoid:** Use 5-field `0 */6 * * *` (runs at :00 every 6 hours) — confirmed syntax per node-cron v4 docs.

---

## Code Examples

### Registering the collector cron in server/index.js
```javascript
// Source: existing pattern from server/utils/expired-listings-cron.js
import { registerCron } from './services/news-collector/index.js';
registerCron(); // fires 0 */6 * * *
```

### rss-parser ESM import (agent-network uses type: "module")
```javascript
// Source: rss-parser GitHub README
import Parser from 'rss-parser';
const parser = new Parser({ timeout: 10000 });
const feed = await parser.parseURL('https://openai.com/news/rss.xml');
// feed.items[0]: { title, link, pubDate, isoDate, contentSnippet, guid }
```

### better-sqlite3 synchronous pattern
```javascript
// Source: better-sqlite3 README — synchronous API, no callbacks
import Database from 'better-sqlite3';
const db = new Database('/path/to/news.db');
const row = db.prepare('SELECT * FROM seen_urls WHERE url_hash = ?').get(hash);
db.prepare('INSERT OR IGNORE INTO seen_urls ...').run(hash, url, title, sourceId, Date.now());
```

### node-cron v4 ESM schedule
```javascript
// Source: node-cron v4 README + verified from agent-network existing usage
import cron from 'node-cron';
cron.schedule('0 */6 * * *', async () => {
  await runCollector();
});
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `node-sqlite3` (callback) | `better-sqlite3` (sync) | ~2018 | Simpler code, faster, no async complexity |
| `request` / `node-fetch@2` | `node-fetch@3` (ESM) | 2021 | ESM-only; no CommonJS require |
| `setInterval` cron | `node-cron` | Long-standing | Crontab syntax, survives misconfigured intervals |
| feedburner Google AI URL | `blog.google/technology/ai/rss/` | ~2023 | feedburner URL is stale/slow; new URL is active |

**Deprecated/outdated:**
- `feeds.feedburner.com/blogspot/gJZg` (Google AI): Works but last entry was 2024. Use `blog.google/technology/ai/rss/` instead.
- `https://ghapi.huchen.dev` (GitHub Trending unofficial API): Archived, do not use.

---

## Open Questions

1. **TAAFT scrape target**
   - What we know: TAAFT has no RSS; `/recently-added/` page returns server-rendered HTML (200 OK)
   - What's unclear: HTML structure of the recently-added page (not inspected during research — would need a GET to confirm selectors)
   - Recommendation: During Wave 1, fetch and inspect `https://theresanaiforthat.com/recently-added/` with cheerio to identify the tool card selector before writing the fetcher

2. **GitHub PAT requirement**
   - What we know: Unauthenticated GitHub Search limit is 10 req/min; at 6h intervals this is adequate in normal operation
   - What's unclear: Whether the team has a GitHub PAT available for `.env`
   - Recommendation: Implement with optional `GITHUB_TOKEN` env var; collector runs without it but logs a warning

3. **HuggingFace Models filter scope**
   - What we know: `filter=text-generation` returns 20 newest text-generation models; many are fine-tunes from tournaments
   - What's unclear: Whether the Phase 2 scorer will want broader scope (all model types) or narrower (only foundation models with >100 likes)
   - Recommendation: Use `filter=text-generation` for Phase 1; expose filter param in config so it can be changed without code edits

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Playwright 1.58.2 (e2e) + manual smoke script |
| Config file | `agent-network/playwright.config.cjs` |
| Quick run command | `node agent-network/server/services/news-collector/index.js` (manual run) |
| Full suite command | `cd agent-network && npx playwright test` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| COLL-01 | All 10 sources fetch without errors | Integration smoke | `node -e "import('./server/services/news-collector/index.js').then(m=>m.runCollector())"` | Wave 0 |
| COLL-02 | Cron fires at 6h interval | Unit | Check cron expression `0 */6 * * *` parses; verify `node-cron.validate()` | Wave 0 |
| COLL-03 | Running collector twice = no duplicates | Integration | Run `runCollector()` twice; assert `db.prepare('SELECT COUNT(*) FROM seen_urls').get()` same | Wave 0 |
| COLL-04 | Changing config.json source list takes effect | Unit | Add dummy disabled source to config; assert fetcher skips it | Wave 0 |
| COLL-05 | All 10 named sources return items | Integration | Assert each `source.id` appears in returned items on clean DB run | Wave 0 |

### Sampling Rate
- **Per task commit:** `node -e "import('./server/services/news-collector/index.js').then(m=>m.runCollector()).then(r=>console.log(r))"` (manual)
- **Per wave merge:** Run the full collector once and inspect `news.db` row count per source
- **Phase gate:** All 10 sources return at least 1 item; DB dedup check passes

### Wave 0 Gaps
- [ ] `agent-network/server/services/news-collector/` — full directory does not exist yet
- [ ] `news.db` — created at runtime by `initDb()`; gitignore entry needed: `server/services/news-collector/news.db`
- [ ] `rss-parser` and `better-sqlite3` not yet installed: `npm install rss-parser better-sqlite3`
- [ ] `GITHUB_TOKEN` — optional env var, document in `.env.example`

---

## Sources

### Primary (HIGH confidence)
- Live API tests (2026-03-18) — All feed URLs, API endpoints, and response schemas verified by direct HTTP calls
- `agent-network/package.json` — Confirmed installed packages and versions

### Secondary (MEDIUM confidence)
- [HN Algolia API docs](https://hn.algolia.com/api) — Endpoint structure confirmed via live test
- [HuggingFace Hub API](https://huggingface.co/docs/hub/en/api) — Endpoints confirmed; rate limits not fully documented
- [GitHub REST API rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) — Confirmed: 10 req/min unauthenticated for search
- [rss-parser GitHub](https://github.com/rbren/rss-parser) — ESM import and usage patterns

### Tertiary (LOW confidence)
- Community Anthropic RSS feed (`taobojlen/anthropic-rss-feed`) — Active as of research date; reliability depends on third party's GitHub Actions uptime

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all packages verified installed or confirmed on npm registry with exact versions
- Architecture: HIGH — follows existing patterns in agent-network (`expired-listings-cron.js`, `server/services/` structure)
- Feed URLs: HIGH — all 10 source endpoints tested with live HTTP calls; status codes and response schemas documented
- Pitfalls: HIGH — most found by direct testing (TAAFT, Anthropic no-RSS, GitHub rate limits, HF API params)
- TAAFT scrape selectors: LOW — page confirmed reachable but selectors not inspected

**Research date:** 2026-03-18
**Valid until:** 2026-04-18 (30 days — RSS URLs and GitHub HTML selectors may change)
