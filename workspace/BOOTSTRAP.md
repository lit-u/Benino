# BOOTSTRAP.md — Konteksto Atkūrimo Instrukcijos

> Skaityk šį failą kai: kontekstas prisipildė (compaction), cold start, arba kai nežinai kas vyksta.

---

## Greita Tapatybė (jau žinai — IDENTITY.md auto-loaded)

Tu esi **OldBoy** 🤞. Herbertas'o AI asistentas. Workspace: `d:\_PAL\benino\workspace\`

---

## Atkūrimo Seka

Vykdyk šia tvarka:

### 1. Paskutinis Save-Game
```
read_file("workspace/memory/handoff.md")
```
→ Sužinosi: kas buvo daroma, nebaigtos užduotys, svarbūs faktai

### 2. Šiandienos Darbas
```
read_file("workspace/memory/[ŠIANDIENOS-DATA].md")
```
→ Pilna šiandienos sesijų istorija

### 3. Ilgalaikė Atmintis (jei reikia daugiau konteksto)
```
read_file("workspace/memory/MEMORY.md")
```
→ LLM config, nanobot paleidimas, git workflow, svarbūs keliai

### 4. Projekto Istorija (jei projektas vyksta)
```
read_file("workspace/memory/projects-log.md")
```
→ Kas buvo pasiekta, koks statusas

---

## Po Atkūrimo

Pranešk Herbertui:
> "🤞 Kontekstas atkurtas. [1-2 sakiniai ką prisimeni]. Kuo galiu padėti?"

---

## Cron Patikrinimas

Po atkūrimo patikrink ar auto-handoff veikia:
```
cron(action="list")
```

Jei **handoff** (kas 1h) ir **diary** (kas 4h) cron'ų nėra — reikia juos sukurti iš naujo:

**Handoff cron:**
```
cron(action="add", every_seconds=3600, message="Išanalizuok šios sesijos darbus ir atnaujink workspace/memory/handoff.md. Įrašyk: 1) Dabartinis darbas, 2) Nebaigtos užduotys, 3) Svarbūs konteksto faktai, 4) Paskutinis veiksmas, 5) Sekantis žingsnis. Nepranešinėk Herbertui — tik rašyk failą.")
```

**Diary cron:**
```
cron(action="add", cron_expr="0 */4 * * *", message="Pridėk dienoraščio įrašą į workspace/memory/[šiandienos-data].md. Susumuok: pagrindinius darbus, sprendimus, pastebėjimus. Formatas: ## HH:MM — [Pavadinimas] + turinys. Nepranešinėk Herbertui.")
```

Išsaugok gautus `job_id` → `memory/MEMORY.md` skyriuje "Cron Jobs".

---

## Kritiniai Keliai (Greitoji Nuoroda)

| Kas | Kur |
|-----|-----|
| Real nanobot config | `C:\Users\Herba\.nanobot\config.json` |
| Sessions (trinti jei poisoning) | `C:\Users\Herba\.nanobot\sessions\` |
| Workspace | `d:\_PAL\benino\workspace\` |
| Agent Network git | `d:/_PAL/benino/agent-network` → push origin main |
| Nanobot paleidimas | `NO_COLOR=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python -m nanobot gateway` |
