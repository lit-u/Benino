---
phase: 04-writer-publisher
verified: 2026-03-19T00:00:00Z
status: human_needed
score: 8/8 must-haves verified
re_verification:
  previous_status: gaps_found
  previous_score: 6/8
  gaps_closed:
    - "The LLM model used comes from config.json writer.model — changing the value changes the model without code edits"
    - "The Telegram bot sends admin a confirmation message with draft_path and title after successful accept"
  gaps_remaining: []
  regressions: []
human_verification:
  - test: "Run the server, have a real DB item in seen_urls with tg_status='pending', press Accept in the Telegram bot, observe what the admin sees in Telegram after the spinning indicator"
    expected: "Admin sees the spinner replaced by a message showing draft title and path, e.g. 'Draft saved: [Title] Path: drafts/<hash>.json'"
    why_human: "Requires live bot token, Telegram session, real DB row, and actual button press — cannot verify Telegram message delivery programmatically"
  - test: "Check generated draft JSON at agent-network/server/services/news-collector/drafts/<hash>.json after a successful accept call"
    expected: "File exists, oldboyBody contains coherent Lithuanian narrative text (not empty, not garbled), tags is array of 3-5 lowercase Lithuanian strings, category is a valid value"
    why_human: "Requires actual OpenRouter API call to produce; static analysis cannot verify LLM output quality"
---

# Phase 4: Writer + Publisher Verification Report

**Phase Goal:** An accepted news item is transformed into a full blog post via LLM and published (or drafted) to Agent Network under the OldBoy-RSS author
**Verified:** 2026-03-19
**Status:** human_needed (all automated checks pass — two items need live system testing)
**Re-verification:** Yes — after gap closure via plan 04-04

## Important Context: User-Approved Overrides

The following deviations from the original plan are intentional and human-verified:

- **Draft-to-disk instead of Supabase publish** — `publisher.js` saves `drafts/<hash>.json` instead of inserting to `blog_posts` table. User-approved in Plan 04-02.
- **`writer_status='draft'`** (not `'published'`) — reflects written-but-not-live state. User-approved.
- **Telegram bot sends confirmation with `draft_path`** (not live URL) — now fully implemented in 04-04.

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Writer produces dual LLM outputs (Mokslius + OldBoy) in Lithuanian | VERIFIED | `news-writer.js` line 178: `Promise.all([generateMokslius, generateOldBoy, generateTags])` |
| 2 | Auto-tags array of 3-5 Lithuanian lowercase strings is returned | VERIFIED | `generateTags()` in `news-writer.js`; `tags.slice(0, 5)` at line 190 |
| 3 | Category derived from source_id/item_type mapping (item_type override first) | VERIFIED | `detectCategory()` lines 67-72; `ITEM_TYPE_OVERRIDES` checked before `SOURCE_CATEGORY_MAP` |
| 4 | Adaptive token logic: short content uses shortPostMaxTokens, full uses fullPostMaxTokens | VERIFIED | `news-writer.js` lines 168-176: `wordCount < shortThreshold ? shortMaxTokens : fullMaxTokens` |
| 5 | writer_status column exists in seen_urls; setWriterStatus() exported | VERIFIED | `db.js` line 34: `addIfMissing('writer_status', 'TEXT')` + lines 62-64: `export function setWriterStatus` |
| 6 | POST /api/news/accept/:hash full pipeline wired; idempotency guard present | VERIFIED | `news.js` lines 40-46: 409 guard on `draft`/`published`; pipeline flows through generateNewsPost(item, cfg) → publishPost |
| 7 | LLM model configurable via config.json writer.model without code changes | VERIFIED | `news.js` line 16: `const cfg = require('../services/news-collector/config.json');` + line 54: `generateNewsPost(item, cfg)` — config.json writer.model now flows through at call time |
| 8 | Admin receives Telegram confirmation with draft_path after successful accept | VERIFIED | `handlers.js` lines 38-45: `const data = await res.json()` parsed; `ctx.editMessageText` replaces spinner with title + path on success, error message on failure |

**Score:** 8/8 truths verified

---

## Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `agent-network/server/services/news-collector/writer/news-writer.js` | `generateNewsPost(item, cfg)` + `detectCategory()` exports | VERIFIED | 193 lines. Exports both functions. OpenRouter wired via `baseURL: 'https://openrouter.ai/api/v1'`. |
| `agent-network/server/services/news-collector/writer/publisher.js` | `publishPost(urlHash, post)` draft-to-disk | VERIFIED | 42 lines. Exports `publishPost`. Saves JSON to `drafts/<hash>.json`. No stubs or TODOs. |
| `agent-network/server/routes/news.js` | POST /api/news/accept/:hash — config wired, no 501 stub | VERIFIED | 81 lines. `cfg` loaded via `createRequire` on line 16. `generateNewsPost(item, cfg)` on line 54. No empty config object. |
| `agent-network/server/services/news-collector/storage/db.js` | writer_status column + setWriterStatus() | VERIFIED | `addIfMissing('writer_status', 'TEXT')` at line 34; `setWriterStatus` exported at line 62. |
| `agent-network/server/services/news-collector/config.json` | writer block with model key | VERIFIED | `"writer": { "model": "google/gemini-2.0-flash-001", ... }` present. Now actually read at runtime. |
| `agent-network/server/services/news-collector/telegram/handlers.js` | Response parsed; ctx.editMessageText sends confirmation | VERIFIED | Lines 38, 42, 48: `res.json()` awaited; success path sends title + path; error paths send error text; `handleAccept` returns `{ ok, data }`. |

