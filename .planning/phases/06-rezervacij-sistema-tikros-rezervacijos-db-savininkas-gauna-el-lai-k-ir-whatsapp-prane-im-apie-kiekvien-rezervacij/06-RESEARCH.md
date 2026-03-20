# Phase 6: Rezervacijų Sistema - Research

**Researched:** 2026-03-20
**Domain:** Supabase DB insert (anonymous), Resend email notification, Express route extension, Vanilla JS form → API POST, admin panel UI extension
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Rezervacijos duomenų modelis (Supabase)**
- Nauja lentelė: `hotel_reservations`
- Laukai: `id` (uuid), `hotel_id` (FK → hotels), `room_id` (FK → hotel_rooms), `guest_name` (text, required), `guest_email` (text, optional), `guest_phone` (text, optional), `arrival_date` (date), `departure_date` (date), `nights` (int, skaičiuojamas), `total_price` (numeric), `message` (text, optional), `status` (enum: pending/confirmed/cancelled, default: pending), `created_at` (timestamptz)
- RLS: savininkas mato tik savo viešbučio rezervacijas; svečias gali tik INSERT (be auth)

**Forma ir pateikimas (frontend)**
- Esama `createReservationForm()` papildoma: vietoj WhatsApp/mailto, forma POST'a į `/api/hotels/:slug/reservations`
- Reikalingi laukai: vardas, atvykimas, išvykimas — kiti neprivalomi
- WhatsApp/email nuorodos lieka kaip antriniai CTA po forma
- Po sėkmingo POST: forma paslepiama, rodomas sėkmės pranešimas
- Klaidos atveju: rodomas klaidos pranešimas, WhatsApp link kaip fallback

**Savininko notifikacija**
- Kanalas: el. laiškas per esamą `email-service.js` (Resend)
- Gavėjas: `hotels.owner_email` laukas (naujas — reikia pridėti prie hotels lentelės)
- Siuntimas asinchroniškai — klaida el. pašte neblokuoja rezervacijos sukūrimo
- WhatsApp pranešimas savininkui: NE automatinis

**Admin rezervacijų valdymas**
- Vieta: `/hotel/:slug/admin` — nauja sekcija "Rezervacijos"
- Sąrašas: kortelės su kambario pavadinimu, svečio vardu, datomis, naktų skaičiumi, suma, statusu, svečio kontaktais
- Veiksmai: "Patvirtinti" (pending → confirmed) + "Atšaukti" (pending/confirmed → cancelled)
- Filtravimas pagal statusą — Claude's discretion
- Pending rezervacijos rodomos pirma

### Claude's Discretion
- Tikslus el. laiško HTML dizainas (reuse esamo email-service.js stiliaus)
- Filtravimo UI detalės admin panelėje
- Ar rodyti rezervacijų skaičiaus badge'ą ant kambario kortelės admin puslapyje
- Svečio el. pašto siuntimo logika po patvirtinimo

### Deferred Ideas (OUT OF SCOPE)
- Automatinis priminimas svečiui prieš atvykimą (24h el. laiškas)
- Booking kalendorius su užblokuotomis datomis
- Mokėjimų integracija (Stripe/Paysera)
- SMS pranešimas savininkui (Twilio)
- Rezervacijų eksportas CSV/Excel
</user_constraints>

---

## Summary

Phase 6 extends the existing hotel mini-website (Phase 5) with a real reservation pipeline: guest submits form → DB insert → owner gets email notification → owner manages reservations in admin panel. The work is almost entirely additive — no existing endpoints are broken, no tables are dropped, only new routes/columns/UI sections are added.

The codebase is well-prepared for this phase. `email-service.js` already has `Resend` wired with a proven HTML email pattern — adding `sendReservationNotification()` is a copy-modify operation. `hotels.js` already has `verifyOwner()`, `requireUser`, and the service-role Supabase client — new reservation routes follow the identical pattern. The frontend `createReservationForm()` already collects name/dates/message; it only needs a `guest_email`/`guest_phone` field addition and a `fetch()` POST replacing the WhatsApp redirect.

