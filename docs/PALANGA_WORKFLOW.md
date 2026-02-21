# Palanga Workflow - Content Analysis & Publishing System

## 📋 Overview

**Palanga metodologija** sukuria **dvigubą analizę** bet kokio šaltinio (YouTube, arXiv, podcast, article):
1. **Mokslius** - techninė, chronologinė, akademinė analizė (asmeninis archyvas)
2. **OldBoy** - naratyvinė, atmosferinė, Palangos stiliaus analizė (blog publikacija)

---

## 🔄 Workflow

### Veiksmas-1: Analizė (Šaltinio Apdorojimas)

**Komanda:**
```
sutvarkyk [YouTube URL / arXiv link / content URL]
```

**Output:**
```
workspace/blog/
├── YYYY-MM-DD_mokslius_[tema]_palanga.md  → Prie alaus 🍺 (archyvas)
└── YYYY-MM-DD_oldboy_[tema]_palanga.md    → Blog publikacija
```

**Mokslius charakteristikos:**
- Chronologinė struktūra su timestamps
- Techniniai terminai lietuviškai
- Implementacijos detalės
- Akademinis rigor
- Performance metrics
- Point-in-time tikslumas

**OldBoy charakteristikos:**
- Pradžia: "Sėdžiu Palangoje, pušys kvepia, jūra ošia..."
- Storytelling su atmosfera
- Metaforos ir dialogo išsaugojimas
- Blockquotes brilliant statements
- Maksimalizmas (never save words)
- Insights ir pastebėjimai

---

### Veiksmas-2: Suskaldymas (Optional - Teminė Ekstraktacija)

**Kai naudoti:**
- Kai OldBoy failas apima **kelias temas**
- Kai reikia **cross-category** content
- Kai kuriamas teminių ištraukų archyvas

**Process:**
1. Paimti pilną OldBoy failą iš `workspace/blog/`
2. Išskirti **atskiras temas/insights**
3. Sukurti temines ištraukas
4. Dėti į `workspace/oldboy/[KATEGORIJA]/`

**Pavyzdys:**
```
workspace/blog/2026-02-08_oldboy_congress_trading_palanga.md
    ↓ (suskaldomas)
workspace/oldboy/
├── AI_Valdymas/2026-02-08_congress_ai_oversight.md      (AI priežiūros aspektas)
├── Karjera/2026-02-08_congress_career_ethics.md         (etika karjeroje)
└── Tendencijos/2026-02-08_congress_society_impact.md    (visuomenės įtaka)
```

**Lankstumas:**
- Viena tema → kelios kategorijos ✅
- Nauja kategorija → naujas folderis ✅

---

## 📁 Katalogų Struktūra

### workspace/blog/ (Pirminės Analizės)

**Paskirtis:** Pilni, nesuskaldyti failai po Veiksmo-1

**Turinys:**
- Mokslius failai (techninė analizė, asmeninis archyvas)
- OldBoy failai (pilna naratyvinė analizė)

**Kategorija:** Nustatoma iš YAML frontmatter tags

**Pavyzdžiai:**
```yaml
tags:
  - Vibe_Coding
  - AI_Tools
→ Category: Tech

tags:
  - Graph_Learning
  - AI_Governance
→ Category: AI Valdymas

tags:
  - Career
  - Ethics
→ Category: Karjera
```

### workspace/oldboy/ (Teminės Ištraukos)

**Paskirtis:** Suskaldytos temos iš OldBoy failų (po Veiksmo-2)

**Kategorijos (esamos):**
- `Technologijos/` → Blog: "Tech"
- `Tendencijos/` → Blog: "Tendencijos"
- `Karjera/` → Blog: "Karjera"
- `Filozofija/` → Blog: "Filosofija"
- `AI_Valdymas/` → Blog: "AI Valdymas"
- `Agentai/` → Blog: "Agentai"
- `Prompt_Engineering/` → Blog: "Tech"

**Naujos kategorijos (dinamiškai):**
- `Medicina/` → Blog: "Medicina"
- `Menas/` → Blog: "Menas"
- `Švietimas/` → Blog: "Švietimas"
- `[BET_KAS]/` → Blog: "[BET_KAS]"

**Taisyklė:** Bet koks folderio pavadinimas tampa Blog kategorija

---

