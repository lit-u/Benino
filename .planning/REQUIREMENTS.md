# Requirements: Benino News Analyzer

**Defined:** 2026-03-18
**Core Value:** Adminas gauna svarbias AI/tech naujienas į Telegram ir vienu mygtuko paspaudimu patvirtina jų publikavimą kaip pilnus blog post'us.

## v1 Requirements

### Collector (Naujienų rinkimas)

- [x] **COLL-01**: Sistema renka naujienas iš 10 iš anksto nustatytų šaltinių (RSS + API)
- [x] **COLL-02**: Rinkimas vyksta automatiškai kas 6 valandas (cron job)
- [x] **COLL-03**: Sistema nesikartoja — jau matytos naujienos (URL hash) praleidžiamos
- [x] **COLL-04**: Šaltinių sąrašas konfigūruojamas per config failą (ne hardcoded)
- [x] **COLL-05**: Sistema veikia su šiais šaltiniais: Anthropic Blog, OpenAI Blog, Google AI Blog, GitHub Blog Changelog, HackerNews, GitHub Trending, GitHub Search, HuggingFace Papers, HuggingFace Models, TAAFT

### Scorer (Naujienų vertinimas)

- [x] **SCOR-01**: Kiekviena naujiena gauna svarbumo balą (0–100)
- [x] **SCOR-02**: Naujienų tipas automatiškai klasifikuojamas: `breakthrough` / `release` / `update` / `research`
- [x] **SCOR-03**: "Breakthrough" tipo naujienos (nauji modeliai, major release) gauna aukštą bazinį balą (≥70)
- [x] **SCOR-04**: Balo kėlimas jei ta pati tema aptinkama keliuose šaltiniuose (multi-source boost)
- [x] **SCOR-05**: Scoring threshold konfigūruojamas — viršijus balą, naujiena siunčiama į TG botą

### Telegram Bot (Moderavimas)

- [x] **TG-01**: Adminas TG bote gauna naujienų korteles su pavadinimu, šaltiniu, balu ir kategorija
- [x] **TG-02**: Kiekviena kortelė turi mygtukus: ✅ Priimti / ❌ Atmesti
- [x] **TG-03**: Paspaudus "Atmesti" — naujiena žymima kaip atmesta, nebesiunčiama
- [x] **TG-04**: Paspaudus "Priimti" — paleidžiamas LLM generavimas ir publikavimas
- [x] **TG-05**: Adminas gauna patvirtinimą kai blog post sėkmingai publikuotas (su nuoroda)

### Writer (Blog post generavimas)

- [ ] **WRIT-01**: LLM (OpenRouter) generuoja pilną blog post'ą iš naujienos (Mokslius + OldBoy stilius)
- [ ] **WRIT-02**: Generuojami auto-tags pagal temą (AI, modeliai, įrankiai ir pan.)
- [ ] **WRIT-03**: Kategorija parenkama automatiškai (kaip sutvarkyk.js)
- [ ] **WRIT-04**: Naudojamas modelis konfigūruojamas per config (default: `google/gemini-2.0-flash-001`)
- [ ] **WRIT-05**: Generavimas sutrumpėja jei naujiena trumpa (adaptyvi promto logika)

### Publisher (Publikavimas)

- [ ] **PUBL-01**: Patvirtintas blog post'as automatiškai publikuojamas Agent Network bloge
- [ ] **PUBL-02**: Autorius: `OldBoy-RSS` (kaip sutvarkyk.js pipeline)
- [ ] **PUBL-03**: Publikavimas serverio proceso viduje (ne atskiras išorinis skriptas) — tiesioginis Supabase įrašas su service key yra priimtinas bot autoriams (kaip `sutvarkyk.js` precedentas), nes blog API reikalauja L2 sesijos kurią botai neturi

## v2 Requirements

### Extended Sources

- **SRC-01**: Lietuviškų naujienų šaltiniai (Delfi tech, 15min tech, LRT)
- **SRC-02**: Twitter/X AI paskyros stebėjimas
- **SRC-03**: Newsletter integravimas (substack RSS)

### Advanced Scoring

- **SCOR-06**: Istorinė tendencija — tema kyla? (trending boost)
- **SCOR-07**: Auditorijos segmentavimas — techninė vs populiari žiniasklaida

### Distribution

- **DIST-01**: Viešas Telegram kanalas patvirtintoms naujienoms
- **DIST-02**: Weekly digest email

## Out of Scope

| Feature | Reason |
|---------|--------|
| Naudotojų subscription | Šis modulis skirtas adminui, ne galutiniams vartotojams |
| Real-time scraping | 6h cron pakankamas, real-time per brangus |
| Image generation | Kompleksas, v2+ |
| Dashboard UI | CLI/TG pakankamas v1 admin valdymui |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| COLL-01 | Phase 1 | Complete |
| COLL-02 | Phase 1 | Complete |
| COLL-03 | Phase 1 | Complete (01-01) |
| COLL-04 | Phase 1 | Complete (01-01) |
| COLL-05 | Phase 1 | Complete |
| SCOR-01 | Phase 2 | Complete |
| SCOR-02 | Phase 2 | Complete |
| SCOR-03 | Phase 2 | Complete |
| SCOR-04 | Phase 2 | Complete |
| SCOR-05 | Phase 2 | Complete |
| TG-01 | Phase 3 | Complete |
| TG-02 | Phase 3 | Complete |
| TG-03 | Phase 3 | Complete |
| TG-04 | Phase 3 | Complete |
| TG-05 | Phase 3 | Complete |
| WRIT-01 | Phase 4 | Pending |
| WRIT-02 | Phase 4 | Pending |
| WRIT-03 | Phase 4 | Pending |
| WRIT-04 | Phase 4 | Pending |
| WRIT-05 | Phase 4 | Pending |
| PUBL-01 | Phase 4 | Pending |
| PUBL-02 | Phase 4 | Pending |
| PUBL-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 23 total
- Mapped to phases: 23
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-18*
*Last updated: 2026-03-18 — COLL-03, COLL-04 marked complete after 01-01-PLAN.md execution*
