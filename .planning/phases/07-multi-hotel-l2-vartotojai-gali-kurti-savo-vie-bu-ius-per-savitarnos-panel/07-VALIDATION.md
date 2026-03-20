---
phase: 7
slug: multi-hotel-l2-vartotojai-gali-kurti-savo-vie-bu-ius-per-savitarnos-panel
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-20
---

# Phase 7 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Playwright |
| **Config file** | `agent-network/playwright.config.cjs` |
| **Quick run command** | `npx playwright test hotel-multi.spec.js --project=chromium` |
| **Full suite command** | `npx playwright test --project=chromium` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `npx playwright test hotel-multi.spec.js --project=chromium`
- **After every plan wave:** Run `npx playwright test --project=chromium`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 07-00-01 | 00 | 0 | MH-01..06 | stub | `npx playwright test hotel-multi.spec.js --project=chromium` | ❌ W0 | ⬜ pending |
| 07-01-01 | 01 | 1 | MH-01 | e2e | `npx playwright test hotel-multi.spec.js --project=chromium` | ✅ | ⬜ pending |
| 07-02-01 | 02 | 2 | MH-02,03 | e2e | `npx playwright test hotel-multi.spec.js --project=chromium` | ✅ | ⬜ pending |
| 07-03-01 | 03 | 2 | MH-04,05,06 | e2e | `npx playwright test hotel-multi.spec.js --project=chromium` | ✅ | ⬜ pending |

---

## Wave 0 Requirements

- [ ] `agent-network/tests/hotel-multi.spec.js` — stubs for MH-01..MH-06

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| L2 user receives hotel admin link after creation | MH-03 | Requires real L2 session | Login as L2, create hotel, verify redirect to /hotel/:slug/admin |
| Hotel appears in public listing | MH-06 | Requires DB + render check | Create hotel, visit /, verify listing card appears |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