---

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `news-writer.js` | OpenRouter API | `new OpenAI({ baseURL: 'https://openrouter.ai/api/v1' })` | WIRED | Line 172 in news-writer.js |
| `news.js` | `config.json` writer.model | `const cfg = require('../services/news-collector/config.json')` + `generateNewsPost(item, cfg)` | WIRED | Line 16 loads config, line 54 passes it — writer.model now flows end-to-end |
| `news.js` route | `news-writer.js` | `import { generateNewsPost }` | WIRED | Line 12 of news.js |
| `news.js` route | `publisher.js` | `import { publishPost }` | WIRED | Line 13 of news.js |
| `news.js` route | `db.js setWriterStatus` | `setWriterStatus(db, hash, 'writing'/'draft'/'failed')` | WIRED | Lines 50, 60, 74 of news.js |
| `publisher.js` | drafts directory | `fs.writeFileSync(path.join(DRAFTS_DIR, hash + '.json'))` | WIRED | Lines 37-38 of publisher.js |
| Telegram `handleAccept()` | POST /api/news/accept/:hash | `fetch(http://localhost:${port}/api/news/accept/${urlHash})` | WIRED | handlers.js line 37 / 81 |
| Telegram `handleAccept()` response | Admin confirmation message | `const data = await res.json()` + `ctx.editMessageText(...)` | WIRED | handlers.js line 38: response parsed; lines 42-44: editMessageText with draft_path + title; line 83: handleAccept returns `{ ok, data }` |

---

## Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| WRIT-01 | 04-01 | LLM (OpenRouter) generates full blog post (Mokslius + OldBoy) | SATISFIED | `generateNewsPost()` in news-writer.js produces both bodies via OpenRouter |
| WRIT-02 | 04-01 | Auto-tags generated (3-5 lowercase Lithuanian strings) | SATISFIED | `generateTags()` + `tags.slice(0,5)` in news-writer.js |
| WRIT-03 | 04-01 | Category auto-selected from source_id/item_type | SATISFIED | `detectCategory()` with full 10-source map + item_type overrides |
| WRIT-04 | 04-01 | Model configurable via config (default: google/gemini-2.0-flash-001) | SATISFIED | config.json loaded via createRequire in news.js; cfg passed to generateNewsPost — changing writer.model in config.json changes the LLM model without code edits |
| WRIT-05 | 04-01 | Adaptive prompt logic for short content | SATISFIED | Lines 168-176 of news-writer.js: `wordCount < shortPostWordThreshold` → shortMaxTokens |
| PUBL-01 | 04-02 | Accepted post automatically processed (draft pipeline) | SATISFIED | POST /api/news/accept/:hash triggers full pipeline; draft JSON saved to disk |
| PUBL-02 | 04-02 | Author: OldBoy-RSS (per user-approved draft override: stored in draft JSON) | SATISFIED | publisher.js includes all OldBoy content in draft JSON; actual Supabase insert deferred per user override |
| PUBL-03 | 04-02 | Pipeline internal to server process (not external script) | SATISFIED | news.js and publisher.js are server-side modules; no external scripts |

All 8 requirements SATISFIED.

---

## Anti-Patterns Found

No blockers or warnings remain. Previously noted stale comments removed in 04-04:

| File | Issue | Resolution |
|------|-------|------------|
| `telegram/handlers.js` | Stale "Phase 4 stub" and "Phase 4 not yet implemented" comments | Removed in 04-04 — replaced with accurate comment "Trigger writer pipeline and send confirmation to admin" |
| `server/routes/news.js` | `createRequire` declared but unused warning | Resolved in 04-04 — `require` now used to load config.json on line 16 |
| `server/routes/news.js` | `generateNewsPost(item, {})` blocker | Fixed in 04-04 — now `generateNewsPost(item, cfg)` |

---

## Human Verification Required

### 1. Telegram Confirmation to Admin (End-to-End)

**Test:** Run the server, ensure a real DB item exists in `seen_urls` with `tg_status='pending'`, press Accept in the Telegram bot, observe what the admin sees in Telegram after the spinning indicator disappears.
**Expected:** The "Generuojama..." spinner message is replaced in-place (via `editMessageText`) with: "Draft saved: [Title] Path: drafts/[hash].json". If the pipeline fails, admin sees "Klaida: [error message]" instead of an indefinite spinner.
**Why human:** Requires live bot token, active Telegram session, real DB row, and actual button press. Cannot verify Telegram message delivery programmatically.

### 2. Draft JSON Content Quality

**Test:** Inspect `agent-network/server/services/news-collector/drafts/<hash>.json` after a successful accept call.
**Expected:** `oldboy` field contains coherent Lithuanian narrative text (not empty, not garbled). `tags` is an array of 3-5 lowercase Lithuanian strings. `category` is one of the valid values. `mokslius` field contains a technical-style write-up.
**Why human:** LLM output quality cannot be verified statically; requires actual OpenRouter API call and human review.

---

## Gaps Summary

No gaps remain. Both gaps identified in the initial verification (04-VERIFICATION.md, status: gaps_found) were closed by plan 04-04:

**Gap 1 — WRIT-04 (closed):** `news.js` now loads `config.json` via `createRequire` and passes `cfg` to `generateNewsPost`. Changing `writer.model` in config.json will change the LLM model without any code edits.

**Gap 2 — Telegram confirmation (closed):** `handlers.js` now parses the accept response with `await res.json()` and calls `ctx.editMessageText` with the draft title and path on success, error message on failure. The `handleAccept` export returns `{ ok, data }` for unit testability.

No regressions detected. Previously verified artifacts (news-writer.js 193 lines, publisher.js 42 lines, db.js writer_status migration, config.json writer block) all remain intact.

---

_Verified: 2026-03-19_
_Verifier: Claude (gsd-verifier)_
_Re-verification after: 04-04 gap closure_
