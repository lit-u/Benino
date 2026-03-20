# Phase 7: Multi-Hotel — Research

**Researched:** 2026-03-20
**Domain:** Vanilla JS SPA + Node.js/Express self-service CRUD, Supabase ownership isolation
**Confidence:** HIGH (all findings from direct codebase inspection)

## Summary

Phase 7 adds a self-service portal so any L2-or-higher authenticated user can create and manage their own hotel. The critical insight from reading the existing code is that **the backend already supports multiple hotels and owner isolation** — `POST /api/hotels` creates a hotel under the requester's `owner_id`, and `verifyOwner()` already gates all mutations by comparing `hotel.owner_id` to the session's `userId`. What is completely missing is the **frontend surface** that lets a user:

1. Create a new hotel (form)
2. See the list of hotels they own (dashboard)
3. Navigate from that list to the already-existing `/hotel/:slug/admin` panel

The auth question is already resolved: `requireUser` rejects `anon` role, and both the new `sessionCore` system (`req.auth.role === 'user'|'admin'`) and the legacy `authContext.level >= 2` path are accepted. An anon/L1 user who tries `POST /api/hotels` gets a 401 today — no new backend guard is needed.

The only meaningful design decision is whether to allow one or multiple hotels per L2 user. Nothing in the DB or backend prevents multiple hotels per owner today. A soft limit (e.g., 3 per user) can be enforced in the `POST /api/hotels` route with a count query — no DB migration required. No new DB columns are needed for Phase 7.

**Primary recommendation:** Build two pages — `/my-hotels` (list + create) and `/create-hotel` is unnecessary as a separate page — the create form can be a modal or inline section on `/my-hotels`. Reuse the existing `/hotel/:slug/admin` for management. Add one API endpoint `GET /api/hotels/mine` that filters hotels by `owner_id`.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Vanilla JS ES6 modules | — | Frontend SPA | Project-standard; all other pages use this |
| Express.js | existing | Route handler for `GET /api/hotels/mine` | Already in project |
| Supabase JS client | existing | DB query with service key | Already in all routes |
| sessionCore + requireUser | existing | Auth gate | Already used by all hotel routes |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| generateSlug + ensureUniqueSlug | existing | Hotel slug generation | Called on hotel name input |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `/my-hotels` SPA page | Inline section in `/dashboard.html` | Dashboard exists but is unrelated; separate page is cleaner |
| Soft limit in route | DB constraint / unique index | DB constraint is too rigid; soft limit allows admin override |

**No new package installation needed.**

## Architecture Patterns

### Recommended Project Structure

New files for Phase 7:
```
public/
├── my-hotels.html                  # Self-service landing: list + create form
└── modules/
    └── my-hotels-module.js         # List owned hotels, create hotel inline form

server/routes/hotels.js             # Add GET /mine endpoint (owner filter)
server/index.js                     # Serve /my-hotels route (SPA fallback already handles it)
```

### Pattern 1: Owner-Filtered Hotel List Endpoint

**What:** `GET /api/hotels/mine` returns only hotels owned by the authenticated user.
**When to use:** Called on page load of `/my-hotels`.

Important: this route must be placed **before** `GET /:slug` in the router, otherwise Express matches `mine` as a slug value.

```javascript
// Source: direct codebase reading of hotels.js
// Place BEFORE router.get('/:slug', ...)
router.get('/mine', requireUser, async (req, res) => {
  const owner_id = req.authContext?.userId || req.auth?.identityId;
  if (!owner_id) return res.status(401).json({ success: false, error: 'Negalima nustatyti vartotojo tapatybės' });

  const { data, error } = await supabase
    .from('hotels')
    .select('id, slug, name, city, created_at, owner_email')
    .eq('owner_id', owner_id)
    .order('created_at', { ascending: false });

  if (error) return res.status(500).json({ success: false, error: error.message });
  return res.json({ success: true, hotels: data || [] });
});
```

### Pattern 2: Soft Hotel Limit Check in POST /api/hotels

**What:** Before inserting a new hotel, count existing hotels for this owner_id. Reject if >= limit (3).
**When to use:** Inside the existing `POST /api/hotels` handler, after owner_id is resolved.

