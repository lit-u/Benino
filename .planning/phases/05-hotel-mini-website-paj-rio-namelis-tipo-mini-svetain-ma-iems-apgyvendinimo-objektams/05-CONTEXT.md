# Phase 5: Hotel Mini-Website — Pajūrio Namelis - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Sukurti "mini svetainę" kiekvienam mažam apgyvendinimo objektui (pensionatui, kambariams, nameliais) sekmes.lt platformoje. Kiekvienas objektas gauna savo URL (`/hotel/:slug`), savininkas (L2+) valdo kambarių foto ir info per admin panelę (`/hotel/:slug/admin`), lankytojas mato gražų puslapį su jūros atžvilgiu ir gali rezervuoti per WhatsApp/email.

MVP apima: kambarių galerijoje + jūros atžvilgis + rezervacijos CTA + prieinamumo šviesoforas + QR kodai.
Booking kalendorius su DB rezervacijomis yra **ne šiame** etape.

</domain>

<decisions>
## Implementation Decisions

### Duomenų modelis
- **3 atskiros lentelės Supabase:** `hotels`, `hotel_rooms`, `room_photos`
- `hotels`: id, slug, owner_id (FK → users), name, description, address, city, phone, whatsapp, created_at
- `hotel_rooms`: id, hotel_id, number, name, price_per_night, area_m2, sea_distance_m, orientation (enum: N/NE/E/SE/S/SW/W/NW), orientation_note (tekstinis papildymas), noise_level (enum: quiet/moderate/lively), availability_status (enum: available/occupied), available_from (date, nullable), description
- `room_photos`: id, room_id, url, type (enum: window_view/interior), sort_order
- Savininkas: L2+ useris, gali turėti **kelis** hotel objektus (owner_id → N hotels)
- URL struktūra: `/hotel/:slug` (publika) + `/hotel/:slug/admin` (savininkas)

### Kambarių foto
- **2 tipai:** 1 `window_view` foto (rodomas pirmas, pagrindinis) + iki 5 `interior` foto
- **Saugykla:** Supabase Storage, bucket `hotel-photos`, kelias: `{hotel_id}/{room_id}/{type}-{sort}.jpg`
- **Admin valdymas:** drag-drop su eilės tvarkymu, `window_view` žymimas atskiru toggle
- **Auto resize:** 600×400px, max 50KB — naudoti esamą upload middleware, originalas ištrinamas
- **MVP kambarių limitas:** iki 10 kambarių per viešbutį

### Jūros atžvilgis (kambario lygmeniu)
- **Atstumas:** savininkas įveda metrais (pvz. 150), sistema rodo "2 min. pėsčiomis" (skaičiuojama: metrai ÷ 80 = minutės)
- **Orientacija:** pasaulio kryptis dropdown (N/NE/E/SE/S/SW/W/NW) + tekstinis `orientation_note` laukas (pvz. "Tiesiai į jūrą, saulėlydis pro langą")
- **Triukšmas:** 3 lygių dropdown: `quiet` (Ramus) / `moderate` (Vidutinis) / `lively` (Gyvas)
- Visi 3 laukai yra **kambario lygyje**, ne viešbučio — skirtingi kambariai gali turėti skirtingas vertes
- JSON-LD: `sea_distance_m`, `orientation`, `noise_level` eksponuojami kaip struktūrizuoti duomenys

### Rezervacija + Prieinamumas
- **Šviesoforas:** savininkas admin panelėje rankiniu būdu perjungia statusą:
  - 🟢 `available` — rodoma "LAISVAS"
  - 🔴 `occupied` + `available_from` data — rodoma "UŽIMTAS / Laisvas nuo: [data]"
  - 🟡 jei `available_from` yra per 14 dienų — geltona "Laisvas netrukus"
- **Rezervacijos CTA:** mygtukas "Rezervuoti" → mini forma (vardas, atvykimas, išvykimas, žinutė) → savininkas pasirenka siuntimo kanalą: 📱 WhatsApp arba 📧 El. paštas
- Forma siunčia tik žinutę — ne į DB, o tiesiai per WhatsApp deep link arba `mailto:`

### QR kodai
- Kiekvienas kambarys gauna QR → `sekmes.lt/hotel/{slug}#room-{number}`
- Admin panelėje: mygtukas "Atsisiųsti QR (PDF)" + "Kopijuoti URL"
- Savininkas gali išspausdinti ir pakabinti kambaryje

