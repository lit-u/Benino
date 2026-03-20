# Phase 6: Rezervacijų Sistema - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Sukurti tikrą rezervacijų sistemą: svetainės forma siunčia rezervacijos duomenis į DB (ne tik WhatsApp/mailto), savininkas gauna el. laišką apie kiekvieną naują rezervaciją, ir admin panelėje mato rezervacijų sąrašą su Patvirtinti/Atšaukti mygtukais.

**Kas neįeina:** mokėjimai, booking kalendorius su užblokuotomis datomis, automatiniai priminimų laiškai, svečio el. laiškas (savininkas susisiekia pats).

</domain>

<decisions>
## Implementation Decisions

### Rezervacijos duomenų modelis (Supabase)
- **Nauja lentelė:** `hotel_reservations`
- Laukai: `id` (uuid), `hotel_id` (FK → hotels), `room_id` (FK → hotel_rooms), `guest_name` (text, required), `guest_email` (text, optional — svečio kontaktas), `guest_phone` (text, optional), `arrival_date` (date), `departure_date` (date), `nights` (int, skaičiuojamas), `total_price` (numeric), `message` (text, optional), `status` (enum: pending/confirmed/cancelled, default: pending), `created_at` (timestamptz)
- **RLS:** savininkas mato tik savo viešbučio rezervacijas; svečias gali tik INSERT (be auth)

### Forma ir pateikimas (frontend)
- Esama rezervacijos forma (`hotel-module.js`) papildoma: vietoj tiesioginės WhatsApp/mailto nuorodos, forma POST'a į `/api/hotels/:slug/reservations`
- Reikalingi laukai: vardas, atvykimas, išvykimas — kiti neprivalomi
- WhatsApp/email nuorodos lieka kaip **antriniai** CTA po forma ("arba susisiekite tiesiogiai")
- Po sėkmingo POST: forma paslepiama, rodomas "✅ Rezervacija priimta! Savininkas susisieks su jumis netrukus."
- Klaidos atveju (server error): rodomas klaidos pranešimas, WhatsApp link kaip fallback

### Savininko notifikacija (el. laiškas)
- **Kanalas:** el. laiškas per esamą `email-service.js` (Resend)
- **Gavėjas:** savininko el. paštas — iš `hotels` lentelės `phone` lauko... bet `hotels` neturi `email` lauko. **Sprendimas:** pridėti `owner_email` lauką prie `hotels` lentelės; admin panelėje savininkas įveda savo el. paštą
- **Laiško turinys:** kambario pavadinimas, svečio vardas, atvykimas–išvykimas, naktų skaičius, suma, žinutė, svečio kontaktai (jei pateikti)
- **Siuntimas:** asinchroniškai po rezervacijos INSERT — klaida el. pašte neblokuoja rezervacijos sukūrimo
- WhatsApp pranešimas savininikui: ne automatinis — savininkas pats nusprendžia susisiekti su svečiu

### Admin rezervacijų valdymas
- **Vieta:** `/hotel/:slug/admin` — nauja sekcija "Rezervacijos" virš arba po kambarių sąrašu
- **Sąrašas:** kortelės su: kambario pavadinimas, svečio vardas, datos, naktų skaičius, suma, statusas (spalvotas badge), svečio kontaktai
- **Veiksmai:** "Patvirtinti" (pending → confirmed) + "Atšaukti" (pending/confirmed → cancelled)
- **Filtravimas:** pagal statusą (visi / laukiantys / patvirtinti / atšaukti) — Claude's discretion
- Tik `pending` rezervacijos rodomos pirma (svarbiausi)
- Paspaudus "Patvirtinti" — galimybė išsiųsti el. laišką svečiui (jei pateikė email) — **Claude's discretion**

### Claude's Discretion
- Tikslus el. laiško HTML dizainas (reuse esamo email-service.js stiliaus)
- Filtravimo UI detalės admin panelėje
- Ar rodyti rezervacijų skaičiaus badge'ą ant kambario kortelės admin puslapyje
- Svečio el. pašto siuntimo logika po patvirtinimo

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Esamas email servisas (PRIVALOMA perskaityti)
- `agent-network/server/services/email-service.js` — Resend integracija, `sendVerificationEmail()` pattern — ADAPTUOTI `sendReservationNotification()` metodui

### Esami hotel routes ir DB schema
- `agent-network/server/routes/hotels.js` — esami hotel CRUD routes, auth pattern (`verifyOwner`), Supabase queries — REUSE pattern
- `.planning/phases/05-hotel-mini-website-paj-rio-namelis-tipo-mini-svetain-ma-iems-apgyvendinimo-objektams/05-CONTEXT.md` — hotels, hotel_rooms lentelių schema

### Frontend forma (esama)
- `agent-network/public/modules/hotel-module.js` — `createReservationForm()`, `buildReservationMessage()`, `buildWhatsAppLink()` funkcijos — MODIFIKUOTI POST logikai

### Auth pattern
- `agent-network/server/middleware/auth-middleware.js` — public routes (be auth) pattern — rezervacijos POST turi veikti be auth (svečias neregistruotas)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `email-service.js` — Resend klase su HTML email pattern; tiesiog pridėti naują metodą `sendReservationNotification()`
- `createReservationForm()` (hotel-module.js) — esama forma su vardas/datos/žinutė laukais; papildyti guest_email/phone ir pakeisti submit logiką
- `verifyOwner` middleware (hotels.js) — apsaugo admin veiksmus; rezervacijų status update naudos tą patį

### Established Patterns
- Supabase insert su `.select()` — grąžina sukurtą įrašą su ID (kaip listings.js)
- Public POST route (be auth) — `/api/listings` leidžia anonymous insert; tas pats modelis rezervacijoms
- Async email siuntimas po DB insert — `await emailService.send()` catch'inamas atskirai

### Integration Points
- `server/routes/hotels.js` — pridėti `/api/hotels/:slug/reservations` (GET admin, POST public) ir `/:slug/reservations/:id/status` (PATCH admin)
- `hotel-admin.html` + `hotel-admin-module.js` — nauja "Rezervacijos" sekcija
- `hotel-module.js` — pakeisti form submit: POST į API vietoj WhatsApp redirect
- Supabase: nauja `hotel_reservations` lentelė + `owner_email` laukas `hotels` lentelėje

</code_context>

<specifics>
## Specific Ideas

- WhatsApp nuoroda lieka kaip fallback — svečiai, kurie nenori pildyti formos, gali tiesiogiai parašyti
- Savininko el. paštas saugomas `hotels.owner_email` — atskiras nuo `phone`; admin panelėje įvedamas per "Viešbučio nustatymai" sekciją
- Rezervacijos kortelė admin panelėje: vizualiai panaši į booking.com korteles — datos didelės, statusas ryškus, kontaktai klikabilūs

</specifics>

<deferred>
## Deferred Ideas

- Automatinis priminimas svečiui prieš atvykimą (24h el. laiškas) — atskira fazė
- Booking kalendorius su užblokuotomis datomis pagal patvirtintas rezervacijas — atskira fazė
- Mokėjimų integracija (Stripe/Paysera) prie rezervacijos — atskira fazė
- SMS pranešimas savininkui (Twilio) — v2
- Rezervacijų eksportas CSV/Excel — v2

</deferred>

---

*Phase: 06-rezervacijų-sistema*
*Context gathered: 2026-03-20*