## 🚀 Blog Publikavimas

### Komanda

```bash
cd agent-network
node upload_palanga_post.js "[failo_kelias]"
```

### Keliai

**Option 1: Pilnas straipsnis iš blog/**
```bash
node upload_palanga_post.js "d:\_PAL\benino\workspace\blog\2026-02-08_oldboy_vibe_coding_palanga.md"
```
- Kategorija: iš YAML tags
- Turinys: pilnas straipsnis

**Option 2: Teminė ištrauka iš oldboy/[TEMA]/**
```bash
node upload_palanga_post.js "d:\_PAL\benino\workspace\oldboy\Karjera\2026-02-08_career_ethics.md"
```
- Kategorija: iš folder pavadinimo
- Turinys: teminė ištrauka

### Automatika

**Script atlieka:**
1. ✅ Tikrina ar `_mokslius_` → praleisti (ne blog)
2. ✅ Nustato kategoriją:
   - `workspace/blog/` → iš YAML tags
   - `workspace/oldboy/[TEMA]/` → iš folder
3. ✅ Konvertuoja Markdown → Clean HTML (Quill compatible)
4. ✅ Prideda:
   - Šaltinį (viršuje dešinėje, italic)
   - Cover image
   - Interactive tag buttons
   - Palanga footer
5. ✅ Įkelia į Supabase `blog_posts` table

---

## 🏷️ YAML Frontmatter Formatas

### Mokslius Failas

```yaml
---
tags:
  - Graph_Learning
  - Temporal_Networks
  - Congressional_Trading
  - AI_Governance
  - Mokslius_Protocol
date: 2026-02-08
author: Mokslius Protocol
source: https://arxiv.org/abs/2602.05514
paper_title: Detecting Information Channels in Congressional Trading
authors: Name1, Name2, Name3
submitted: 2026-02-05
category: cs.CE
---
```

### OldBoy Failas

```yaml
---
tags:
  - AI_Governance
  - Congressional_Trading
  - Graph_Networks
  - Palanga_Edition
  - OldBoy_Extracts
date: 2026-02-08
author: OldBoy Alchemist
source: https://arxiv.org/abs/2602.05514
paper_title: Detecting Information Channels in Congressional Trading
authors: Name1, Name2, Name3
submitted: 2026-02-05
---
```

---

## 📊 Category Mapping Logic

### Tag → Category (workspace/blog/)

```javascript
// Upload script checks YAML tags
if (frontmatter.includes('Vibe_Coding') || frontmatter.includes('AI_Tools')) {
    category = 'Tech';
} else if (frontmatter.includes('Graph_Learning') || frontmatter.includes('AI_Governance')) {
    category = 'AI Valdymas';
} else if (frontmatter.includes('Career') || frontmatter.includes('Karjera')) {
    category = 'Karjera';
} else if (frontmatter.includes('Philosophy') || frontmatter.includes('Filozofija')) {
    category = 'Filosofija';
} else {
    category = 'Tendencijos'; // Default
}
```

### Folder → Category (workspace/oldboy/)

```javascript
const categoryMap = {
    'Technologijos': 'Tech',
    'Tendencijos': 'Tendencijos',
    'Filozofija': 'Filosofija',
    'Karjera': 'Karjera',
    'AI_Valdymas': 'AI Valdymas',
    'Agentai': 'Agentai',
    'Prompt_Engineering': 'Tech',
    // Naujos kategorijos
    'Medicina': 'Medicina',
    'Menas': 'Menas',
    'Švietimas': 'Švietimas'
};

// If not in map, use folder name
category = categoryMap[folderName] || folderName;
```

**Lankstumas:** Bet koks naujas folderis tampa kategorija automatiškai.

---

## 🎯 Use Cases

### Case 1: YouTube Video → Blog

**Workflow:**
```
1. "sutvarkyk https://youtube.com/watch?v=xxx"
   → Generates: workspace/blog/2026-XX-XX_oldboy_xxx.md

2. cd agent-network
   node upload_palanga_post.js "workspace/blog/2026-XX-XX_oldboy_xxx.md"
   → Published to blog with auto-detected category
```

### Case 2: arXiv Paper → Multiple Themes

**Workflow:**
```
1. "sutvarkyk https://arxiv.org/abs/xxxx.xxxxx"
   → Generates:
     - workspace/blog/2026-XX-XX_mokslius_paper.md (prie alaus)
     - workspace/blog/2026-XX-XX_oldboy_paper.md (pilnas)

2. Manual suskaldymas:
   workspace/blog/2026-XX-XX_oldboy_paper.md
   → Extract themes:
      - workspace/oldboy/AI_Valdymas/2026-XX-XX_theme1.md
      - workspace/oldboy/Karjera/2026-XX-XX_theme2.md
      - workspace/oldboy/Tendencijos/2026-XX-XX_theme3.md

3. Publish each theme:
   node upload_palanga_post.js "workspace/oldboy/AI_Valdymas/2026-XX-XX_theme1.md"
   node upload_palanga_post.js "workspace/oldboy/Karjera/2026-XX-XX_theme2.md"
   node upload_palanga_post.js "workspace/oldboy/Tendencijos/2026-XX-XX_theme3.md"
```

### Case 3: Naujos Kategorijos Kūrimas

**Scenario:** Straipsnis apie medicinines AI aplikacijas

**Workflow:**
```
1. "sutvarkyk [medical AI article]"
   → workspace/blog/2026-XX-XX_oldboy_medical_ai.md

2. Sukurti naują kategoriją:
   mkdir workspace/oldboy/Medicina

3. Extract tema:
   → workspace/oldboy/Medicina/2026-XX-XX_ai_diagnostics.md

4. Publish:
   node upload_palanga_post.js "workspace/oldboy/Medicina/2026-XX-XX_ai_diagnostics.md"
   → Category: "Medicina" (naujas)
```

---

## 🛠️ Technical Details

### Upload Script Features

**1. Mokslius Filter:**
```javascript
if (fullPath.includes('_mokslius_')) {
    console.log('ℹ️  Mokslius failas - praleistas');
    process.exit(0);
}
```

**2. Path Detection:**
```javascript
if (fullPath.includes('workspace/blog/')) {
    // Full article - category from tags
} else {
    // Theme extract - category from folder
}
```

**3. Markdown → Clean HTML:**
- Quill editor compatible
- No complex inline styles
- Semantic tags: `<h2>`, `<p>`, `<ul>`, `<strong>`, `<em>`
- Blockquotes preserved
- Links target="_blank"

**4. Interactive Elements:**
- Source link (top right, italic)
- Tag buttons (navigate to tag search)
- Palanga footer signature

**5. Clean Excerpt:**
- Strips markdown syntax
- Removes images/links
- First 160 chars
- No formatting artifacts

---

## ✅ Success Criteria

**Veiksmas-1 Success:**
- [ ] 2 failai sukurti (`workspace/blog/`)
- [ ] Mokslius: techninė analizė su timestamps
- [ ] OldBoy: "Sėdžiu Palangoje..." pradžia
- [ ] YAML frontmatter complete
- [ ] Cover image link valid

**Veiksmas-2 Success:**
- [ ] Temos išskirtos logiškai
- [ ] Kiekviena tema - atskiras failas
- [ ] Tinkamose kategorijose
- [ ] Cross-category jei reikia

**Blog Upload Success:**
- [ ] Clean HTML formatavimas
- [ ] Šaltinis viršuje dešinėje
- [ ] Tagai filtruoja search
- [ ] Excerpt be markdown syntax
- [ ] Quill editor compatible (editable)

---

## 🎓 Filosofija

**Palanga principas:** Laikas ir erdvė reflekcijai

- Maksimalizmas virš minimalizmo
- Storytelling virš bulletpoints
- Context virš abstractions
- Insight virš information

**Workflow principas:** Lankstumas

- Nėra griežtų kategorijų
- Nėra vieno "teisingo" būdo
- Tema gali būti keliose vietose
- Naujos kategorijos sukuriamos pagal poreikį

---

## 📝 Maintenance Notes

**Category Map Updates:**
Kai kuriamos naujos kategorijos dažnai, pridėti į `categoryMap` (`upload_palanga_post.js`)

**Tag → Category Rules:**
Kai naujų tag'ų daugėja, atnaujinti frontmatter parsing logic

**Folder Cleanup:**
Periodiškai peržiūrėti `workspace/oldboy/` - seni/netinkami folderiai

---

**OldBoy 🤞**
*Palanga edition v2.0*
