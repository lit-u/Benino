---
name: poilsis
description: >
  Interaktyvus atostogų planavimo įrankis. Veda per žaismingas Q&A klausimų
  serijas (kelionės tipas, trukmė, grupė, vaikai, biudžetas, veiklos, maistas,
  nakvynė, transportas), tada generuoja spalvingą kelionės scenarijų su
  dienotvarke ir "misijų" aprašymu vaikams, bei paruoštą Perplexity promptą.
  Naudoti kai vartotojas sako: "planuojam atostogas", "kur vykti vasarą",
  "poilsis", "/poilsis", "kelionės planas", "ką veikti su vaikais",
  "kur su šeima", "sukurk kelionės planą".
---

# /poilsis — Atostogų Planavimo Įrankis

## Web įrankis

Visas žaismingasis quiz su CSS scenomis ir interaktyviu srauto:

**→ http://localhost:3000/poilsis/sukurk** (local)
**→ https://www.sekmes.lt/poilsis/sukurk** (production)

## Terminal režimas

Kai vartotojas prašo planuoti kelionę per pokalbį (be naršyklės),
Claude veda Q&A pats ir sugeneruoja scenarijų bei Perplexity promptą.

### Klausimų seka:

1. **Kelionės tipas:** Pajūris / Gamta / Miestas / Kalnai / Egzotika / Stovyklavimas / SPA
2. **Trukmė:** Savaitgalis / Savaitė / 2 savaitės / Mėnuo+
3. **Grupė:** Vienas / Pora / Šeima su vaikais / Draugų grupė / Didelė grupė
4. **Vaikų amžius** *(jei Šeima)*: Kūdikis / Ikimokyklinis / Pradinukas / Paauglys
5. **Biudžetas:** Ekonomiškas (<200€) / Vidutinis (200-600€) / Komfortiškas / Premium
6. **Transportas:** Automobilis / Traukinys / Lėktuvas / Laivas / Kombinuotas
7. **Veiklos** *(iki 3)*: Vandens sportas / Žygiai / Kultūra / Renginiai / Kulinarija / ir kt.
8. **Maistas** *(iki 2)*: Vietinė virtuvė / Jūros gėrybės / Vegetariška / ir kt.
9. **Nakvynė:** Viešbutis / Nuoma / Stovykla / Agroturizmas / Glamping
10. **Jausmas grįžus:** Atsipūtęs / Nuotykio pilnas / Kultūringas / Aktyvus / Arčiau šeimos
11. **Vaikų veiklos** *(jei Šeima, iki 2)*: Gyvūnai / Parkas / Paplūdimys / ir kt.

### Rezultato struktūra:

```
🌊 JŪSŲ MISIJA: "[KŪRYBINIS PAVADINIMAS]"
[Trukmė] · [Grupė] · [Biudžeto ženklas]

📖 SCENARIJUS
[2 sakiniai aventūriniu stiliumi pagal tipą + grupę]

🗓️ DIENOTVARKĖ
Diena 1: 🚗 Atvykimas + įsikūrimas
Diena 2: [Veikla pagal tipą]
...
Diena N: 🌅 Atsisveikinimo ceremonija

🎯 VAIKO MISIJA (jei yra vaikų)
- ☐ [Užduotis 1]
- ☐ [Užduotis 2]
- ☐ 📸 Nufotografuoti labiausiai patikusią akimirką
- ☐ 🍦 Paragauti vietinio patiekalo

💡 3 VIETINIAI PATARIMAI

🔍 PERPLEXITY PROMPTAS
[Pilnas promptas su struktūra žemiau]
```

### Perplexity prompto struktūra:

```
Planuoju [TRUKMĖ] [TIPAS] kelionę. [GRUPĖ].
Biudžetas: [BIUDŽETAS]. Transportas: [TRANSPORTAS]. Nakvynė: [NAKVYNĖ].
Pomėgiai: [VEIKLOS]. Maistas: [MAISTAS].

**1. ATRAKCIJOS IR VEIKLOS** — 5-8 objektai su nuorodomis, darbo laiku, kaina
**2. NAKVYNĖ** — 3-4 variantai su Booking/Airbnb nuorodomis
**3. RESTORANAI** — 3 restoranai su Google Maps nuorodomis
**4. LOGISTIKA** — Rezervacija, transporto patarimai, atstumas
[**5. VAIKŲ VEIKLOS** — jei keliauja vaikai]
**6. BIUDŽETO SĄMATA** — Bendras ~€ vienam asmeniui
**7. VIETINIAI PATARIMAI** — Geriausi mėnesiai, vietinių paslaptys
```

## Trigger žodžiai

- "kur vykti atostogų"
- "planuok kelionę"
- "kelionės planas su vaikais"
- "ką veikti pajūryje"
- "kur su šeima vasarą"
- "atostogų idėjos"
- `/poilsis`