### AI/Agents Friendly
- **SSR renderinimas:** `/hotel/:slug` grąžina pilną HTML iš serverio (kaip esamas `/:type/:slug` pattern) — ne SPA
- **JSON-LD schema:** `LodgingBusiness` (viešbutis) + `HotelRoom` (kambariai) su `name`, `description`, `priceRange`, `address`, `amenityFeature` (jūros atstumas, orientacija, triukšmas)
- **Semantic HTML:** `<article>`, `<address>`, `<time>` — ne `<div>` sriubos
- **Meta tags:** `og:title`, `og:description`, `og:image` (pirmasis kambario foto), canonical URL
- Reuse esamą `injectMeta()` funkciją iš `server/index.js` — praplėsti su hotel schema

### Claude's Discretion
- Tikslus puslapio dizainas ir CSS (dark theme kaip likusi platforma)
- QR generavimo biblioteka (pvz. `qrcode` npm)
- Supabase Storage bucket konfigūracija ir RLS taisyklės
- Prieinamumo šviesoforo tikslus spalvų kodas UI

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Esami patterns (PRIVALOMA perskaityti)
- `agent-network/server/index.js` §686-780 — `injectMeta()` funkcija ir SSR meta injection pattern — REUSE šiam
- `agent-network/server/routes/listings.js` — listing CRUD pattern su Supabase, slug generation, auth middleware
- `agent-network/server/routes/upload.js` — esamas foto upload su resize — REUSE arba adaptuoti
- `agent-network/server/utils/slug-generator.js` — slug generavimo utils
- `agent-network/server/middleware/auth-middleware.js` — `requireAuthLevel` L2+ apsauga

### Esami hotel routes (kontekstui)
- `agent-network/server/routes/hotel-map.js` — Google Maps Static API proxy (iš 3D projekto)
- `agent-network/server/routes/hotel-street-view.js` — Street View embed + wing orientacijos logika (WING_HEADINGS pattern tinka orientacijai)

### DB schema referensai
- No external specs — requirements fully captured in decisions above

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `injectMeta()` (server/index.js:686) — SSR meta + JSON-LD injection, tiesiai reusable hotel puslapiams
- `requireAuthLevel` middleware — L2+ apsauga admin routams
- `upload.js` route — foto upload su auto-resize, tik adaptuoti bucket pavadinimą
- `slug-generator.js` — generuoti hotel slug iš pavadinimo
- WING_HEADINGS objektas (hotel-street-view.js) — N/NE/E/SE/S/SW/W/NW → laipsniai, panašus pattern orientacijai

### Established Patterns
- Visas SSR: `/:type/:slug` → Supabase query → injectMeta() → sendFile(indexHtmlPath) — tiksliai tas pats hotelams
- Frontend: Vanilla JS ES6 modules (`public/modules/`) — nauja `hotel-module.js`
- Auth: `requireAuthLevel('L2')` middleware prieš admin routes
- Supabase RLS: service role key bypass serveryje (kaip listings.js)

### Integration Points
- `server/index.js` — pridėti `/hotel/:slug` SSR route ir `/hotel/:slug/admin` route
- `public/` — naujas `hotel.html` (publika) + `hotel-admin.html` (admin)
- `public/modules/` — `hotel-module.js` + `hotel-admin-module.js`
- Supabase: naujos lentelės `hotels`, `hotel_rooms`, `room_photos` + Storage bucket `hotel-photos`

</code_context>

<specifics>
## Specific Ideas

- Jūros atžvilgio blokas vizualiai primena "info kortelę": 🌊 Iki jūros: 2 min. / 🧭 Orientacija: Vakarų (saulėlydis) / 🔇 Triukšmas: Ramus
- Šviesoforas kambario kortelėje — ryški žalia/raudona/geltona spalva su "LAISVAS" / "UŽIMTAS" tekstas
- Lango vaizdo foto rodomas pirmas galerijoje, su subtiliu "🪟 Lango vaizdas" ženklu
- QR kodas gali būti naudojamas ir fiziškai — savininkas išspausdina ir klijuoja prie kambario durų
- Foto resize: 600×400, max 50KB — svarbu greičiui ir Supabase Storage limitams

</specifics>

<deferred>
## Deferred Ideas

- Pilnas booking kalendorius su rezervacijomis DB — tai yra C versija (atskira fazė)
- Pajūrio 2.5D žemėlapis su viešbučiais kaip interaktyviais pin'ais — ilgalaikė vizija, atskira fazė
- Room planner (baldų stumdymas) — blueprint3d arba react-planner integracija — atskira fazė
- Stripe/Paysera mokėjimų integracija — atskira fazė
- Multi-language (EN/DE) — v2
- Savininko dashboard su visų objektų statistika — atskira fazė

</deferred>

---

*Phase: 05-hotel-mini-website*
*Context gathered: 2026-03-19*