**Primary recommendation:** Build in three focused plans — (1) DB schema + backend API, (2) frontend form change + success/error states, (3) admin panel "Rezervacijos" section.

---

## Standard Stack

### Core (already installed — no new dependencies needed)
| Library | Purpose | Location |
|---------|---------|----------|
| `@supabase/supabase-js` | DB insert/query, RLS | `server/routes/hotels.js` — reuse existing client |
| `resend` | Email delivery | `server/services/email-service.js` — add new method |
| `express` | Route handler | `server/routes/hotels.js` — append new routes |

### No new npm packages required
All required capabilities exist in the current stack. The `nights` column can be computed in JS before insert (no DB trigger needed for MVP).

**Installation:** none — existing packages cover everything.

---

## Architecture Patterns

### Recommended New File/Route Structure
```
server/routes/hotels.js          ← append 3 new route handlers here
server/services/email-service.js ← add sendReservationNotification() method
public/modules/hotel-module.js   ← modify createReservationForm() submit logic
public/modules/hotel-admin-module.js ← add reservations section rendering
```

No new files needed for Phase 6 core. All changes are additions to existing files.

### Pattern 1: Public POST Route (No Auth) — Anonymous Reservation Insert
**What:** Guest POSTs reservation data without a session cookie.
**When to use:** Confirmed by CONTEXT.md and the existing `/api/listings` precedent in codebase.
**Exact pattern from listings.js and hotels.js:**
```javascript
// No requireUser — public endpoint
router.post('/:slug/reservations', async (req, res) => {
  const { slug } = req.params;
  // Resolve hotel_id from slug (no owner check)
  const { data: hotel } = await supabase
    .from('hotels')
    .select('id, owner_email')
    .eq('slug', slug)
    .single();
  if (!hotel) return res.status(404).json({ success: false, error: 'Hotel not found' });

  // Insert with .select() to get the created row back
  const { data: reservation, error } = await supabase
    .from('hotel_reservations')
    .insert({ hotel_id: hotel.id, ...fields })
    .select()
    .single();

  if (error) return res.status(500).json({ success: false, error: error.message });

  // Fire-and-forget email — does NOT block the 201 response
  if (hotel.owner_email) {
    emailService.sendReservationNotification({ ...reservationData, ownerEmail: hotel.owner_email })
      .catch(err => console.error('Email send failed (non-blocking):', err));
  }

  return res.status(201).json({ success: true, reservation });
});
```

### Pattern 2: Admin GET Reservations (Protected with verifyOwner)
**What:** Owner fetches all reservations for their hotel.
**Pattern from existing hotels.js:**
```javascript
router.get('/:slug/reservations', requireUser, async (req, res) => {
  const { error: ownerError, hotel } = await verifyOwner(req, slug);
  if (ownerError === 'not_found') return res.status(404).json(...);
  if (ownerError === 'forbidden') return res.status(403).json(...);

  const { data, error } = await supabase
    .from('hotel_reservations')
    .select('*, hotel_rooms(name, number)')
    .eq('hotel_id', hotel.id)
    .order('created_at', { ascending: false });

  return res.json({ success: true, reservations: data || [] });
});
```

### Pattern 3: Status Update (PATCH — Protected)
**What:** Owner confirms or cancels a reservation.
```javascript
router.patch('/:slug/reservations/:reservationId/status', requireUser, async (req, res) => {
  const { slug, reservationId } = req.params;
  const { status } = req.body; // 'confirmed' | 'cancelled'

  const { error: ownerError, hotel } = await verifyOwner(req, slug);
  if (ownerError) return res.status(...);

  // Validate status
  const validStatuses = ['confirmed', 'cancelled'];
  if (!validStatuses.includes(status)) return res.status(400)...;

  const { data, error } = await supabase
    .from('hotel_reservations')
    .update({ status })
    .eq('id', reservationId)
    .eq('hotel_id', hotel.id)  // Safety: ensure this reservation belongs to this hotel
    .select()
    .single();

  return res.json({ success: true, reservation: data });
});
```