```javascript
// Source: direct codebase reading — same pattern as "max 10 rooms per hotel" check
const HOTEL_LIMIT_PER_USER = 3;
const { count } = await supabase
  .from('hotels')
  .select('id', { count: 'exact', head: true })
  .eq('owner_id', owner_id);

if ((count || 0) >= HOTEL_LIMIT_PER_USER) {
  return res.status(400).json({ success: false, error: `Maksimalus viešbučių skaičius: ${HOTEL_LIMIT_PER_USER}` });
}
```

### Pattern 3: My Hotels Frontend Module

**What:** Vanilla JS module that: (a) checks auth, (b) loads `/api/hotels/mine`, (c) renders hotel cards, (d) shows inline create form, (e) redirects to `/hotel/:slug/admin` on success.
**When to use:** Loaded by `my-hotels.html`.

Auth check uses same pattern as `hotel-admin-module.js`:
```javascript
// Source: hotel-admin-module.js lines 27-31
sessionId = localStorage.getItem('agent_session_id') || '';
if (!sessionId) {
  showAuthGate('Prisijunkite, kad galėtumėte valdyti savo viešbučius.');
  return;
}
```

After `POST /api/hotels` returns `{ success: true, slug }`, redirect to `/hotel/${slug}/admin`.

### Pattern 4: apiFetch with X-Session-ID Header

**What:** All protected API calls include session ID as header.
**When to use:** Every API call in `my-hotels-module.js`.

This is the established project pattern — `hotel-admin-module.js` uses `apiFetch()` which adds the `X-Session-ID` header from `localStorage.getItem('agent_session_id')`. Copy the same helper.

### Pattern 5: HTML Page Registration in server/index.js

**What:** New `.html` pages are served as static files. The existing static middleware handles this automatically — no route registration needed for `/my-hotels` (it falls through to SPA `index.html` if not found, but `my-hotels.html` in `public/` will be served directly).

**Confirmed pattern:** All existing pages like `hotel-admin.html`, `brain.html`, `dashboard.html` are served without explicit routes in `server/index.js`.

### Anti-Patterns to Avoid

- **Don't add `requireUser` to `GET /api/hotels/mine` at the Express route level via middleware AND inside the handler:** pick one place. Use `requireUser` middleware on the route, then read `owner_id` from `req.auth` inside.
- **Don't place `GET /mine` after `GET /:slug`:** Express greedy matching will treat `mine` as a slug value and look for a hotel named "mine" in the DB.
- **Don't redirect to `/hotel/:slug` (public page) after creation:** redirect to `/hotel/:slug/admin` so the user can immediately add rooms.
- **Don't use `owner_id` as a display field in the UI.** It is an internal identity ID (UUID-like TEXT), not a human-readable name.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Slug generation | Custom transliterator | `generateSlug` + `ensureUniqueSlug` in `server/utils/slug-generator.js` | Already handles Lithuanian chars, collision counter |
| Auth check | Custom session lookup | `requireUser` middleware + `req.auth` / `req.authContext` | Dual-system (sessionCore + legacy) already handled |
| Owner isolation | Re-implement ownership check | `verifyOwner()` in `hotels.js` | Already used by all mutation routes |
| Image upload on creation | File upload in create form | Skip for creation; images added in `/admin` panel after creation | Hotel admin panel already has drag-drop upload |

**Key insight:** The entire hotel management backend already exists. Phase 7 is almost entirely a frontend task — one new API endpoint (`GET /mine`) and two new frontend files.

## Common Pitfalls

### Pitfall 1: Express Route Order — `/mine` vs `/:slug`

**What goes wrong:** If `GET /mine` is registered after `GET /:slug`, Express matches `mine` as the slug parameter and queries `SELECT ... WHERE slug = 'mine'` — returns 404 in most cases but could match a real hotel named "mine".
**Why it happens:** Express routes match in registration order.
**How to avoid:** Place `router.get('/mine', ...)` before `router.get('/:slug', ...)` in `hotels.js`.
**Warning signs:** API returns `{ success: false, error: 'Hotel not found' }` instead of a list.

### Pitfall 2: owner_id Source Inconsistency

