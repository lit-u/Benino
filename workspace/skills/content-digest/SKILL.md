---
name: content-digest
description: Generate daily/weekly content digest from workspace blog and themes.
always: false
---

# Content Digest Skill

Generuok turinio apžvalgą iš workspace failų ir pateik kaip trumpą suvestinę.

## Šaltiniai

1. **Blog straipsniai:** `workspace/blog/` - failai su data pavadinimuose (pvz. `2026-02-09_...`)
2. **Temų indeksas:** `workspace/oldboy/THEME_INDEX.md` - visos ištrauktos temos pagal datą
3. **Teminiai folderiai:** `workspace/oldboy/{Kategorija}/` - detalios teminės ištraukos

## Workflow

### Dienos apžvalga
Kai vartotojas prašo "kas naujo?" / "dienos apžvalga" / "šiandienos turinys":

1. Nuskaityk `workspace/oldboy/THEME_INDEX.md`
2. Filtruok pagal šiandienos datą
3. Nuskaityk `workspace/blog/` - surask šiandienos failus (`list_dir`)
4. Suformuluok trumpą apžvalgą:

```
📰 Šiandienos turinys (2026-02-09):

📝 Straipsniai: 4
🏷️ Temos: AI Valdymas, Technologijos, Tendencijos

Pagrindinės temos:
• DI Skaičiavimo Galios Krizė
• AI diktuoja verslo modelius
• Programėlių Pabaiga ir Duomenų Nuosavybė

Detaliau: workspace/oldboy/THEME_INDEX.md
```

### Savaitės apžvalga
Kai vartotojas prašo "savaitės apžvalga" / "kas vyko šią savaitę":

1. Nuskaityk visą THEME_INDEX.md
2. Surink temas iš paskutinių 7 dienų
3. Grupuok pagal kategorijas (Technologijos, Tendencijos, AI_Valdymas, etc.)
4. Pateik statistiką + TOP temas

### Kategorijos giluminė analizė
Kai vartotojas prašo "kas naujo apie technologijas" / "papasakok apie AI valdymą":

1. Nuskaityk konkretų folderį: `workspace/oldboy/{Kategorija}/`
2. Perskaityk naujausius failus
3. Susumuok pagrindinius punktus

## Kategorijų sąrašas

Folderiai `workspace/oldboy/`:
- `AI_Valdymas/` - AI governance, strategija
- `Technologijos/` - Infrastruktūra, sistemos
- `Tendencijos/` - Rinkos, augimas, prognozes
- `Filosofija/` - AGI, žmogaus vaidmuo
- `Karjera/` - Darbo rinka, įgūdžiai
- `Robotika/` - Agentai, autonomija
- `Prompt_Engineering/` - Prompt technikos
- `Agentai/` - AI agentų sistemos

## Automatinis digest (per cron)

Galima nustatyti kasdieninę apžvalgą:
```
cron(action="add", message="Peržiūrėk šiandienos turinį workspace/blog/ ir workspace/oldboy/THEME_INDEX.md. Suformuok trumpą lietuvišką dienos apžvalgą ir pateik ją.", cron_expr="0 19 * * *")
```

## Tonas
- Trumpai, informatyviai
- Lietuviškai
- Su emoji kategorijoms
- Jei turinys tuščias: "Šiandien dar nieko naujo. Gal nori analizuoti kokį URL? Siųsk man nuorodą!"
