---
name: reminder
description: Set WhatsApp reminders and recurring notifications using cron tool.
always: true
---

# Reminder Skill

Naudok `cron` tool priminimams kurti. Priminimas bus automatiškai pristatytas į dabartinį WhatsApp pokalbį.

## Kaip veikia

Kai vartotojas prašo priminimo, tu:
1. Išanalizuoji laiką (po kiek laiko arba konkrečią datą/laiką)
2. Suformuluoji trumpą priminimo žinutę
3. Iškvieti `cron` tool su tinkamais parametrais
4. Patvirtini vartotojui, kad priminimas sukurtas

**Svarbu:** `cron` tool automatiškai pristato priminimą į dabartinį pokalbį. Nereikia nurodyti kanalo ar gavėjo.

## Laiko interpretavimas

| Vartotojas sako | Parametras |
|----------------|------------|
| "po 5 min" / "už 5 minučių" | `delay_seconds=300` |
| "po valandos" / "už valandos" | `delay_seconds=3600` |
| "po 2 valandų" | `delay_seconds=7200` |
| "rytoj 9:00" | Apskaičiuok sekundes nuo dabar iki rytojaus 9:00 |
| "kas valandą" | `every_seconds=3600` |
| "kas dieną 8:00" | `cron_expr="0 8 * * *"` |
| "kas pirmadienį 9:00" | `cron_expr="0 9 * * 1"` |
| "darbo dienomis 17:00" | `cron_expr="0 17 * * 1-5"` |

## Pavyzdžiai

### Vienkartinis priminimas
Vartotojas: "Primink man po 30 min paskambinti Jonui"
```
cron(action="add", message="Paskambink Jonui! ☎️", delay_seconds=1800)
```
Atsakymas: "Gerai, priminsiu po 30 min paskambinti Jonui."

### Pasikartojantis priminimas
Vartotojas: "Kas dieną 8 ryto primink apie vaistus"
```
cron(action="add", message="Laikas gerti vaistus! 💊", cron_expr="0 8 * * *")
```
Atsakymas: "Sukurta! Kiekvieną dieną 8:00 priminsiu apie vaistus."

### Priminimų valdymas
Vartotojas: "Kokie mano priminimai?" / "Parodyk priminimus"
```
cron(action="list")
```

Vartotojas: "Pašalink priminimą apie vaistus"
```
cron(action="remove", job_id="abc123")
```

## Apskaičiavimas

Jei vartotojas nurodo konkretų laiką (pvz. "rytoj 15:00"):
1. Paimk dabartinį laiką (iš runtime info)
2. Apskaičiuok skirtumą sekundėmis
3. Naudok `delay_seconds` su apskaičiuotu skaičiumi

Jei vartotojas nurodo reguliarų laiką:
- Naudok `cron_expr` su standartine cron sintakse
- Formatas: `minutė valanda diena mėnuo savaitės_diena`

## Tonai

- Patvirtink priminimą trumpai ir draugiškai
- Priminimo žinutėje naudok emoji kad būtų matoma
- Jei neaišku kada - paklausk: "Kada norėtum gauti priminimą?"