**What goes wrong:** The `POST /api/hotels` handler reads `owner_id` from `req.authContext?.userId || req.auth?.identityId`. The `authContext.userId` key does not actually exist in the legacy middleware — legacy sets `authContext.sessionId`, not `authContext.userId`. So for legacy L2 sessions, `owner_id` comes from `req.auth?.identityId` (sessionCore path).
**Why it happens:** Dual auth migration not yet complete; `verifyOwner()` reads the same combination.
**How to avoid:** Use the exact same expression already in `POST /api/hotels`: `req.authContext?.userId || req.auth?.identityId`. For `GET /mine`, use the same expression.
**Warning signs:** Hotels created but `owner_id = null`, so `verifyOwner()` always returns `forbidden`.

### Pitfall 3: Auth Gate Shows but Session Actually Exists

**What goes wrong:** `my-hotels-module.js` checks `localStorage.getItem('agent_session_id')` client-side. If the cookie (`sid_core`) is set but `agent_session_id` is not in localStorage (possible after browser cache clear), the user sees "please log in" even though they have a valid session.
**Why it happens:** The project uses both cookie-based sessionCore and localStorage session ID. The hotel admin module uses localStorage. If localStorage was cleared but the cookie persists, the page appears broken.
**How to avoid:** Same pattern as hotel-admin-module — show auth gate with a link to login, same as existing behavior.
**Warning signs:** Reported as "I can't access my hotels" after clearing browser data.

### Pitfall 4: Slug Changes on Hotel Rename

**What goes wrong:** `PUT /:slug` already regenerates the slug when `name` changes. If a user creates a hotel, navigates to `/my-hotels`, and then renames it from the admin panel, the slug changes. Any bookmarked `/hotel/old-slug/admin` URL breaks.
**Why it happens:** Slug is derived from name; rename = new slug.
**How to avoid:** Phase 7 does not need to address this — it is a pre-existing behavior. Document in UI that slug changes on rename (out of scope for Phase 7).

### Pitfall 5: "One Hotel Per User" vs "Many" — No DB Enforcement

**What goes wrong:** If the soft limit is only in `POST /api/hotels` route code, an admin using `admin-helpers.js` to directly insert into Supabase bypasses the limit.
**Why it happens:** No DB-level constraint.
**How to avoid:** This is intentional and acceptable — admin should be able to create hotels for users manually. Document in code comment that the 3-hotel limit is a UI/API convention, not a DB constraint.

## Code Examples

Verified patterns from direct codebase inspection:

### How verifyOwner works (existing, unchanged for Phase 7)
```javascript
// Source: server/routes/hotels.js lines 48-61
async function verifyOwner(req, slug) {
  const { data: hotel } = await supabase
    .from('hotels')
    .select('id, owner_id')
    .eq('slug', slug)
    .single();

  if (!hotel) return { error: 'not_found', hotel: null };

  const userId = req.authContext?.userId || req.auth?.identityId;
  if (hotel.owner_id !== userId) return { error: 'forbidden', hotel };

  return { error: null, hotel };
}
```

### How POST /api/hotels already assigns owner_id
```javascript
// Source: server/routes/hotels.js lines 238-245
const owner_id = req.authContext?.userId || req.auth?.identityId;
if (!owner_id) {
  return res.status(401).json({ success: false, error: 'Negalima nustatyti vartotojo tapatybės' });
}
// ... insert with owner_id
```

### Frontend redirect after hotel creation (pattern to use)
```javascript
// After successful POST /api/hotels
const { hotel, slug } = await response.json(); // response has { success, hotel, slug }
window.location.href = `/hotel/${slug}/admin`;
```