### Pattern 4: Email Service Method Extension
**What:** Add `sendReservationNotification()` to `EmailService` class.
**Key constraint from email-service.js:** `if (!this.resend) return { success: false }` guard must be present. Error must not be re-thrown (non-blocking caller).
```javascript
async sendReservationNotification({ ownerEmail, hotelName, roomName, guestName,
  guestEmail, guestPhone, arrivalDate, departureDate, nights, totalPrice, message }) {
  if (!this.resend) return { success: false, error: 'RESEND_API_KEY not configured' };
  try {
    const { data, error } = await this.resend.emails.send({
      from: this.from,
      to: ownerEmail,
      subject: `Nauja rezervacija — ${roomName}, ${hotelName}`,
      html: `...` // Reuse .header/.content/.footer CSS class pattern from existing emails
    });
    if (error) throw error;
    return { success: true, messageId: data.id };
  } catch (err) {
    console.error('Failed to send reservation notification:', err);
    return { success: false, error: err.message }; // Return, do NOT throw
  }
}
```

### Pattern 5: Frontend Form — POST Instead of WhatsApp Redirect
**What:** Replace WhatsApp/mailto buttons with a single "Siųsti rezervaciją" submit button.
**Key insight from hotel-module.js analysis:** The form already has `getFormData()` and `validate()` helpers. The CTA row must be restructured. WhatsApp/email become secondary links below the submit button.
```javascript
// In createReservationForm(): replace the CTA row with:
const submitBtn = document.createElement('button');
submitBtn.type = 'button';
submitBtn.className = 'btn-submit-reservation';
submitBtn.textContent = 'Siųsti rezervaciją';

submitBtn.addEventListener('click', async () => {
  const data = getFormData();
  if (!validate(data)) { /* show error */ return; }

  submitBtn.disabled = true;
  submitBtn.textContent = 'Siunčiama...';

  try {
    const nights = Math.round((new Date(data.departure) - new Date(data.arrival)) / 86400000);
    const resp = await fetch(`/api/hotels/${slug}/reservations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        room_id: room.id,
        guest_name: data.name,
        guest_email: data.email || null,
        guest_phone: data.phone || null,
        arrival_date: data.arrival,
        departure_date: data.departure,
        nights,
        total_price: nights > 0 && room.price_per_night ? nights * room.price_per_night : null,
        message: data.message || null
      })
    });
    const json = await resp.json();
    if (json.success) {
      // Hide form, show success message
      formEl.innerHTML = '<p class="reservation-success">Rezervacija priimta! Savininkas susisieks su jumis netrukus.</p>';
    } else {
      throw new Error(json.error || 'Server error');
    }
  } catch (err) {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Siųsti rezervaciją';
    // Show error + fallback WhatsApp link
    errorEl.textContent = 'Nepavyko išsiųsti. ' + (hotel.whatsapp ? 'Susisiekite per WhatsApp.' : '');
    errorEl.classList.add('visible');
  }
});
```

### Pattern 6: Admin Panel — Reservations Section
**What:** New section in hotel-admin-module.js rendered after room list, showing reservation cards.
**When to load:** On `init()`, after `renderRoomList()`. Fetch `/api/hotels/:slug/reservations` with session header (same `apiFetch()` helper pattern already in hotel-admin-module.js).

### Anti-Patterns to Avoid
- **Blocking email in POST handler:** Do NOT `await emailService.send()` before returning 201. Use fire-and-forget `.catch()` pattern.
- **Fetching hotel by owner_id in public POST:** Public endpoint gets hotel by slug only — no auth context available or needed.
- **Storing `nights` without validation:** Always validate `departure > arrival` before inserting — negative nights would corrupt price.
- **owner_email from `phone` field:** Phase 5 state doc confirms `hotel.phone used as mailto` but this is a WhatsApp number / phone, NOT email. The new `owner_email` column is required — do not reuse `phone` for email.
- **Status enum without DB constraint:** Define status as `text CHECK (status IN ('pending','confirmed','cancelled'))` rather than relying on app-level validation alone.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Email HTML | Custom HTML string with no structure | Extend existing EmailService HTML pattern | Already has CSS classes, responsive, tested |
| Auth guard for admin reservation routes | New middleware | `requireUser` + `verifyOwner(req, slug)` | Identical pattern used by all hotel mutation routes |
| Slug → hotel_id resolution | New DB query pattern | Existing `supabase.from('hotels').select('id,...').eq('slug', slug).single()` | Already proven in all hotel routes |
| Nights calculation | JS date library | `Math.round((new Date(dep) - new Date(arr)) / 86400000)` | Already used in `buildReservationMessage()` — exact same formula |
| Session passing in frontend | New auth system | `localStorage.getItem('agent_session_id')` + `X-Session-ID` header | Same as hotel-admin-module.js `apiFetch()` |
| Confirm dialog | Custom dialog | Reuse `showConfirm()` from hotel-admin-module.js | Already implemented with cleanup handlers |

**Key insight:** Phase 6 is almost entirely a composition of already-proven patterns. The risk is low because every building block exists.

---

## Common Pitfalls

### Pitfall 1: owner_email Column Missing at Deploy Time
**What goes wrong:** The `sendReservationNotification()` call silently fails because `hotels.owner_email` is NULL for all existing records (column didn't exist in Phase 5).
**Why it happens:** Phase 5 schema had no `owner_email` — State.md confirms "hotel.phone used as mailto recipient — no separate email column".
**How to avoid:** The DB migration (adding `owner_email` to hotels) must be in Wave 0 / Plan 1 before any route code is added. Admin panel must show a prompt "Įveskite savininko el. paštą" if `owner_email` is empty.
**Warning signs:** `owner_email` is null in Supabase dashboard for existing hotels.

### Pitfall 2: RLS Blocks Anonymous INSERT
**What goes wrong:** Public POST to `/api/hotels/:slug/reservations` returns 403 from Supabase because default RLS denies all.
**Why it happens:** Supabase tables have RLS enabled by default; INSERT requires explicit policy.
**How to avoid:** hotels.js uses `SUPABASE_SERVICE_ROLE_KEY` which bypasses RLS entirely — this is the existing pattern for all hotel writes. Anonymous insert works fine through the server (RLS only applies to direct Supabase client calls). No special RLS policy needed for server-side inserts via service role.
**Warning signs:** If using the anon key by accident, insert returns RLS error.

### Pitfall 3: Resend "onboarding@resend.dev" Domain Restriction
**What goes wrong:** Reservation notification emails only arrive at the Resend account owner's inbox, not the actual `owner_email`.
**Why it happens:** `email-service.js` line 22-28 clearly documents: "Emails will ONLY be sent to the Resend account owner" when using the test domain.
**How to avoid:** Test in dev knowing this limitation. For production, a custom domain must be verified in Resend dashboard. This is a deployment concern, not a code concern. Document in plan verification steps.
**Warning signs:** Emails not arriving at owner's address during testing.

### Pitfall 4: Form Submit Replaces WhatsApp/Email Buttons Entirely
**What goes wrong:** Removing the WhatsApp and email buttons breaks the fallback for guests who don't trust or can't use the form.
**Why it happens:** Misreading CONTEXT.md — "WhatsApp/email nuorodos lieka kaip antriniai CTA po forma" is a locked decision.
**How to avoid:** The submit button is PRIMARY. WhatsApp/email links remain but are moved to a secondary row below the main submit button with smaller styling.

### Pitfall 5: `nights` Stored as 0 When Dates Are Swapped
**What goes wrong:** Guest enters departure before arrival — `nights` becomes negative, `total_price` becomes negative.
**Why it happens:** Frontend `validate()` currently only checks that fields are non-empty, not that departure > arrival.
**How to avoid:** Add date order validation: `if (nights <= 0) { showError('Išvykimo data turi būti vėlesnė nei atvykimo'); return; }`.

### Pitfall 6: Admin Reservations Section Loads on Every Hotel Fetch
**What goes wrong:** Admin panel `init()` already calls `refreshHotel()` on every room save — if reservations are fetched inside `refreshHotel()`, every room save makes 2 API calls.
**Why it happens:** Coupling reservation fetch to the hotel refresh cycle.
**How to avoid:** Fetch reservations independently. Add a dedicated `loadReservations()` function, called once on init and after status PATCH. Do not tie to `refreshHotel()`.

---

## Code Examples

### Supabase Table Creation SQL
```sql
-- Add owner_email to hotels
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS owner_email text;

