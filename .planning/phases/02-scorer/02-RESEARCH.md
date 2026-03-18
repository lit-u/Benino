# Phase 2: Scorer - Research

**Researched:** 2026-03-18
**Domain:** News importance scoring — heuristic + LLM hybrid, SQLite schema extension, OpenRouter integration
**Confidence:** HIGH

---

## Summary

Phase 2 adds a scoring layer directly on top of the existing Phase 1 SQLite storage. Every item already in `seen_urls` (which currently has no score) must receive a 0-100 numeric score, a type label (`breakthrough` / `release` / `update` / `research`), and a pass/fail flag. The scoring pipeline triggers after each collector run and stores results in the same SQLite database so Phase 3 (Telegram bot) can query "all items that passed threshold and have not yet been sent."

The cleanest architecture for this codebase is a **hybrid two-stage scorer**: fast heuristics run first on every item (keyword/source rules produce a provisional score), then a single batched LLM call refines only items that fall into an ambiguous mid-range (30–70 by default). This keeps LLM costs near-zero for obvious items while still catching nuanced breakthroughs. The existing `openai` npm package (v5.20.2, already installed) can call OpenRouter with a single `baseURL` override — no new dependency needed.

SQLite schema extension is the correct approach (not a separate table), because all Phase 3 queries need score + type alongside url/title/source in a single row. Adding four columns to `seen_urls` is a one-liner migration guarded by `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` — zero risk to existing data.

**Primary recommendation:** Hybrid scoring (heuristics first, LLM only for 30-70 range), schema extension via `ALTER TABLE`, OpenRouter via `openai` SDK baseURL override. Score all unscored items after each `runCollector()` call.

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SCOR-01 | Every news item gets a 0-100 importance score | Heuristic layer assigns base score; LLM refines ambiguous range. Stored in `seen_urls.score` column. |
| SCOR-02 | Type classified as: breakthrough / release / update / research | Keyword sets per type + LLM confirmation for ambiguous items. Stored in `seen_urls.item_type`. |
| SCOR-03 | "Breakthrough" items (new models, major releases) score >= 70 | Keyword boost rules ensure GPT-5 / Claude 4 / major model titles hit >= 70 from heuristics alone. |
| SCOR-04 | Multi-source boost: same story from multiple sources = higher score | Title similarity dedup (normalized Levenshtein >= 0.85 on title) groups items; each extra source adds +5, capped at +15. |
| SCOR-05 | Scoring threshold configurable; items below it don't proceed to Telegram | `scoringThreshold` field in `config.json`; items above get `threshold_pass = 1`. |
</phase_requirements>

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `better-sqlite3` | ^12.8.0 | Schema migration + score storage | Already installed; synchronous API ideal for batch ops |
| `openai` | ^5.20.2 | OpenRouter API calls | Already installed; supports any OpenAI-compatible endpoint via `baseURL` |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `node-fetch` | ^3.3.2 | HTTP fallback | Already installed; only if direct fetch needed |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `openai` SDK + baseURL | `axios` direct POST to OpenRouter | openai SDK handles retries, streaming; use it |
| Extending `seen_urls` | Separate `scored_items` table | Separate table adds JOIN complexity for Phase 3 queries; same-row extension is simpler |
| Hybrid scoring | LLM-only scoring | LLM-only: ~10x slower, costs ~€0.002/item; heuristics handle 80% of clear cases free |
| Hybrid scoring | Heuristics-only | Misses nuanced breakthroughs that don't hit keyword lists; LLM safety net needed |

**Installation:** No new packages required. All needed dependencies already installed.

**Verified package versions (from package.json):**
- `better-sqlite3`: ^12.8.0 (confirmed in agent-network/package.json)
- `openai`: ^5.20.2 (confirmed in agent-network/package.json)

---

## Architecture Patterns

### Recommended Project Structure
```
server/services/news-collector/
├── config.json              # EXTENDED: add scoringThreshold, llmModel, llmEnabled
├── index.js                 # EXTENDED: call runScorer() after runCollector()
├── storage/
│   └── db.js                # EXTENDED: initDb() adds 4 columns; addScorerFunctions()
├── sources/                 # unchanged
└── scorer/
    ├── index.js             # runScorer(db) — main entry point
    ├── heuristics.js        # scoreByHeuristics(item) → {score, type}
    └── llm-scorer.js        # scoreBatchWithLLM(items) → [{url_hash, score, type}]
```

