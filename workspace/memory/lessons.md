# Pamokos iš Klaidų

> Čia saugomi patikrini sprendimai. Prieš debugginant — perskaityk.
> Formato taisyklė: `### [DATA] — [Trumpas aprašymas]`

---

### 2026-03-10 — v0.1.4 allowFrom: [] dabar blokuoja visus

**Klaida:** Gateway paleidžiamas bet WhatsApp neveikia — `"whatsapp" has empty allowFrom (denies all)`
**Priežastis:** v0.1.4 breaking change — tuščias `allowFrom: []` = "blokuoti visus" (anksčiau = "leisti visiems")
**Sprendimas:** `config.json` → `channels.whatsapp.allowFrom: ["*"]` arba konkretūs numeriai
**Prevencija:** Po kiekvieno nanobot update patikrinti ar WhatsApp veikia iš karto

---

### 2026-03-10 — always: false string bug → per didelis system prompt

**Klaida:** TPM rate limit exceeded — system prompt 8,515 tokenų (turėjo būti ~4,000)
**Priežastis:** Nanobot YAML parser grąžina `always: false` kaip **string `"false"`** — Python `if "false"` = `True`! Todėl VISI skills su `always: false` frontmatter buvo loaded pilnai kiekvienai žinutei
**Sprendimas:** Pašalinti `always: false` eilutę iš skills frontmatter (tuščia = neloaded). Palikti tik `always: true` kai tikrai reikia
**Prevencija:** Nanobot skills: NIEKADA nerašyti `always: false`. Tik `always: true` arba eilutę praleisti

---

### 2026-02-10 — Windows emoji crash nanobot paleidžiant

**Klaida:** `UnicodeEncodeError: 'charmap' codec can't encode character` — Rich console krenta su cp1252
**Priežastis:** Windows terminalo encoding cp1252 negali apdoroti emoji
**Sprendimas:**
```bash
NO_COLOR=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python -m nanobot gateway
```
**Prevencija:** Visada naudok šiuos tris env vars paleidžiant gateway Windows aplinkoje

---

### 2026-02-10 — Session poisoning po modelio keitimo

**Klaida:** LLM kartoja tas pačias klaidas net po to, kai pakeistas modelis
**Priežastis:** Senos klaidos liko sesijos istorijoje → LLM "pasimoką" iš jų kartoti
**Sprendimas:**
1. Stop gateway
2. Ištrink sesijos failą: `C:\Users\Herba\.nanobot\sessions\`
3. Restart bridge → gateway
**Prevencija:** Jei klaida kartojasi daugiau nei 2 kartus → pirma patikrink sesiją

---

### 2026-02-10 — Config keitimas be restart

**Klaida:** Modelio pakeitimas config.json neturi efekto
**Priežastis:** Nanobot config nuskaitomas TIK startup metu
**Sprendimas:** Visada restart gateway po config.json keitimo
**Prevencija:** Prisimink: config → restart → testuok

---

### 2026-03-10 — workspace/MEMORY.md ≠ auto-loaded

**Klaida:** `workspace/MEMORY.md` (root lygyje) nėra automatiškai įkeliamas nanobot
**Tiesa:** Nanobot auto-loads tik `workspace/memory/MEMORY.md` (memory/ subdirektoriją)
**Prevencija:** Ilgalaikę atmintį rašyk į `workspace/memory/MEMORY.md`, ne workspace šaknyje
