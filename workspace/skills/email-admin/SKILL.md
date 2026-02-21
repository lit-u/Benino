---
name: email-admin
description: Manage admin mailbox workflow (triage, priorities, draft replies, daily digest).
always: true
---

# Email Admin Skill

Use this skill when user asks to manage mailbox tasks for `admin@sekmes.lt`.

## Goals

- Triage incoming emails
- Mark priority and action type
- Propose concise Lithuanian replies
- Keep a daily summary with action list

## Triage Format

For each email, return:

1. Priority: `P1` (urgent), `P2` (important), `P3` (normal)
2. Type: `Sales`, `Support`, `Billing`, `Partner`, `Spam`, `Other`
3. One-line summary
4. Suggested next action
5. Draft reply (if needed)

## Reply Rules

- Keep tone professional and short.
- Do not invent facts.
- If request is unclear, ask one clarifying question.
- If legal/financial risk appears, flag it explicitly.

## Daily Digest

When user asks for "email suvestin?":

- Group by type and priority
- Provide:
  - `Reikia atsakyti ?iandien`
  - `Galima atid?ti`
  - `Ignoruoti / spam`

## Safety

- Never expose passwords or tokens in replies.
- Confirm before sending high-impact commitments.
