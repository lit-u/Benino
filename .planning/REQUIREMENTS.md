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

- [x] **WRIT-01**: LLM (OpenRouter) generuoja pilną blog post'ą iš naujienos (Mokslius + OldBoy stilius)
- [x] **WRIT-02**: Generuojami auto-tags pagal temą (AI, modeliai, įrankiai ir pan.)
- [x] **WRIT-03**: Kategorija parenkama automatiškai (kaip sutvarkyk.js)
- [x] **WRIT-04**: Naudojamas modelis konfigūruojamas per config (default: `google/gemini-2.0-flash-001`)
- [x] **WRIT-05**: Generavimas sutrumpėja jei naujiena trumpa (adaptyvi promto logika)

### Publisher (Publikavimas)

- [x] **PUBL-01**: Patvirtintas blog post'as automatiškai publikuojamas Agent Network bloge
- [x] **PUBL-02**: Autorius: `OldBoy-RSS` (kaip sutvarkyk.js pipeline)
- [x] **PUBL-03**: Publikavimas serverio proceso viduje (ne atskiras išorinis skriptas) — tiesioginis Supabase įrašas su service key yra priimtinas bot autoriams (kaip `sutvarkyk.js` precedentas), nes blog API reikalauja L2 sesijos kurią botai neturi

### Rezervacijų Sistema (Hotel Reservations)

- [x] **RES-01**: Svečias pateikia rezervacijos formą — duomenys saugomi `hotel_reservations` lentelėje per POST API
- [x] **RES-02**: Savininkas gauna el. laišką (Resend) apie kiekvieną naują rezervaciją
- [x] **RES-03**: Admin panelėje rodomas rezervacijų sąrašas su statuso badge'ais (Laukia/Patvirtinta/Atsaukta)
- [x] **RES-04**: Savininkas gali patvirtinti arba atšaukti kiekvieną rezervaciją per admin panelę
- [x] **RES-05**: WhatsApp ir el. pašto nuorodos lieka kaip antriniai CTA po forma
- [x] **RES-06**: `owner_email` laukas pridėtas prie `hotels` lentelės; savininkas įveda per admin panelę

### Multi-Hotel (Savitarnos panelė)

- [x] **MH-01**: `GET /api/hotels/mine` grąžina tik autentifikuoto vartotojo viešbučius
- [x] **MH-02**: `POST /api/hotels` be sesijos grąžina 401
- [x] **MH-03**: `POST /api/hotels` L2 vartotojui sukuria viešbutį ir grąžina slug
- [x] **MH-04**: `/my-hotels` puslapis rodo auth gate neautentifikuotam vartotojui
- [x] **MH-05**: Po viešbučio sukūrimo naršyklė nukreipia į `/hotel/:slug/admin`
- [x] **MH-06**: Soft limitas: 4-o viešbučio kūrimas grąžina 400

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
| WRIT-01 | Phase 4 | Complete |
| WRIT-02 | Phase 4 | Complete |
| WRIT-03 | Phase 4 | Complete |
| WRIT-04 | Phase 4 | Complete |
| WRIT-05 | Phase 4 | Complete |
| PUBL-01 | Phase 4 | Complete |
| PUBL-02 | Phase 4 | Complete |
| PUBL-03 | Phase 4 | Complete |
| RES-01 | Phase 6 | Planned (06-00, 06-01, 06-02) |
| RES-02 | Phase 6 | Planned (06-01) |
| RES-03 | Phase 6 | Planned (06-00, 06-03) |
| RES-04 | Phase 6 | Planned (06-00, 06-01, 06-03) |
| RES-05 | Phase 6 | Planned (06-02) |
| RES-06 | Phase 6 | Planned (06-01, 06-03) |
| MH-01 | Phase 7 | Planned (07-00, 07-01) |
| MH-02 | Phase 7 | Planned (07-00, 07-01) |
| MH-03 | Phase 7 | Planned (07-00, 07-01) |
| MH-04 | Phase 7 | Planned (07-00, 07-02) |
| MH-05 | Phase 7 | Planned (07-00, 07-02) |
| MH-06 | Phase 7 | Planned (07-00, 07-01) |

**Coverage:**
- v1 requirements: 35 total
- Mapped to phases: 35
- Unmapped: 0

---
*Requirements defined: 2026-03-18*
*Last updated: 2026-03-20 — Phase 7 (MH-01 through MH-06) added and mapped to plans*
