---
phase: 06-rezervacij-sistema
plan: 01
subsystem: reservation-backend
tags: [api, email, supabase, hotels, reservations]
dependency_graph:
  requires: [06-00]
  provides: [reservation-api, email-notification-method]
  affects: [agent-network/server/routes/hotels.js, agent-network/server/services/email-service.js]
tech_stack:
  added: []
  patterns: [fire-and-forget-email, verifyOwner-admin-guard, public-post-no-auth]
key_files:
  created: []
  modified:
    - agent-network/server/services/email-service.js
    - agent-network/server/routes/hotels.js
decisions:
  - Non-throwing email method: sendReservationNotification() returns { success: false } on error — never re-throws — consistent with sendWelcomeEmail pattern
  - Public POST route: No requireUser middleware — anonymous guests submit without session, service role key bypasses RLS
  - Fire-and-forget email: .catch() on email promise — reservation 201 never blocked by email failure
  - room_id optional: Validated conditionally — reservation can be submitted without specifying a room
metrics:
  duration: 7min
  completed_date: "2026-03-20"
  tasks_completed: 2
  files_modified: 2
---

# Phase 6 Plan 1: Reservation Backend API + Email Notification Summary

**One-liner:** POST/GET/PATCH reservation routes on hotel slug + amber-gradient Resend email notification method with fire-and-forget delivery.

## What Was Built

The complete reservation backend for the hotel mini-website system:

1. **`sendReservationNotification()` in EmailService** — new method that sends an amber/gold HTML email to the hotel owner when a new reservation arrives. Uses the same `.header/.content/.footer` CSS pattern as existing emails. Non-blocking: catches all errors and returns `{ success: false }` without throwing.

2. **3 reservation API routes in `hotels.js`:**
   - `POST /:slug/reservations` — public, no auth required. Validates guest_name, arrival_date, departure_date, nights > 0. Inserts to `hotel_reservations` table. Fires email asynchronously if `hotel.owner_email` is set.
   - `GET /:slug/reservations` — protected by `requireUser` + `verifyOwner()`. Returns all reservations for the hotel with room name/number joined, ordered newest first.
   - `PATCH /:slug/reservations/:reservationId/status` — protected. Validates status is `confirmed` or `cancelled`. Returns 404 if reservation not found or doesn't belong to the hotel.

## DB Migration (Pre-executed by User)

The following was confirmed applied in Supabase before this plan ran:
- `ALTER TABLE hotels ADD COLUMN IF NOT EXISTS owner_email text`
- `CREATE TABLE hotel_reservations (...)` with hotel_id FK, room_id FK, status CHECK constraint, 2 indexes

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | sendReservationNotification() method | ee17fa3 | server/services/email-service.js |
| 2 | 3 reservation routes | 2ffc569 | server/routes/hotels.js |

## Deviations from Plan

None — plan executed exactly as written.

## Verification Results

- `grep -c "sendReservationNotification" email-service.js` → 1 (method definition)
- `grep -c "if (!this.resend) return" email-service.js` → 1 (guard in new method; note: sendVerificationEmail uses try/catch pattern without early-return guard — only sendWelcomeEmail and the new method use the early-return guard)
- `grep -c "success: false, error: err.message" email-service.js` → 1 (non-throwing catch)
- `grep -c "RESERVATION ENDPOINTS" hotels.js` → 1
- `grep -c "import emailService" hotels.js` → 1
- `grep -c "emailService.sendReservationNotification" hotels.js` → 1
- `grep -c "hotel_reservations" hotels.js` → 3 (insert, select, update)
- Module load test: `node -e "import('./server/routes/hotels.js')..."` → no syntax errors (supabaseUrl error is expected in env-less test context)

## Self-Check

- [x] `agent-network/server/services/email-service.js` — modified (sendReservationNotification added)
- [x] `agent-network/server/routes/hotels.js` — modified (3 routes + emailService import added)
- [x] Commit ee17fa3 exists (Task 1)
- [x] Commit 2ffc569 exists (Task 2)