### Pattern 1: SQLite Schema Extension (Migration)
**What:** `initDb()` already runs `CREATE TABLE IF NOT EXISTS`. Extend it with `ALTER TABLE ... ADD COLUMN` guards.
**When to use:** Adding columns to an existing live table without destroying data.
**Example:**
```javascript
// In storage/db.js — extend initDb()
// Source: better-sqlite3 docs (synchronous DDL execution)
export function initDb() {
  const db = new Database(DB_PATH);
  db.exec(`
    CREATE TABLE IF NOT EXISTS seen_urls (
      url_hash       TEXT PRIMARY KEY,
      url            TEXT NOT NULL,
      title          TEXT,
      source_id      TEXT,
      seen_at        INTEGER NOT NULL,
      score          INTEGER DEFAULT NULL,
      item_type      TEXT DEFAULT NULL,
      threshold_pass INTEGER DEFAULT NULL,
      scored_at      INTEGER DEFAULT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_seen_at ON seen_urls(seen_at);
    CREATE INDEX IF NOT EXISTS idx_threshold ON seen_urls(threshold_pass, scored_at);
  `);
  // Safe migration for existing databases that have the table but lack new columns
  const addIfMissing = (col, type) => {
    try { db.exec(`ALTER TABLE seen_urls ADD COLUMN ${col} ${type} DEFAULT NULL`); } catch (_) {}
  };
  addIfMissing('score', 'INTEGER');
  addIfMissing('item_type', 'TEXT');
  addIfMissing('threshold_pass', 'INTEGER');
  addIfMissing('scored_at', 'INTEGER');
  return db;
}
```

### Pattern 2: OpenRouter via openai SDK
**What:** The `openai` npm package (OpenAI-compatible) accepts any base URL. OpenRouter exposes `https://openrouter.ai/api/v1`.
**When to use:** Any LLM call in the news-collector service.
**Example:**
```javascript
// Source: OpenRouter docs (https://openrouter.ai/docs/quick-start)
// openai SDK v4+ and v5+ both support this pattern
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
});

const response = await client.chat.completions.create({
  model: 'google/gemini-2.0-flash-001',  // from config — configurable
  messages: [{ role: 'user', content: prompt }],
  temperature: 0.1,   // low temp for deterministic scoring
  max_tokens: 200,
});
```

**Important:** `OPENROUTER_API_KEY` is NOT yet in `.env` or `.env.example`. The plan must add it to both files. The key itself is already used by nanobot (same project, same billing account).

### Pattern 3: Hybrid Scoring Pipeline
**What:** Two-stage process — heuristics first, LLM only for ambiguous mid-range.
**When to use:** Always. This is the recommended architecture.

```
runScorer(db):
  1. Query: SELECT unscored items (score IS NULL)
  2. For each item: heuristicScore(item) → {score, type}
  3. Split:
     - score >= 71 OR score <= 29 → confident, skip LLM
     - score 30-70 → ambiguous, batch for LLM
  4. If ambiguous.length > 0: call LLM once (batch prompt, max 20 items)
  5. Merge scores, apply multi-source boost
  6. Persist: UPDATE seen_urls SET score, item_type, threshold_pass, scored_at
```

### Pattern 4: Multi-Source Boost (Title Similarity Dedup)
**What:** Detect same story from multiple sources by normalized title similarity.
**Why not URL matching:** Same story has completely different URLs on HN vs Anthropic Blog vs HuggingFace Papers.

```javascript
// Approach: normalize title, compute similarity within unscored batch
function normTitle(t) {
  return t.toLowerCase().replace(/[^a-z0-9 ]/g, '').replace(/\s+/g, ' ').trim();
}

function titleSimilarity(a, b) {
  // Jaccard similarity on word sets — simple, no dependencies
  const sa = new Set(normTitle(a).split(' '));
  const sb = new Set(normTitle(b).split(' '));
  const inter = [...sa].filter(w => sb.has(w)).length;
  const union = new Set([...sa, ...sb]).size;
  return inter / union;
}

// Group items with similarity >= 0.5 → apply +5 per extra source, cap +15
```

**Note:** Levenshtein is NOT pre-installed. Jaccard word-set similarity needs zero new dependencies and works well for news titles (identical keywords = same story).

### Pattern 5: Heuristic Keyword Scoring
**What:** Keyword lists with weights assigned per type and significance level.

```javascript
// Breakthrough signals (score += major weight)
const BREAKTHROUGH_KEYWORDS = [
  // Model launches
  'gpt-5', 'gpt-6', 'claude 4', 'claude 3.7', 'gemini 2.5', 'llama 4',
  'new model', 'launches', 'introduces', 'announces', 'release of',
  // Capability jumps
  'agi', 'superhuman', 'surpasses', 'state-of-the-art', 'sota',
  'beats', 'outperforms', 'world record',
  // Major events
  'acquisition', 'acquired', 'billion', 'raises', 'series',
];

const RELEASE_KEYWORDS = [
  'released', 'available', 'now available', 'v2', 'v3', 'version',
  'open source', 'open-source', 'github.com', 'huggingface',
];

const RESEARCH_KEYWORDS = [
  'arxiv', 'paper', 'study', 'research', 'we present', 'we propose',
  'novel', 'approach', 'method', 'framework',
];

// Source-based baseline scores
const SOURCE_BASELINES = {
  'anthropic':         { base: 50, typeHint: 'release' },   // Official blog = significant
  'openai':            { base: 55, typeHint: 'release' },
  'google-ai':         { base: 45, typeHint: 'release' },
  'huggingface-papers':{ base: 40, typeHint: 'research' },
  'hackernews':        { base: 35, typeHint: 'update' },     // Community discussion
  'github-trending':   { base: 30, typeHint: 'release' },
  'github-search':     { base: 25, typeHint: 'update' },
  'taaft':             { base: 20, typeHint: 'update' },     // Tool listings = low signal
  'github-changelog':  { base: 30, typeHint: 'update' },
  'huggingface-models':{ base: 20, typeHint: 'update' },    // Model uploads = low signal
};
```

### Pattern 6: LLM Batch Prompt for Ambiguous Items
**What:** Single API call with multiple items, JSON response.
**When to use:** Items in 30-70 heuristic score range.

```javascript
// Batch up to 20 items per LLM call to minimize API costs
const SCORER_SYSTEM_PROMPT = `You are a tech news importance scorer.
For each news item, return JSON with: score (0-100), type (breakthrough|release|update|research).

Scoring guide:
- 70-100: Major model launches, AGI announcements, billion-dollar acquisitions, landmark research
- 40-69: New tool releases, significant paper, notable open-source project, company news
- 10-39: Minor updates, changelogs, tool listings, routine research
- 0-9: Spam, duplicates, irrelevant

Types:
- breakthrough: New models (GPT-5, Claude 4, etc.), capability leaps, major research findings
- release: Software release, open-source launch, product launch
- update: Changelog, minor version, bug fix, feature addition
- research: ArXiv paper, academic study, technical report

Return ONLY valid JSON array: [{"url_hash":"...","score":85,"type":"breakthrough"}]`;
```

### Anti-Patterns to Avoid
- **Scoring inside the fetcher:** Keep scoring separate from collection. runCollector() collects, runScorer() scores — single responsibility.
- **Scoring in real-time per item:** Batch LLM calls (up to 20 items) are 10-20x cheaper than per-item calls.
- **Storing LLM raw response in DB:** Only store score (INTEGER) and type (TEXT) — normalized fields Phase 3 can query efficiently.
- **Re-scoring already-scored items:** Always filter `WHERE score IS NULL` — idempotent re-runs are critical.
- **Separate `scored_items` table with JOIN:** One table is simpler. Phase 3 does: `SELECT * FROM seen_urls WHERE threshold_pass = 1 AND tg_sent IS NULL`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HTTP to OpenRouter | Custom fetch wrapper | `openai` SDK with `baseURL` override | SDK handles retries, error parsing, streaming |
| Title similarity | Levenshtein distance library | Jaccard word-set (pure JS, zero deps) | Sufficient precision for news titles; no install needed |
| Score persistence | In-memory cache | SQLite column update | Persists across server restarts; Phase 3 needs it |
| LLM JSON parsing | Custom parser | `JSON.parse()` with try/catch fallback | LLM output is JSON array; standard parse works; fallback to heuristic score on parse failure |

**Key insight:** The scoring domain's biggest complexity is the LLM's JSON reliability — always have a heuristic fallback so a bad LLM response degrades gracefully to "heuristic score only" without crashing.

---

## Common Pitfalls

### Pitfall 1: OPENROUTER_API_KEY Not in .env
**What goes wrong:** `scorer/llm-scorer.js` silently gets `undefined` API key; every OpenRouter call returns 401; scorer crashes or falls back to heuristics-only without warning.
**Why it happens:** The key is only in nanobot's config, not agent-network's `.env`.
**How to avoid:** Plan must add `OPENROUTER_API_KEY=` to both `.env` and `.env.example`. Add a startup check: if key is missing, log a warning and run heuristics-only (graceful degradation).
**Warning signs:** `401 Unauthorized` in scorer logs; all items in ambiguous range get heuristic scores only.

### Pitfall 2: Scoring Runs Before DB Column Exists
**What goes wrong:** `runScorer()` is called before `initDb()` runs the migration; `UPDATE seen_urls SET score = ?` hits "no such column" error.
**Why it happens:** If scorer is initialized independently of the server startup path.
**How to avoid:** `runScorer(db)` always receives a db instance returned by `initDb()`. The migration lives in `initDb()` so it runs first by design.

### Pitfall 3: LLM Returns Malformed JSON
**What goes wrong:** `JSON.parse(llmResponse)` throws; entire batch of ambiguous items loses scores.
**Why it happens:** LLMs occasionally wrap JSON in markdown code fences or add explanatory text.
**How to avoid:** Strip markdown fences before parsing: `response.replace(/```json\n?|\n?```/g, '').trim()`. Wrap in try/catch and fall back to heuristic score for items in that batch.
**Warning signs:** `SyntaxError: Unexpected token` in scorer logs.

### Pitfall 4: Multi-Source Boost Applied Incorrectly Across Runs
**What goes wrong:** A story scored in run 1 (from 1 source) gets +5 in run 2 when a second source picks it up — but the first item is already scored (`score IS NULL` filter skips it), so the boost is never applied.
**Why it happens:** Multi-source boost requires rescoring already-scored items.
**How to avoid:** Multi-source grouping runs within the current unscored batch only. If same-story dedup across runs is needed (v2 feature), add a separate `source_count` column and a rescore trigger. For Phase 2, restrict boost to items collected in the same `runCollector()` call.

### Pitfall 5: `ALTER TABLE ADD COLUMN` on Existing Rows
**What goes wrong:** `ALTER TABLE seen_urls ADD COLUMN score INTEGER DEFAULT NULL` fails with "duplicate column name" if called a second time (e.g., server restart).
**Why it happens:** SQLite does not support `IF NOT EXISTS` in `ALTER TABLE`.
**How to avoid:** Wrap in try/catch (ignore "duplicate column" error). See Pattern 1 code example above.

### Pitfall 6: Config Extension Breaks Existing `createRequire` Import
**What goes wrong:** Adding `scoringThreshold` and `llmModel` to `config.json` is safe for JSON (valid), but if the config schema is validated anywhere it might fail.
**Why it happens:** No validation currently exists — confirmed by reading `index.js` (raw `require()` only).
**How to avoid:** Just add fields to `config.json`. No schema validation to break.

---

## Code Examples

### Config Extension
```javascript
// config.json additions (to existing file)
{
  "pollIntervalCron": "0 */6 * * *",
  "maxItemsPerSource": 30,
  "scoring": {
    "enabled": true,
    "threshold": 50,
    "llmEnabled": true,
    "llmModel": "google/gemini-2.0-flash-001",
    "llmAmbiguousMin": 30,
    "llmAmbiguousMax": 70,
    "llmBatchSize": 20
  },
  "sources": [ ... ]
}
```

### runScorer() Entry Point
```javascript
// scorer/index.js
import { createRequire } from 'module';
import { scoreByHeuristics } from './heuristics.js';
import { scoreBatchWithLLM } from './llm-scorer.js';

const require = createRequire(import.meta.url);
const config = require('../config.json');

export async function runScorer(db) {
  const scoringCfg = config.scoring;
  if (!scoringCfg?.enabled) return { scored: 0 };

  const unscored = db.prepare(
    'SELECT url_hash, url, title, source_id, summary FROM seen_urls WHERE score IS NULL'
  ).all();

  if (unscored.length === 0) return { scored: 0 };

  // Stage 1: heuristics on all items
  const withHeuristics = unscored.map(item => ({
    ...item,
    ...scoreByHeuristics(item),
  }));

  // Stage 2: LLM refinement for ambiguous items
  const ambiguous = withHeuristics.filter(
    i => i.score >= scoringCfg.llmAmbiguousMin && i.score <= scoringCfg.llmAmbiguousMax
  );

  if (scoringCfg.llmEnabled && ambiguous.length > 0) {
    const llmResults = await scoreBatchWithLLM(ambiguous, scoringCfg);
    for (const r of llmResults) {
      const item = withHeuristics.find(i => i.url_hash === r.url_hash);
      if (item) { item.score = r.score; item.item_type = r.type; }
    }
  }

  // Stage 3: multi-source boost within this batch
  applyMultiSourceBoost(withHeuristics);

  // Stage 4: persist
  const update = db.prepare(`
    UPDATE seen_urls
    SET score = ?, item_type = ?, threshold_pass = ?, scored_at = ?
    WHERE url_hash = ?
  `);
  const threshold = scoringCfg.threshold;
  const now = Date.now();
  for (const item of withHeuristics) {
    const pass = item.score >= threshold ? 1 : 0;
    update.run(item.score, item.item_type, pass, now, item.url_hash);
  }

  console.log(`[scorer] Scored ${withHeuristics.length} items, ${withHeuristics.filter(i => i.score >= threshold).length} above threshold ${threshold}`);
  return { scored: withHeuristics.length };
}
```

### Integrating Scorer into runCollector()
```javascript
// index.js — add after existing runCollector() exports
import { runScorer } from './scorer/index.js';

export async function runCollector() {
  const db = initDb();
  // ... existing collection logic ...
  db.close();

  // Score newly collected items (open fresh connection — same as collection pattern)
  const db2 = initDb();
  await runScorer(db2);
  db2.close();

  return results;
}
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| LLM-only scoring (expensive) | Hybrid heuristics + LLM | 2024+ (cost optimization trend) | ~80% cost reduction |
| Per-item LLM call | Batched prompts (10-20 items) | 2023+ | 10x faster, 10x cheaper |
| Custom OpenAI-compatible clients | `openai` SDK + baseURL override | openai SDK v4+ | Single package for all providers |
| Separate score table + JOIN | Same-row schema extension | SQLite best practice | Simpler queries for Phase 3 |

---

## Open Questions

1. **OPENROUTER_API_KEY availability**
   - What we know: Key exists in nanobot billing; `.env` does NOT have it currently
   - What's unclear: Does the user know the key value to add to `.env`?
   - Recommendation: Plan task should note "admin must add `OPENROUTER_API_KEY=<key>` to `.env`" and implement graceful fallback (heuristics-only if key absent)

2. **Multi-source boost scope — same run only vs. cross-run**
   - What we know: SCOR-04 says "same story from multiple sources = higher score"
   - What's unclear: Should boost apply when source 2 is collected in a later 6h run (after source 1 was already scored)?
   - Recommendation: Phase 2 — same-batch only (simpler, no rescore needed). Cross-run boost is SCOR-06 territory (v2). Success criteria says "three sources scores higher than one source" — testable with a single test batch.

3. **LLM scoring cost estimate**
   - What we know: OpenRouter credit ~€6; `google/gemini-2.0-flash-001` is cheap
   - Estimate: 994 items Phase 1 collected. If 30% ambiguous = ~300 items / 20 per batch = 15 LLM calls. At ~€0.0002/call = €0.003 total for all existing items. Normal ongoing cost: ~2-5 LLM calls per 6h run.
   - Recommendation: Budget risk is negligible. Proceed without throttle for Phase 2.

---

## Validation Architecture

> `workflow.nyquist_validation` not set in config.json — treating as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | None detected in news-collector service (no jest/vitest config) |
| Config file | None — Wave 0 must create minimal test harness OR use manual smoke test |
| Quick run command | `node -e "import('./scorer/index.js').then(m => console.log('ok'))"` (module load test) |
| Full suite command | Manual: `node agent-network/server/services/news-collector/scorer/test-scorer.js` |

> Note: Agent-network has Playwright E2E tests but no unit test framework. The scorer is a Node.js service module, not a UI component. Playwright is not appropriate here. A lightweight manual smoke test script is the correct approach for this service.

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SCOR-01 | Every item gets 0-100 score | unit smoke | `node scorer/test-scorer.js` | ❌ Wave 0 |
| SCOR-02 | Type is breakthrough/release/update/research | unit smoke | `node scorer/test-scorer.js` | ❌ Wave 0 |
| SCOR-03 | GPT-5 launch item scores >= 70 | unit smoke | `node scorer/test-scorer.js` | ❌ Wave 0 |
| SCOR-04 | 3-source item scores higher than 1-source | unit smoke | `node scorer/test-scorer.js` | ❌ Wave 0 |
| SCOR-05 | Threshold change filters correctly | unit smoke | `node scorer/test-scorer.js` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** Import sanity: `node --input-type=module <<< "import './scorer/index.js'"` (confirms no syntax errors)
- **Per wave merge:** Run `node scorer/test-scorer.js` — must print all 5 assertions PASS
- **Phase gate:** Full smoke test green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `server/services/news-collector/scorer/test-scorer.js` — covers SCOR-01 through SCOR-05 with in-memory SQLite + fake items
- [ ] No framework install needed — pure Node.js assertions (`assert` module)

---

## Sources

### Primary (HIGH confidence)
- Direct code inspection of `agent-network/server/services/news-collector/storage/db.js` — confirmed schema, existing columns, `better-sqlite3` usage pattern
- Direct code inspection of `agent-network/server/services/news-collector/index.js` — confirmed `runCollector()` shape, db.close() pattern
- Direct code inspection of `agent-network/package.json` — confirmed `openai@^5.20.2` and `better-sqlite3@^12.8.0` are installed
- Direct inspection of `agent-network/.env` — confirmed `OPENROUTER_API_KEY` is absent, `GROQ_API_KEY` and `OPENAI_API_KEY` exist
- OpenRouter API docs pattern: `baseURL: 'https://openrouter.ai/api/v1'` with `openai` SDK — standard integration, confirmed by OpenRouter's own quick-start documentation

### Secondary (MEDIUM confidence)
- Hybrid scoring approach (heuristics + LLM for ambiguous range): established pattern in production news-scoring systems (2024-2025 trend); consistent with cost optimization best practices
- Jaccard similarity for title dedup: suitable for news titles with 5-15 words; documented alternative to Levenshtein when no library is available

### Tertiary (LOW confidence)
- Keyword lists for breakthrough/release/update/research classification: derived from analysis of source types and AI news patterns; should be validated against actual collected items in `news.db` before finalizing

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all packages confirmed installed; no new dependencies needed
- Architecture: HIGH — patterns derived directly from existing Phase 1 code style
- SQLite migration: HIGH — `ALTER TABLE` try/catch is standard SQLite pattern for additive migrations
- OpenRouter integration: HIGH — `openai` SDK baseURL override is official OpenRouter guidance; SDK confirmed installed
- Keyword lists: MEDIUM — reasonable starting set; may need tuning after first real scoring run
- Multi-source boost: HIGH — Jaccard similarity, no new deps, logic is clear
- Pitfalls: HIGH — all derived from direct code inspection or known SQLite/LLM behaviors

**Research date:** 2026-03-18
**Valid until:** 2026-04-18 (stable domain — SQLite and OpenRouter patterns are not rapidly changing)