-- Create hotel_reservations table
CREATE TABLE hotel_reservations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  hotel_id uuid NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
  room_id uuid REFERENCES hotel_rooms(id) ON DELETE SET NULL,
  guest_name text NOT NULL,
  guest_email text,
  guest_phone text,
  arrival_date date NOT NULL,
  departure_date date NOT NULL,
  nights integer NOT NULL CHECK (nights > 0),
  total_price numeric(10,2),
  message text,
  status text NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'confirmed', 'cancelled')),
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Index for owner queries (fetch all reservations for a hotel)
CREATE INDEX hotel_reservations_hotel_id_idx ON hotel_reservations(hotel_id);
CREATE INDEX hotel_reservations_status_idx ON hotel_reservations(status);
```

### Email Template (Reservation Notification)
```javascript
// Follows existing EmailService HTML pattern: .header / .content / .footer divs
// Source: agent-network/server/services/email-service.js (sendVerificationEmail pattern)
const html = `
  <!DOCTYPE html>
  <html>
    <head><meta charset="utf-8"><style>
      body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
             line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
      .header { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white; padding: 30px 20px; border-radius: 10px 10px 0 0; text-align: center; }
      .content { background: #f9f9f9; padding: 30px 20px; border-radius: 0 0 10px 10px; }
      .detail-row { padding: 8px 0; border-bottom: 1px solid #eee; display: flex; gap: 12px; }
      .detail-label { color: #666; font-size: 13px; min-width: 120px; }
      .detail-value { font-weight: 600; }
      .status-badge { display: inline-block; background: #f59e0b; color: white;
                      padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
    </style></head>
    <body>
      <div class="header"><h2>Nauja rezervacijos užklausa</h2><p>${hotelName}</p></div>
      <div class="content">
        <span class="status-badge">NAUJA</span>
        <div class="detail-row"><span class="detail-label">Kambarys</span><span class="detail-value">${roomName}</span></div>
        <div class="detail-row"><span class="detail-label">Svečias</span><span class="detail-value">${guestName}</span></div>
        <div class="detail-row"><span class="detail-label">Atvykimas</span><span class="detail-value">${arrivalDate}</span></div>
        <div class="detail-row"><span class="detail-label">Išvykimas</span><span class="detail-value">${departureDate}</span></div>
        <div class="detail-row"><span class="detail-label">Naktys</span><span class="detail-value">${nights}</span></div>
        ${totalPrice ? `<div class="detail-row"><span class="detail-label">Suma</span><span class="detail-value">${totalPrice}€</span></div>` : ''}
        ${guestEmail ? `<div class="detail-row"><span class="detail-label">El. paštas</span><span class="detail-value"><a href="mailto:${guestEmail}">${guestEmail}</a></span></div>` : ''}
        ${guestPhone ? `<div class="detail-row"><span class="detail-label">Telefonas</span><span class="detail-value"><a href="tel:${guestPhone}">${guestPhone}</a></span></div>` : ''}
        ${message ? `<div class="detail-row"><span class="detail-label">Žinutė</span><span class="detail-value">${message}</span></div>` : ''}
        <p style="margin-top:24px;color:#666;font-size:13px;">
          Prisijunkite prie admin panelės, kad patvirtintumėte arba atšauktumėte rezervaciją.
        </p>
      </div>
    </body>
  </html>`;
