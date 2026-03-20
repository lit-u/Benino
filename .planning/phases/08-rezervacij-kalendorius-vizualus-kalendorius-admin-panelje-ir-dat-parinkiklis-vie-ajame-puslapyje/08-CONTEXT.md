# Phase 8: Rezervacijų Kalendorius - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning
**Source:** PRD Express Path (inline)

<domain>
## Phase Boundary

This phase adds two calendar surfaces to the existing hotel reservation system:

1. **Admin panel calendar** — hotel owner sees a monthly grid showing all reservations, color-coded by status (confirmed/pending/cancelled). Clicking an entry opens the reservation detail.

2. **Public hotel page date picker** — guest selects check-in and check-out dates in the reservation form before submitting. Dates are validated (no past dates, check-out > check-in) and sent in the POST body.

No new backend tables needed — `hotel_reservations` already has `check_in` / `check_out` columns from Phase 6. Backend changes are minimal: ensure `check_in`/`check_out` fields are accepted in POST /api/reservations and returned in GET.

</domain>

<decisions>
## Implementation Decisions

### Admin Panel Calendar (CAL-01, CAL-02, CAL-03)
- Vanilla JS calendar — NO external libraries (pure HTML/CSS/JS, consistent with project stack)
- Monthly grid view: 7 columns (Mon–Sun), rows per week
- Each day cell shows reservation chips: guest name + room name, truncated
- Color coding: confirmed = `#22c55e` (green), pending = `#f59e0b` (yellow/amber), cancelled = `#6b7280` (grey)
- Clicking a chip (or day cell with one reservation) opens a detail panel — reuse existing reservation list item logic
- Month navigation: prev/next arrows, current month/year header
- Calendar placed in admin panel as a new tab alongside "Rezervacijos" list tab
- Calendar fetches from existing GET /api/hotels/:slug/reservations — filters by month client-side

### Public Date Picker (CAL-04, CAL-05, CAL-06)
- Native `<input type="date">` fields — no custom calendar widget
- Two fields: "Atvykimas" (check-in) and "Išvykimas" (check-out)
- `min` attribute on check-in = today's date (set dynamically via JS)
- `min` on check-out = check-in value + 1 day (updated when check-in changes)
- Both fields required for form submission
- Values sent as `check_in` and `check_out` in JSON body to POST /api/hotels/:slug/reservations
- UI placement: above the existing name/phone/message fields in the reservation form

### Backend (minimal changes)
- POST /api/hotels/:slug/reservations: accept `check_in` and `check_out` string fields, store in DB
- GET /api/hotels/:slug/reservations: include `check_in`, `check_out` in response JSON
- No availability conflict checking in this phase (future scope)

### Claude's Discretion
- Calendar CSS grid layout details
- Mobile responsiveness of calendar (chips may collapse to dots on narrow screens)
- Exact Lithuanian labels

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Hotel Admin Panel
- `agent-network/public/hotel-admin.html` — admin panel structure, tab system, reservation list section
- `agent-network/public/modules/hotel-admin-module.js` — reservation rendering, API calls, state management

### Public Hotel Page
- `agent-network/public/hotel.html` — public page structure, reservation form HTML
- `agent-network/public/modules/hotel-module.js` — reservation form submission logic

### Backend Routes
- `agent-network/server/routes/hotels.js` — POST /api/hotels/:slug/reservations and GET endpoints

### DB Schema
- `agent-network/server/routes/hotels.js` — hotel_reservations table columns (check_in, check_out already exist from Phase 6)

### CSS Patterns
- `agent-network/public/hotel-admin.html` — CSS variables (--a-bg, --a-card, --a-text, --a-accent etc.)
- `agent-network/public/hotel.html` — CSS variables (--h-bg, --h-card, --h-accent etc.)

</canonical_refs>

<specifics>
## Specific Ideas

- Admin calendar tab label: "Kalendorius"
- Public form: check-in label "Atvykimas", check-out label "Išvykimas"
- Confirmed chip color: `#22c55e` (matches existing status badge from Phase 6)
- Pending chip color: `#f59e0b`
- Cancelled chip color: `#6b7280`
- Calendar should work in both light and dark themes (use CSS vars)

</specifics>

<deferred>
## Deferred Ideas

- Availability conflict detection (blocked dates when room is full)
- iCal export
- Multi-room occupancy view
- Week view or agenda view

</deferred>

---

*Phase: 08-rezervacij-kalendorius*
*Context gathered: 2026-03-20 via PRD Express Path (inline)*
