# Benino Workspace 🦞

Šis katalogas skirtas darbui su Benino botu.

## 📂 Katalogų struktūra:

### `personas/` - Botų Asmenybės 🎭
Failai, apibrėžiantys skirtingus boto vaidmenis:
- `oldboy.md` - Pagrindinis (išmintingas meistras).
- `concierge.md` - Asistentas užduotims.
- Čia galite kurti naujus (pvz., `doctor.md`, `guide.md`).

### `skills/` - Įgūdžiai ⚡
Papildomos funkcijos botui:
- `persona/` - Gebėjimas keisti asmenybę.
- `cron/` - Laiko planavimas.

### `memory/` - Atmintis 🧠
Boto "užrašų knygelė" faktams saugoti:
- `economy.md` - Saulių balansas ir transakcijos.
- `contacts.md` - Klientų ir savininkų kontaktai.

### `documents/` - Dokumentai analizei
Dėkite čia:
- PDF failus analizei
- Word dokumentus
- Excel lenteles
- Teksto failus

**Pvz.:**
```
documents/
├── sutartis.pdf
├── ataskaita.docx
└── duomenys.csv
```

### `projects/` - Projektai
Benino gali padėti su kodavimu:
- Python projektai
- JavaScript/Node.js
- HTML/CSS
- Bet koks kitas kodas

**Pvz.:**
```
projects/
├── python-scraper/
│   ├── main.py
│   └── requirements.txt
└── website/
    ├── index.html
    └── style.css
```

### `notes/` - Užrašai ir idėjos
- Užrašai .txt ar .md formatu
- TODO sąrašai
- Idėjų brainstorming
- Projektų planai

**Pvz.:**
```
notes/
├── ideas.md
├── todo.txt
└── project-plan.md
```

### `scripts/` - Automatizacijos scriptai
Benino sukurti ar modifikuoti scriptai:
- Python automatizacijos
- Bash scriptai
- PowerShell scriptai

**Pvz.:**
```
scripts/
├── backup.py
├── cleanup.sh
└── report-generator.ps1
```

### `temp/` - Laikini failai
Failai, kurie bus automatiškai išvalomi:
- Test failai
- Eksperimentai
- Downloads

**⚠️ Šis katalogas gali būti išvalytas bet kada!**

---

## 💡 Kaip naudoti:

### 1. Paprasčiausias būdas - tiesiog nukopijuokite failus:
```bash
# Windows Explorer:
Nukopijuokite failus į d:\_PAL\benino\workspace\documents\

# Arba per komandų eilutę:
copy C:\Users\Herba\Downloads\failas.pdf d:\_PAL\benino\workspace\documents\
```

### 2. Per Benino Dashboard:
Ateityje galėsite upload'inti failus tiesiai per Web UI.

### 3. Paprašykite Benino:
```
"Benino, perskaityk failą workspace/documents/sutartis.pdf"
"Išanalizuok CSV failą workspace/documents/duomenys.csv"
"Sukurk Python scriptą workspace/scripts/backup.py"
```

---

## ✅ Kas prieinamas Benino:

Benino **MATO** ir gali:
- ✅ Skaityti visus failus šiame kataloge
- ✅ Kurti naujus failus
- ✅ Redaguoti egzistuojančius
- ✅ Analizuoti duomenis
- ✅ Paleisti kodo failus (Python, JS, etc.)

Benino **NEMATO**:
- ❌ Failų už `d:\_PAL\benino` ribų
- ❌ Jūsų asmeninių dokumentų
- ❌ Kitų diskų (C:\, E:\, etc.)

---

## 🔒 Privatumas:

### .gitignore setup:
Jei norite, kad VISI workspace failai nebūtų push'inami į GitHub:

```gitignore
# Workspace failai (optional)
workspace/documents/*
workspace/temp/*

# Bet leisti notes ir scripts
!workspace/notes/
!workspace/scripts/
```

### Slaptų failų apsauga:
**NIEKADA** nedėkite čia:
- Slaptažodžių
- API raktų (turi būti `.env`)
- Asmeninių nuotraukų
- Konfidencialių dokumentų

---

## 🎯 Pavyzdžiai:

### 1. PDF analizė:
```bash
# Įdėti PDF
copy report.pdf workspace/documents/

# Paklausti Benino:
"Išanalizuok workspace/documents/report.pdf ir sudaryk santrauką"
```

### 2. CSV duomenų analizė:
```bash
# Paklausti:
"Perskaityk workspace/documents/sales.csv ir parašyk Python scriptą analizei"
```

### 3. Kodo generavimas:
```bash
# Paklausti:
"Sukurk Python scriptą workspace/scripts/email-sender.py, kuris siųstų el. laiškus"
```

### 4. Projektų valdymas:
```bash
# Paklausti:
"Sukurk TODO sąrašą workspace/notes/project-tasks.md projektui X"
```

---

## 🗑️ Valymas:

### Išvalyti temp katalogą:
```bash
# Windows
del /q d:\_PAL\benino\workspace\temp\*

# Linux/Mac (Docker viduje)
docker exec openclaw-fresh rm -rf /app/workspace/temp/*
```

### Išvalyti visus failus:
```bash
# ATSARGIAI! Ištrina VISKĄ workspace!
rm -rf workspace/* && mkdir -p workspace/{documents,projects,notes,scripts,temp}
```

---

**Sukurta:** 2026-02-01
**Benino versija:** OpenClaw 2026.1.30
**Status:** ✅ Paruošta naudojimui
