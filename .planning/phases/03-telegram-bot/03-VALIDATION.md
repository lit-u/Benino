---
phase: 3
slug: telegram-bot
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Inline `node -e` smoke scripts + live Telegram API calls |
| **Base path** | `agent-network/server/services/news-collector/telegram/` |
| **Quick run command** | Copy the `<verify><automated>` command from the relevant plan task |
| **Full suite command** | Run each verify command from plans 03-01..03-03 sequentially |
| **Estimated runtime** | ~5s per task (network: Telegram API ~1s) |

---

## Sampling Rate

- **After every task commit:** Run the `<verify><automated>` command for that task
- **After every plan wave:** Run all verify commands for completed plans
- **Before `/gsd:verify-work`:** All verify commands must output PASS
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Automated Command | Status |
|---------|------|------|-------------|-------------------|--------|
| 3-01-01 | 01 | 1 | TG-03..04 | db.js tg columns smoke test | ⬜ pending |
| 3-01-02 | 01 | 1 | TG-03..04 | Config telegram block + test scaffold | ⬜ pending |
| 3-02-01 | 02 | 2 | TG-01..02 | sendNewsCard() sends real TG message | ⬜ pending |
| 3-02-02 | 02 | 2 | TG-03..04 | callback_query handler import smoke test | ⬜ pending |
| 3-03-01 | 03 | 3 | TG-01..05 | dispatchPendingItems() + server integration smoke | ⬜ pending |
| 3-03-02 | 03 | 3 | TG-01..05 | Human checkpoint — live TG card + button press | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

None — all tasks have inline automated verify commands.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Accept/Reject buttons work in TG | TG-02..04 | Requires human to press inline button | Human checkpoint in plan 03-03 |
| Phase 4 stub triggers correctly | TG-04 | Requires Phase 4 endpoint | Accept → check log for stub call |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify
- [ ] Sampling continuity maintained
- [ ] No Wave 0 required
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
