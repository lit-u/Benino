---
phase: 2
slug: scorer
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-18
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Inline `node -e` smoke scripts (no test runner needed) |
| **Base path** | `agent-network/server/services/news-collector/` |
| **Quick run command** | Copy the `<verify><automated>` command from the relevant plan task |
| **Full suite command** | Run each verify command from plans 02-01..02-03 sequentially |
| **Estimated runtime** | ~5–15 seconds per task (LLM calls ~3s via OpenRouter) |

---

## Sampling Rate

- **After every task commit:** Run the `<verify><automated>` command for that task
- **After every plan wave:** Run all verify commands for completed plans
- **Before `/gsd:verify-work`:** All verify commands must output PASS
- **Max feedback latency:** 15 seconds (heuristic tasks), 30 seconds (LLM tasks)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Automated Command | Status |
|---------|------|------|-------------|-------------------|--------|
| 2-01-01 | 01 | 1 | SCOR-01 | db.js migration smoke test | ⬜ pending |
| 2-01-02 | 01 | 1 | SCOR-01..03 | heuristic scorer smoke test | ⬜ pending |
| 2-01-03 | 01 | 1 | SCOR-04..05 | threshold filter smoke test | ⬜ pending |
| 2-02-01 | 02 | 2 | SCOR-02..03 | multi-source boost smoke test | ⬜ pending |
| 2-02-02 | 02 | 2 | SCOR-01..02 | LLM scorer smoke test (OpenRouter) | ⬜ pending |
| 2-03-01 | 03 | 3 | SCOR-01..05 | runScorer() integration smoke test | ⬜ pending |
| 2-03-02 | 03 | 3 | SCOR-01..05 | Human checkpoint — full pipeline verify | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

None — all tasks have inline `node -e` automated verify commands. No test stubs needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| LLM scores ambiguous items correctly | SCOR-02 | Requires judgment on LLM output quality | Inspect scored items in DB: `SELECT title, score, item_type FROM seen_urls WHERE scored_at IS NOT NULL LIMIT 20` |
| Threshold change takes immediate effect | SCOR-05 | Requires config edit + re-run observation | Edit `scoringThreshold` in settings.json, run `runScorer()`, verify filtered count changes |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify — inline node -e commands
- [ ] Sampling continuity: every task has an automated verify command
- [ ] No Wave 0 required
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
