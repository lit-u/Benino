---
phase: 04-writer-publisher
plan: "02"
subsystem: api
tags: [publisher, draft-system, news-route, writer-pipeline, sqlite]

# Dependency graph
requires:
  - phase: 04-01
    provides: generateNewsPost(item, cfg), setWriterStatus(db, hash, status), writer_status column

provides:
  - publishPost(urlHash, post) in publisher.js — saves draft JSON to news-collector/drafts/<hash>.json
  - POST /api/news/accept/:hash — full pipeline replacing 501 stub
  - writer_status lifecycle: null → writing → draft | failed

affects:
  - Telegram bot handleAccept() — now receives { success, draft_path, title, tags, category } from accept route
  - Future publish step — reads drafts/<hash>.json and posts to Supabase blog_posts

# Tech tracking
tech-stack:
  added: []  # No new dependencies — uses built-in fs module only
  patterns:
    - "Draft-to-disk pattern: save JSON file instead of Supabase insert (user-gated publish)"
    - "Idempotency guard on writer_status: draft/published → 409 Conflict"
    - "db.close() in finally block — established pattern from Phase 01/02"
    - "writer_status state machine: null → writing → draft | failed"

key-files:
  created:
    - agent-network/server/services/news-collector/writer/publisher.js
  modified:
    - agent-network/server/routes/news.js
    - agent-network/.gitignore

key-decisions:
  - "USER OVERRIDE: Draft-to-disk instead of Supabase publish — user reviews drafts/<hash>.json manually before publishing"
  - "writer_status='draft' (not 'published') — clean semantic distinction between written and live"
  - "publishPost export name (not publishNewsPost) — matches implementation override spec"
  - "No Supabase client import in news.js — not needed for draft-only flow"
  - "drafts/ dir gitignored — generated content should not be committed"

# Metrics
duration: 3min
completed: 2026-03-18
---

# Phase 4 Plan 02: Publisher Module Summary

**Draft-to-disk publisher saving generated posts as JSON files to news-collector/drafts/ for manual review, replacing the 501 stub in POST /api/news/accept/:hash with the full writer pipeline**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-18T17:25:15Z
- **Completed:** 2026-03-18T17:27:38Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- `publisher.js` created with `publishPost(urlHash, post)` — saves draft JSON to `news-collector/drafts/<hash>.json`
- `news.js` 501 stub fully replaced with complete pipeline: load item → set writing → generateNewsPost → publishPost → set draft
- Idempotency guard: returns 409 if `writer_status` is already `draft` or `published`
- writer_status state machine: `null → writing → draft | failed`
- `db.close()` in `finally` block — no SQLite connection leak
- `drafts/` directory added to `.gitignore` — generated content not committed
- No new npm dependencies (uses built-in `fs` module only)

## Task Commits

Each task was committed atomically:

1. **Task 1: publisher.js — draft-to-disk writer output** - `fbc1fd5` (feat)
2. **Task 2: news.js — replace 501 stub with full writer pipeline** - `25f4289` (feat)

## Files Created/Modified

- `server/services/news-collector/writer/publisher.js` — saves draft JSON; exports `publishPost(urlHash, post)`
- `server/routes/news.js` — full pipeline replacing 501 stub; transitions writer_status through writing→draft
- `.gitignore` — added `server/services/news-collector/drafts/` entry

## Decisions Made

- **USER OVERRIDE applied:** Draft-to-disk instead of Supabase publish. `writer_status='draft'` not `'published'`. Admin reviews `drafts/<hash>.json` manually before publishing.
- `publishPost` export name matches override spec (not `publishNewsPost` from original plan)
- No Supabase client needed in `news.js` — clean separation for the draft-only flow
- `drafts/` dir is created lazily via `fs.mkdirSync(..., { recursive: true })` — no manual setup needed
- Accept route returns `{ success, draft_path, title, tags, category }` — Telegram bot gets confirmation + file path

## Deviations from Plan

### User-Directed Override

**[User Override] Draft-to-disk instead of Supabase publish**
- **Decision source:** User instruction in execution prompt
- **Original plan:** `publisher.js` inserts into `blog_posts` table via Supabase service key; `writer_status='published'`
- **Actual implementation:** `publisher.js` saves `drafts/<hash>.json`; `writer_status='draft'`
- **Rationale:** User wants to review generated content before publishing live
- **Impact:** Telegram bot receives `draft_path` instead of `url`; publish step deferred to future manual action
- **Files affected:** `publisher.js` (no Supabase), `news.js` (no Supabase client)

## Issues Encountered

- Shell `!` character caused bash syntax error in inline `node -e` verification. Fixed by using temporary `.mjs` script files (same pattern as Phase 04-01).

## User Setup Required

- `drafts/` directory is created automatically on first `publishPost()` call — no manual setup needed.
- To publish a draft manually: read `server/services/news-collector/drafts/<hash>.json` and insert into Supabase `blog_posts` table.

## Next Phase Readiness

- Phase 4 is now functionally complete for the draft flow
- When user is ready to publish: a future `POST /api/news/publish/:hash` route can read the draft JSON and insert into Supabase `blog_posts`
- `detectCategory` is still exported from `news-writer.js` for reuse if a future publisher needs it

## Self-Check: PASSED

- FOUND: server/services/news-collector/writer/publisher.js
- FOUND: server/routes/news.js (no 501 stub — grep returns 0)
- FOUND: .gitignore (drafts/ entry added)
- COMMIT fbc1fd5: feat(04-02): publisher.js — draft-to-disk writer output
- COMMIT 25f4289: feat(04-02): news.js — replace 501 stub with full writer pipeline

---
*Phase: 04-writer-publisher*
*Completed: 2026-03-18*
