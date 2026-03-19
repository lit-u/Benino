---
phase: 5
slug: hotel-mini-website-pajurio-namelis
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-19
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Playwright (already installed) |
| **Config file** | `agent-network/playwright.config.cjs` |
| **Quick run command** | `npx playwright test --project=chromium tests/hotel.spec.js` |
| **Full suite command** | `npx playwright test` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `npx playwright test --project=chromium tests/hotel.spec.js`
- **After every plan wave:** Run `npx playwright test`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** ~30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 5-01-01 | 01 | 1 | HOTEL-01 | Playwright smoke | `npx playwright test --project=chromium tests/hotel.spec.js::ssr-title` | ❌ W0 | ⬜ pending |
| 5-01-02 | 01 | 1 | HOTEL-02 | Playwright smoke | `npx playwright test --project=chromium tests/hotel.spec.js::json-ld` | ❌ W0 | ⬜ pending |
| 5-01-03 | 01 | 1 | HOTEL-03 | API integration | `npx playwright test --project=chromium tests/hotel.spec.js::create-hotel` | ❌ W0 | ⬜ pending |
| 5-02-01 | 02 | 1 | HOTEL-04 | Playwright auth | `npx playwright test --project=chromium tests/hotel.spec.js::admin-auth` | ❌ W0 | ⬜ pending |
| 5-02-02 | 02 | 1 | HOTEL-05 | API integration | `npx playwright test --project=chromium tests/hotel.spec.js::photo-upload` | ❌ W0 | ⬜ pending |
| 5-03-01 | 03 | 2 | HOTEL-06 | API smoke | `npx playwright test --project=chromium tests/hotel.spec.js::qr-png` | ❌ W0 | ⬜ pending |
| 5-03-02 | 03 | 2 | HOTEL-07 | Unit | `node -e "const d=new Date(); d.setDate(d.getDate()+7); require('./server/utils/hotel-utils.js').getAvailabilityStatus('occupied',d.toISOString())==='soon'"` | ❌ W0 | ⬜ pending |
| 5-03-03 | 03 | 2 | HOTEL-08 | Unit | `node -e "const u=require('./server/utils/hotel-utils.js').buildWhatsAppUrl('+37060000000','Test'); console.assert(u.startsWith('https://wa.me/'))"` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `agent-network/tests/hotel.spec.js` — Playwright tests covering HOTEL-01 through HOTEL-06 (SSR, JSON-LD, CRUD, auth, photo upload, QR)
- [ ] No new fixtures needed — existing `webServer` config in `playwright.config.cjs` handles server startup

*Existing Playwright infrastructure covers all phase test requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Drag-drop photo reorder saves correctly | HOTEL-05 | Visual interaction difficult to automate reliably in MVP | Open admin panel, drag photo, refresh page, verify order persisted in DB |
| WhatsApp deep link opens correct chat | HOTEL-08 | Requires WhatsApp installed on device | Tap "WhatsApp" CTA on room page, verify pre-filled message contains room number and hotel name |
| Traffic light color display | HOTEL-07 | CSS color verification | Open room with available_from within 14 days, verify yellow 🟡 badge shows |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
