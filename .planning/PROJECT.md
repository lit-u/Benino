# Benino — AI News Analyzer Module

## What This Is

Benino yra AI ekosistema su WhatsApp botu (Nanobot) ir web platforma (Agent Network / Pajūrio Tinklas). Šis GSD projektas seka naują modulį — **automatizuotą naujienų analizatorių**, kuris renka AI/tech naujienas, jas vertina pagal svarbą ir per Telegram botą leidžia patvirtinti arba atmesti publikavimą į Agent Network blogą.

## Core Value

Adminas gauna svarbias AI/tech naujienas į Telegram, vienu mygtuko paspaudimu patvirtina, ir jos automatiškai tampa pilnais blog post'ais Agent Network platformoje.

## Requirements

### Validated

<!-- Benino bazinė platforma jau veikia — čia tik šio modulio reikalavimai -->

(Šis GSD projektas prasideda nuo News Analyzer modulio — v1.0)

### Active

- [ ] Naujienų rinkėjas (Collector) iš 10 šaltinių kas 6 val.
- [ ] Naujienų vertinimo (Scoring) logika — svarbumo balas
- [ ] Telegram botas su Accept/Reject veiksmais
- [ ] LLM blog post generavimas (OpenRouter) + auto-tags
- [ ] Auto-publish į Agent Network blogą

### Out of Scope

- Viešas Telegram kanalas — ne šiame milestone
- Lietuviškų naujienų šaltiniai — v2
- Naudotojų subscription sistema — v2

## Context

**Esama infrastruktūra:**
- Agent Network (`agent-network/`) — Node.js/Express, Supabase, blog sistema veikia
- Sutvarkyk.js (`agent-network/sutvarkyk.js`) — URL → blog post pipeline (Groq LLM) — ŠABLONAS šiam projektui
- Nanobot (`nanobot/`) — Python, WhatsApp botas, OpenRouter/Groq

**Naujas modulis:** `newsbot/` arba `workspace/skills/newsbot/`
- Collector: RSS/HTTP polling (node-fetch, rss-parser)
- Scorer: Heuristics + LLM (OpenRouter)
- TG Bot: node-telegram-bot-api
- Publisher: HTTP POST į agent-network blog API

**Naujienų šaltiniai (v1):**
- Anthropic Blog (RSS)
- OpenAI Blog (RSS)
- Google AI Blog (RSS)
- GitHub Blog Changelog (RSS)
- HackerNews (Algolia API)
- GitHub Trending (scrape/API)
- GitHub Search (API — AI modeliai)
- HuggingFace Papers (RSS)
- HuggingFace Models (API — nauji modeliai)
- TAAFT — There's An AI For That (RSS)

**LLM Provider:** OpenRouter (`google/gemini-2.0-flash-001` arba konfigūruojamas)
**Blog autorius:** `OldBoy-RSS` (kaip sutvarkyk.js)

## Constraints

- **Tech stack**: Node.js (integravimui su agent-network) arba Python (integravimui su nanobot)
- **LLM**: OpenRouter — lengvai perjungiamas modelis per config
- **TG Bot**: Tuščias botas jau sukurtas — tik token reikia
- **Scoring threshold**: Konfigūruojamas — viršijus auto-trigger LLM rašymui
- **Rate limits**: GitHub API, HuggingFace API — reikia rate limiting

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Node.js (ne Python) | Tiesioginė integracija su agent-network blog API | — Pending |
| OpenRouter LLM | Lengvas modelio keitimas, billing kontrolė | — Pending |
| 6h cron interval | Balansas tarp aktualumo ir API apkrovos | — Pending |
| Publish to AN blog | Viena vieta visiems turiniams, existing pipeline | — Pending |

---
*Last updated: 2026-03-18 after v1.0 milestone start*
