---
phase: 05-hotel-mini-website
plan: 01
subsystem: agent-network/server
tags: [hotels, supabase, qrcode, express-router, image-upload]
dependency_graph:
  requires: []
  provides:
    - agent-network/server/routes/hotels.js
    - agent-network/server/services/hotel-image-service.js
    - agent-network/scripts/hotel-schema.sql
  affects:
    - agent-network/server/index.js
tech_stack:
  added:
    - qrcode@1.5.4 (npm package, QR PNG generation)
  patterns:
    - Express Router CRUD with requireUser owner isolation
    - HotelImageService extends ImageUploadService (bucket override pattern)
    - SQL schema with TEXT owner_id (no FK — auth transition safety)
key_files:
  created:
    - agent-network/server/routes/hotels.js
    - agent-network/server/services/hotel-image-service.js
    - agent-network/scripts/hotel-schema.sql
  modified:
    - agent-network/server/index.js
    - agent-network/package.json
decisions:
  - "owner_id is TEXT (not UUID FK) in hotels table — avoids FK constraint failures during dual-auth system transition"
  - "HotelImageService extends ImageUploadService — thin subclass overrides bucketName and watermarkPath, reuses all compression logic"
  - "verifyOwner() helper checks req.authContext.userId || req.auth.identityId — compatible with both legacy and new auth systems"
  - "QR endpoint is public (no auth) — anyone can generate a QR for a room URL"
  - "Room limit 10, photo limit 6 enforced at API level before insert"
metrics:
  duration: "68 min"
  completed_date: "2026-03-19"
  tasks_completed: 3
  files_created: 3
  files_modified: 2
---

# Phase 05 Plan 01: Hotel Backend — Schema, CRUD API, Image Service Summary

**One-liner:** Express CRUD API for hotels/rooms/photos at /api/hotels with QR PNG generation, HotelImageService extending ImageUploadService for hotel-photos bucket, and 3-table Supabase schema (hotels/hotel_rooms/room_photos) with TEXT owner_id and RLS.

## What Was Built

### Task 1 — DB Schema + HotelImageService + qrcode install
- `agent-network/scripts/hotel-schema.sql`: 3 tables (`hotels`, `hotel_rooms`, `room_photos`) with all fields from CONTEXT.md. RLS enabled on all 3 tables. Public read policies for all. Owner write policies using TEXT owner_id cast comparison. No UUID FK on owner_id per research open question resolution.
- `agent-network/server/services/hotel-image-service.js`: Extends `ImageUploadService`. Overrides `bucketName = 'hotel-photos'` and `watermarkPath = null`. Adds `uploadRoomPhoto(buffer, name, hotelId, roomId, type, sortOrder)` and `deleteRoomPhoto(filePath)`.
- `npm install qrcode@1.5.4`

### Task 2 — hotels.js CRUD API Route
- 12 route handlers on Express router
- Public: `GET /`, `GET /:slug`, `GET /:slug/rooms/:num/qr`
- Protected (requireUser): `POST /`, `PUT /:slug`, `DELETE /:slug`
- Room CRUD: `POST /:slug/rooms`, `PUT /:slug/rooms/:roomId`, `DELETE /:slug/rooms/:roomId`
- Photo management: `POST /:slug/rooms/:roomId/photos`, `PUT /:slug/rooms/:roomId/photos/order`, `DELETE /:slug/rooms/:roomId/photos/:photoId`
- `verifyOwner()` helper queries hotels table and checks owner_id against both auth systems
- Room limit: 10 per hotel; photo limit: 6 per room (existing + new checked before upload)
- QR generates PNG buffer via `QRCode.toBuffer()` with `Content-Type: image/png`

### Task 3 — Register routes in server/index.js
- Added `import hotelsRouter from './routes/hotels.js'` at line 100
- Added `app.use('/api/hotels', hotelsRouter)` at line 232 (after news routes, before SPA fallback)

## Decisions Made

1. **TEXT owner_id**: Research doc showed an open question about owner_id FK type. Plan explicitly resolved it as TEXT (not UUID FK) to avoid FK constraint failures during dual-auth system transition. Enforced in application code, not DB.

2. **HotelImageService as thin subclass**: All compression/upload/bucket logic reused from ImageUploadService parent. Only bucketName and watermarkPath overridden. Custom `uploadRoomPhoto()` adds hotel-specific path format: `{hotelId}/{roomId}/{type}-{sortOrder}-{uuid}.jpg`.

3. **QR endpoint is public**: No `requireUser` on QR generation — rooms are public info, QR just encodes the public URL. Consistent with GET /:slug also being public.

4. **verifyOwner dual-auth compatibility**: Checks `req.authContext?.userId` (legacy) OR `req.auth?.identityId` (new). Same pattern as existing listings.js and research doc recommendation.

## Deviations from Plan

None — plan executed exactly as written.

## Commits

| Task | Commit | Files |
|------|--------|-------|
| Task 1: Schema + HotelImageService + qrcode | 36b6c10 | scripts/hotel-schema.sql, server/services/hotel-image-service.js, package.json |
| Task 2: hotels.js CRUD API | 1cd785e | server/routes/hotels.js |
| Task 3: Register in index.js | 4d6964b | server/index.js |

## Self-Check: PASSED

- FOUND: agent-network/scripts/hotel-schema.sql
- FOUND: agent-network/server/services/hotel-image-service.js
- FOUND: agent-network/server/routes/hotels.js
- FOUND: commit 36b6c10 (Task 1)
- FOUND: commit 1cd785e (Task 2)
- FOUND: commit 4d6964b (Task 3)