### Hotel card template for my-hotels list (modeled on existing patterns)
```javascript
// Modeled on hotel-admin-module.js room list pattern
function renderHotelCard(hotel) {
  return `
    <div class="hotel-card">
      <div class="hotel-card-name">${hotel.name}</div>
      <div class="hotel-card-city">${hotel.city || 'Palanga'}</div>
      <a href="/hotel/${hotel.slug}/admin" class="btn-manage">Valdyti</a>
      <a href="/hotel/${hotel.slug}" target="_blank" class="btn-view">Peržiūrėti</a>
    </div>
  `;
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single hardcoded hotel (manual DB insert) | Multi-hotel with owner_id isolation | Phase 5 (backend ready) | Phase 7 only needs frontend |
| L1/L2/L3 numeric levels | anon/user/admin roles (sessionCore) + legacy L2 fallback | Phase 5 migration ongoing | `requireUser` accepts both paths |

**Deprecated/outdated:**
- Manual hotel creation via Supabase dashboard or admin-helpers.js: replaced by self-service create form in Phase 7 (but still valid for admin use).

## Open Questions

1. **One hotel or multiple hotels per L2 user?**
   - What we know: Backend has no limit; room limit is 10 per hotel; existing pattern uses soft limit for rooms.
   - What's unclear: Product decision — is 1 hotel per user simpler UX?
   - Recommendation: Allow multiple (up to 3 soft limit) — it costs nothing extra and is more useful. Single-hotel restriction would require extra enforcement logic.

2. **Where does the "create hotel" UI live?**
   - What we know: No `/create-hotel` page exists. `/my-hotels` does not exist yet.
   - What's unclear: Modal vs inline section vs separate page.
   - Recommendation: Inline section at bottom of `/my-hotels` page — one page, no navigation overhead. If user has 0 hotels, show create form prominently. If they have hotels, show list + "Add another" button that reveals the form.

3. **How does a new user find `/my-hotels`?**
   - What we know: Navigation is in `index.html` / the main SPA shell; no nav audit done.
   - What's unclear: Whether `/my-hotels` needs to be linked from the main nav or profile area.
   - Recommendation: Out of scope for Phase 7 execution — add a link from the main nav or user profile page. The planner can include this as a task (add nav link) in the wave that builds `my-hotels.html`.

## Validation Architecture

> `workflow.nyquist_validation` key is absent from `.planning/config.json` — treat as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Playwright (existing) |
| Config file | `agent-network/playwright.config.cjs` |
| Quick run command | `npx playwright test tests/my-hotels.spec.js` |
| Full suite command | `npx playwright test` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| MH-01 | `GET /api/hotels/mine` returns only caller's hotels | API (request) | `npx playwright test tests/my-hotels.spec.js::mine-api` | Wave 0 |
| MH-02 | `POST /api/hotels` by anon returns 401 | API (request) | `npx playwright test tests/my-hotels.spec.js::create-anon-blocked` | Wave 0 |
| MH-03 | `POST /api/hotels` by L2 user creates hotel + returns slug | API (request) | `npx playwright test tests/my-hotels.spec.js::create-success` | Wave 0 |
| MH-04 | `/my-hotels` page loads and shows auth gate for unauthenticated | E2E (page) | `npx playwright test tests/my-hotels.spec.js::page-auth-gate` | Wave 0 |
| MH-05 | After create, browser redirects to `/hotel/:slug/admin` | E2E (page) | manual-only (needs real L2 session) | Wave 0 stub |
| MH-06 | Soft limit: 4th hotel creation returns 400 | API (request) | manual-only (needs 3 existing hotels) | Wave 0 stub |

### Sampling Rate
- **Per task commit:** `npx playwright test tests/my-hotels.spec.js`
- **Per wave merge:** `npx playwright test`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `agent-network/tests/my-hotels.spec.js` — covers MH-01 through MH-06 as `test.skip()` stubs
- [ ] No new framework or config needed — Playwright already configured

## Sources

### Primary (HIGH confidence)
- `agent-network/server/routes/hotels.js` — full route inspection: owner_id assignment, verifyOwner(), slug generation calls, room limit pattern
- `agent-network/server/middleware/requireRole.js` — requireUser implementation, legacy L2 support
- `agent-network/server/middleware/sessionCore.js` — auth data shape: `req.auth.role`, `req.auth.identityId`
- `agent-network/public/modules/hotel-admin-module.js` — frontend auth pattern, apiFetch pattern, session key name
- `agent-network/server/utils/slug-generator.js` — generateSlug + ensureUniqueSlug already support Lithuanian

### Secondary (MEDIUM confidence)
- `.planning/STATE.md` — confirmed owner_id is TEXT (not UUID FK), dual-auth migration ongoing
- `agent-network/tests/hotel.spec.js` — Wave 0 stub pattern for new test file

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all from direct code reading, no external dependencies needed
- Architecture: HIGH — GET /mine endpoint pattern is direct extension of existing GET / endpoint
- Pitfalls: HIGH — Express route order and owner_id source issues verified from actual code

**Research date:** 2026-03-20
**Valid until:** 2026-04-20 (stable stack, no external dependencies)
