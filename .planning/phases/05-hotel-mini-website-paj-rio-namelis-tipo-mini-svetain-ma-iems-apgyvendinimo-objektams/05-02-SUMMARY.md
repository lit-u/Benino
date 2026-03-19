---
phase: 05-hotel-mini-website
plan: 02
subsystem: agent-network/hotel-page
tags: [ssr, json-ld, schema.org, vanilla-js, hotel, sea-proximity, availability, reservation]
requires: [05-01]
provides: [hotel-public-page, hotel-admin-route, lodging-schema]
affects: [server/index.js, public/hotel.html, public/modules/hotel-module.js]
tech-stack:
  added: []
  patterns: [SSR-meta-injection, JSON-LD-LodgingBusiness, availability-traffic-light, wa.me-deep-link]
key-files:
  created:
    - agent-network/public/hotel.html
    - agent-network/public/modules/hotel-module.js
  modified:
    - agent-network/server/index.js
decisions:
  - injectMeta extended with optional ogImage parameter (backward-compatible — all existing callers omit it)
  - hotel.phone used as mailto recipient (no separate email column in schema)
  - buildLodgingSchema builds JS object first then JSON.stringify — avoids manual quote escaping
  - requireUser imported at module top-level (not inline) — required for ES module semantics
metrics:
  duration: 11min
  tasks_completed: 2
  files_modified: 3
  completed_date: 2026-03-19
---

# Phase 5 Plan 02: Hotel Public Page + SSR Meta Summary

**One-liner:** SSR /hotel/:slug with LodgingBusiness JSON-LD + og:image from room photo, Vanilla JS hotel page with availability traffic lights, sea-proximity info blocks, and WhatsApp/email reservation form using hotel.phone as contact.

---

## What Was Built

### Task 1: Extend injectMeta + SSR routes in server/index.js
- Extended `injectMeta()` to accept optional `ogImage` parameter (line 701). All existing callers unchanged — they get the default `palanga-hero.jpg`. Hotel SSR route passes the first room's `window_view` photo URL.
- Added `buildLodgingSchema(hotel)` function (line 725) — builds Schema.org `LodgingBusiness` object with nested `HotelRoom` entries. Each room includes `amenityFeature` array with `LocationFeatureSpecification` for sea distance (in walking minutes), compass orientation, and noise level (Lithuanian labels).
- Added `/hotel/:slug/admin` route (line 893) with `requireUser` middleware — returns 401 for unauthenticated users (satisfies HOTEL-04).
- Added `/hotel/:slug` SSR route (line 898) — queries `supabaseSeo` for hotel + rooms + photos, finds first `window_view` photo for og:image, injects `LodgingBusiness` JSON-LD via `extraSchema` parameter.
- Route ordering: admin → SSR → SPA fallback (critical for Express matching).
- `requireUser` imported at line 101 (module top-level, not inline).

### Task 2: hotel.html + hotel-module.js
- `public/hotel.html`: Standalone dark-theme page (not index.html SPA). 800px max-width centered. Responsive room grid (1-col < 480px, 2-col 480–768px, 3-col 768px+). All UI-SPEC colors: `#1a1a1a` bg, `#252525` cards, `#FFC700` accent, `#22c55e`/`#eab308`/`#ef4444` traffic lights, `#25D366` WhatsApp. Semantic elements: `<header>`, `<main>`, `<article>` per room, `<address>`.
- `public/modules/hotel-module.js`: ES6 module. Key functions:
  - `getAvailabilityDisplay(room)` — green/yellow (14-day)/red logic using `toLocaleDateString('lt-LT')`
  - `buildWhatsAppLink()` — returns `https://wa.me/{number}?text={encoded}`
  - `buildReservationMessage()` — Lithuanian-language reservation message
  - `buildMailtoLink()` — uses `hotel.phone` as recipient (note: no separate email column)
  - All 8 compass directions with Lithuanian names (Šiaurė, Pietūs, etc.)
  - Noise levels: Ramus/Vidutinis/Gyvas
  - Sea distance: `Math.ceil(meters / 80)` minutes
  - Gallery strip with thumbnail click to swap main photo + window-view badge toggle
  - Inline reservation form (slide open on Rezervuoti click, no modal)
  - URL hash scroll: if `#room-N` in URL, scrolls to room card after render

---

## Decisions Made

1. **`injectMeta` backward-compatible extension** — added `ogImage = null` as optional param with `||` fallback to hero image. No existing callers break.
2. **`hotel.phone` as mailto recipient** — the `hotels` table has no `email` column; `phone` field doubles as contact. Documented in code comments.
3. **`buildLodgingSchema` uses `JSON.stringify()`** — avoids the manual `.replace(/"/g, '\\"')` pattern used in blog SSR. Cleaner and correct per Pitfall 4 in RESEARCH.md.
4. **`requireUser` imported at module top-level** — ES module `import` declarations must be at the static head of the file. Moving inline `import` to line 101 prevents runtime SyntaxError.

---

## Deviations from Plan

None — plan executed exactly as written.

---

## Verification Results

All verification checks passed:
- `grep "LodgingBusiness" server/index.js` — 3 matches (function, return type, route)
- `grep "ogImage" server/index.js` — parameter in signature + usage in hotel route
- `grep "requireUser" server/index.js | grep hotel` — import line + admin route
- `grep "supabaseSeo" server/index.js` — client defined at line 686, used in hotel SSR route
- `grep "wa.me" public/modules/hotel-module.js` — `https://wa.me/` format confirmed
- `grep "hotel.phone" public/modules/hotel-module.js` — used as mailto recipient
- `grep "#22c55e|#eab308|#ef4444" public/hotel.html` — all 3 traffic light colors present

---

## Self-Check: PASSED

Files created/modified:
- FOUND: agent-network/server/index.js (modified)
- FOUND: agent-network/public/hotel.html (created)
- FOUND: agent-network/public/modules/hotel-module.js (created)

Commits:
- bb40135 — feat(05-02): extend injectMeta with ogImage + hotel SSR routes + admin auth gate
- f06e963 — feat(05-02): create hotel.html and hotel-module.js public page
