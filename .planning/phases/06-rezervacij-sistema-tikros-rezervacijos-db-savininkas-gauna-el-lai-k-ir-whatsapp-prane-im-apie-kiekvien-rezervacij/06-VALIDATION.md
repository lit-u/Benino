---
phase: 6
slug: rezervacij-sistema
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-20
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Playwright (already installed in agent-network) |
| **Config file** | `agent-network/playwright.config.cjs` |
| **Quick run command** | `cd agent-network && npx playwright test --project=chromium hotel-reservations.spec.js` |
| **Full suite command** | `cd agent-network && npx playwright test` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `cd agent-network && npx playwright test --project=chromium hotel-reservations.spec.js`
- **After every plan wave:** Run `cd agent-network && npx playwright test`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Behavior | Test Type | Automated Command | Status |
|---------|------|------|----------|-----------|-------------------|--------|
| 06-00-01 | 00 | 0 | Test stubs exist | file check | `test -f agent-network/tests/hotel-reservations.spec.js` | ⬜ pending |
| 06-01-01 | 01 | 1 | hotel_reservations table exists | API smoke | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |
| 06-01-02 | 01 | 1 | owner_email column in hotels | API smoke | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |
| 06-02-01 | 02 | 2 | POST /api/hotels/:slug/reservations saves to DB | API smoke | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |
| 06-02-02 | 02 | 2 | Missing required fields returns 400 | API unit | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |
| 06-02-03 | 02 | 2 | Admin GET returns reservation list | API smoke | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |
| 06-02-04 | 02 | 2 | Status PATCH transitions correctly | API smoke | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |
| 06-03-01 | 03 | 3 | Form POST replaces WhatsApp redirect | E2E | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |
| 06-03-02 | 03 | 3 | Success message shown after submit | E2E | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |
| 06-03-01 | 03 | 3 | Admin panel shows Rezervacijos section | E2E | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |
| 06-03-02 | 03 | 3 | Confirm/Cancel buttons update status | E2E | `npx playwright test hotel-reservations.spec.js --project=chromium` | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `agent-network/tests/hotel-reservations.spec.js` — Playwright spec with stubs for all reservation API + E2E behaviors (test.skip stubs so spec compiles without server)

*Wave 0 pattern: test.skip() stubs created before backend — per Phase 5 decision in STATE.md*

---

## Manual-Only Verifications

| Behavior | Why Manual | Test Instructions |
|----------|------------|-------------------|
| Owner receives email notification on new reservation | Resend test domain only delivers to account owner; can't assert inbox in CI | Submit test reservation, check Resend dashboard → sent emails |

---

## Validation Sign-Off

- [ ] All tasks have automated verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING test file references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
