---
phase: 06-rezervacij-sistema
plan: 02
subsystem: ui
tags: [vanilla-js, fetch-api, forms, reservation, post]

# Dependency graph
requires:
  - phase: 06-01
    provides: POST /api/hotels/:slug/reservations endpoint that accepts guest data and saves to DB
provides:
  - Modified createReservationForm() in hotel-module.js — submits reservation via POST to API
  - Success state showing 'Rezervacija priimta' on 201 response
  - Error state with WhatsApp fallback on server failure
  - guest_email and guest_phone optional fields in reservation form
  - Date validation rejecting departure <= arrival
affects:
  - 06-03 (email/WhatsApp notification — triggered by the POST this plan submits)
  - 06-04 (owner reservation dashboard — displays reservations submitted by this form)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "fetch POST with async/await and try/catch for form submission"
    - "Inline <style> block inside innerHTML for component-scoped CSS"
    - "Replace entire formEl.innerHTML on success — clean success state without DOM manipulation"

key-files:
  created: []
  modified:
    - agent-network/public/modules/hotel-module.js

key-decisions:
  - "Inline <style> block inside formEl.innerHTML — scoped CSS without external stylesheet changes"
  - "Replace formEl.innerHTML on success (not just show message) — prevents re-submit and cleans up unused form fields"
  - "WhatsApp fallback in error message text (not a button) — keeps UI uncluttered"

patterns-established:
  - "Secondary CTAs as small gray links below primary submit button — progressive disclosure pattern"

requirements-completed: [RES-01, RES-05]

# Metrics
duration: 2min
completed: 2026-03-20
---

# Phase 06 Plan 02: Reservation Form — POST Submit Summary

**Public reservation form now POSTs to API via fetch, shows 'Rezervacija priimta' success state, and keeps WhatsApp/phone as secondary CTAs below the primary submit button**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-20T09:04:03Z
- **Completed:** 2026-03-20T09:06:00Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- Replaced WhatsApp/email primary CTA buttons with 'Siusti rezervacija' submit button (amber/gold, full-width)
- POST to `/api/hotels/:slug/reservations` with room_id, guest_name, dates, nights, total_price
- Success state: `formEl.innerHTML` replaced with green 'Rezervacija priimta!' paragraph
- Error state: descriptive message with WhatsApp fallback if hotel has whatsapp configured
- Added guest_email and guest_phone optional fields between name and message fields
- Updated `validate()` to check `nights <= 0` (departure must be after arrival)
- Retained WhatsApp and phone call as small secondary CTAs below submit button

## Task Commits

Each task was committed atomically:

1. **Task 1: Modify createReservationForm() — add fields, submit button, POST logic** - `5d037d3` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified
- `agent-network/public/modules/hotel-module.js` - createReservationForm() extended with POST submit, email/phone fields, date validation, success/error states, secondary CTAs

## Decisions Made
- Inline `<style>` block inside `formEl.innerHTML` for component-scoped CSS without touching external stylesheets
- `formEl.innerHTML` replacement on success — prevents re-submit possibility and removes all form DOM cleanly
- Secondary CTAs as plain anchor tags with small gray text — keeps primary submit button visually dominant

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Reservation form complete — guests can now submit reservations that are stored in DB
- Plan 06-03 (email/WhatsApp notification to hotel owner) can now be executed — it hooks into the POST endpoint that is now being called from the frontend

---
*Phase: 06-rezervacij-sistema*
*Completed: 2026-03-20*