```

### Admin Panel Reservation Card HTML (Vanilla JS)
```javascript
// Rendered in hotel-admin-module.js — follows existing card patterns
function createReservationCard(res) {
  const card = document.createElement('div');
  card.className = `reservation-card status-${res.status}`;
  card.innerHTML = `
    <div class="res-header">
      <span class="res-room">${res.hotel_rooms?.name || 'Kambarys'}</span>
      <span class="res-status-badge status-${res.status}">${STATUS_LABELS[res.status]}</span>
    </div>
    <div class="res-guest">${res.guest_name}</div>
    <div class="res-dates">${res.arrival_date} – ${res.departure_date} (${res.nights} naktys)</div>
    ${res.total_price ? `<div class="res-price">${res.total_price}€</div>` : ''}
    ${res.guest_email ? `<a href="mailto:${res.guest_email}" class="res-contact">${res.guest_email}</a>` : ''}
    ${res.guest_phone ? `<a href="tel:${res.guest_phone}" class="res-contact">${res.guest_phone}</a>` : ''}
    ${res.message ? `<div class="res-message">${res.message}</div>` : ''}
    <div class="res-actions">
      ${res.status === 'pending' ? `<button class="btn-confirm" data-id="${res.id}">Patvirtinti</button>` : ''}
      ${res.status !== 'cancelled' ? `<button class="btn-cancel" data-id="${res.id}">Atšaukti</button>` : ''}
    </div>
  `;
  return card;
}
const STATUS_LABELS = { pending: 'Laukia', confirmed: 'Patvirtinta', cancelled: 'Atšaukta' };
```

### Pending Count Badge on Admin Sidebar (Claude's Discretion — RECOMMENDED)
```javascript
// In renderRoomList() or a new renderReservationBadge() — show pending count
// as a small badge on the "Rezervacijos" section header
const pendingCount = reservations.filter(r => r.status === 'pending').length;
if (pendingCount > 0) {
  sectionHeader.innerHTML += ` <span class="pending-badge">${pendingCount}</span>`;
}
```

---

## Integration Points Summary

| Component | What Changes | Type |
|-----------|-------------|------|
| `server/routes/hotels.js` | Add 3 routes: POST `/:slug/reservations`, GET `/:slug/reservations`, PATCH `/:slug/reservations/:id/status` | Additive |
| `server/services/email-service.js` | Add `sendReservationNotification()` method | Additive |
| `public/modules/hotel-module.js` | Modify `createReservationForm()`: add email/phone fields, replace CTA with submit button, add async POST logic | Modification |
| `public/modules/hotel-admin-module.js` | Add `loadReservations()`, `renderReservationsSection()`, status PATCH calls | Additive |
| `public/hotel-admin.html` | Add "Rezervacijos" section HTML skeleton (filter tabs, reservation list container) | Additive |
| Supabase | `ALTER TABLE hotels ADD COLUMN owner_email`, create `hotel_reservations` table | Schema migration |

---

## Validation Architecture

> `workflow.nyquist_validation` key absent from config.json — treating as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Playwright (already installed in agent-network) |
| Config file | `agent-network/playwright.config.cjs` |
| Quick run command | `cd agent-network && npx playwright test --project=chromium hotel-reservations.spec.js` |
| Full suite command | `cd agent-network && npx playwright test` |

### Phase Requirements → Test Map
| Behavior | Test Type | Automated Command |
|----------|-----------|-------------------|
| POST `/api/hotels/:slug/reservations` saves to DB | API smoke | playwright test: fetch reservation endpoint, assert 201 + DB row |
| Missing required fields returns 400 | API unit | playwright test: POST without guest_name, assert 400 |
| Owner receives email notification on new reservation | Manual | Verify in Resend dashboard / account email (test domain limitation) |
| Admin GET `/api/hotels/:slug/reservations` returns list | API smoke | playwright test with session header |
| Status PATCH transitions correctly | API smoke | playwright test: confirm pending→confirmed, assert status |
| Form POST replaces WhatsApp redirect | E2E | playwright test: fill form, submit, verify success message shown |
| Admin panel shows "Rezervacijos" section | E2E | playwright test: load admin page, assert section visible |
| Confirm/Cancel buttons update status | E2E | playwright test: click confirm, reload, assert badge changes |

### Sampling Rate
- **Per task commit:** `npx playwright test hotel-reservations.spec.js --project=chromium`
- **Per wave merge:** `npx playwright test`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `agent-network/tests/hotel-reservations.spec.js` — covers all reservation API + E2E behaviors above
- [ ] Supabase migration SQL must be applied before any tests run (Wave 0 task)

---

## Open Questions

1. **Resend custom domain for production**
   - What we know: Current setup uses `onboarding@resend.dev` test domain — emails only go to Resend account owner
   - What's unclear: Whether the project has a verified custom domain in Resend
   - Recommendation: Note in plan verification steps; don't block implementation. Add `owner_email` field + admin save immediately so owner can test flow end-to-end even with test domain

2. **hotels.owner_email migration on Vercel**
   - What we know: Agent-network deploys to Vercel; Supabase schema changes are applied via Supabase dashboard SQL editor, not code migrations
   - What's unclear: Whether a Wave 0 plan step or a separate "run SQL manually" instruction is the right format
   - Recommendation: Plan should include explicit "Run this SQL in Supabase dashboard" step as Wave 0, separate from code changes

3. **owner_email input location in admin panel**
   - What we know: CONTEXT.md says "admin panelėje savininkas įveda savo el. paštą"
   - What's unclear: Whether this is a new "Nustatymai" section or added to existing hotel settings
   - Recommendation: Claude's discretion — add as a simple one-field inline form in the admin panel header or as part of hotel info section. Keep it minimal for Phase 6.

---

## Sources

### Primary (HIGH confidence)
- Direct code analysis: `agent-network/server/services/email-service.js` — full Resend integration pattern
- Direct code analysis: `agent-network/server/routes/hotels.js` — `verifyOwner`, `requireUser`, service role Supabase client, all route patterns
- Direct code analysis: `agent-network/public/modules/hotel-module.js` — `createReservationForm()`, `getFormData()`, `validate()`, form CTA structure
- Direct code analysis: `agent-network/public/modules/hotel-admin-module.js` — `apiFetch()`, `showConfirm()`, `refreshHotel()`, full admin lifecycle
- Direct code analysis: `agent-network/server/middleware/requireRole.js` — `requireUser` exact behavior (L2+ legacy + new auth)
- CONTEXT.md: All locked decisions, exact field names, enum values, flow specifications

### Secondary (MEDIUM confidence)
- STATE.md decision log: "hotel.phone used as mailto recipient — no separate email column in hotels table" — confirms owner_email is genuinely new
- Phase 5 CONTEXT.md: Hotels table schema fields confirmed (no owner_email column)
- Supabase service role bypass pattern: confirmed by hotels.js comment "Supabase client with service role key (bypasses RLS — owner check done in app code)"

### Tertiary (LOW confidence)
- None — all claims are grounded in direct code inspection

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new packages, all existing
- Architecture: HIGH — direct code inspection of all modified files
- Pitfalls: HIGH — grounded in specific code behaviors observed
- Email: HIGH — Resend integration fully read; one LOW item (custom domain status) flagged as open question
- DB schema: HIGH — exact SQL provided, matches CONTEXT.md decisions

**Research date:** 2026-03-20
**Valid until:** 2026-04-20 (stable stack, internal codebase — low churn risk)
