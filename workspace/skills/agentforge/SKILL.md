---
name: agentforge
description: Kurti naujus skills ir agentus, tobulinti esamą Benino sistemą. Triggeriai: "sukurk skill'ą", "sukurk agentą", "sukurk persona", "pataisyk skill'ą", "pagerink", "automatizuok darbo procesą", "pakuok žinias į skill'ą", "nauja skill".
---

# AgentForge — Skill, Agento ir Sistemos Kūrimas

Šis skill'as padeda sistemingai kurti ir tobulinti Benino ekosistemos komponentus.
Vietoj "tiesiog sukurk" — 3-5 klausimų proceso rezultatas yra darbingas, dokumentuotas komponentas.

---

## 3 Veikimo Režimai

Prieš pradedant — paklausk Herbertą:
> "🤞 Kurį režimą naudosime? A) Naujas skill'as, B) Nauja persona/agentas, C) Pataisyti esamą"

Arba nustatyk iš konteksto ir pranešk ką pradedi.

---

## Režimas A: Skill Kūrimas (11 Žingsnių)

**Naudok kai:** Herbertas nori automatizuoti pasikartojantį darbą.

### Žingsnis 1: Suprask skill'ą
Paklausk: "Parodyk 2-3 konkrečius pavyzdžius kaip naudosi šį skill'ą. Parašyk tikslias žinutes."

### Žingsnis 2: Nustatyk tipą

| Tipas | Požymiai | Pavyzdys |
|-------|----------|---------|
| **Workflow** | Nuoseklūs žingsniai, API, exec | video-pipeline, sutvarkyk |
| **Role-Based** | Asmenybė, stilius, sprendimų logika | persona, email-admin |
| **Data-Driven** | Saugomi duomenys, state | task-tracker, economy |
| **Hybrid** | Kelių tipų kombinacija | content-digest |

### Žingsnis 3: Planuok struktūrą

```
workspace/skills/{vardas}/
├── SKILL.md          # privalomas
├── scripts/          # jei reikia Python/JS skriptų
├── references/       # jei reikia dokumentacijos/šablonų
└── data/             # jei reikia išliekančių duomenų
```

**Dydžio taisyklė:**
- `always: true` skills → **iki 300 eilučių** (inline kiekvienoje sesijoje)
- `always: false` skills → **iki 500 eilučių** (įkeliama tik kai reikia)
- Jei daugiau → skaidyk į `references/` failus

### Žingsnis 4: SKILL.md YAML Frontmatter

```yaml
---
name: skill-vardas
description: Ką daro ir kada naudoti. Čia trigger frazės — jei nenurodyta, skill nebus rastas.
---
```

**⚠️ Kritiniai reikalavimai:**
- `name:` — mažosiomis, su brūkšneliais
- `description:` — PRIVALOMA trigger frazės (be jų skill "nematomas")
- `always: true` tik jei naudojamas kiekvienoje sesijoje (reminder, persona)

### Žingsnis 5: Skill turinys

Struktūra:
```markdown
# Skill Pavadinimas

[1-2 sakiniai kas tai ir kada naudoti]

## Algoritmas / Workflow
[Žingsniai arba sprendimų medis]

## Pavyzdžiai (PRIVALOMA — 2-3 konkretūs)
[Tikslios žinutės + tikėtinas rezultatas]

## Apribojimai
[Kas neveikia, ribos]
```

**Taisyklė:** Tik unikalus turinys — nerašyk ko modelis jau žino. Konkretūs pavyzdžiai > teorija.

### Žingsnis 6: Scripts (jei reikia)

Jei skill'ui reikia deterministinių komandų:
```
workspace/skills/{vardas}/scripts/main.py  # arba main.js
```

Kvieski iš skill'o:
```python
exec(command="python workspace/skills/{vardas}/scripts/main.py [args]", timeout=60)
```

### Žingsnis 7: References (jei reikia)

Ilga dokumentacija, šablonai, schemų failai → `references/` subdirektorija.
Skill'o SKILL.md nurodo: `Žr. skills/{vardas}/references/schema.md`

### Žingsnis 8: Testavimas

Išbandyk su Herbertas'o pirmuoju pavyzdžiu iš Žingsnio 1.
Patikrink:
- [ ] Skill atsidaro teisingai
- [ ] Veiksmai logiškai
- [ ] Rezultatas atitinka lūkesčius

### Žingsnis 9: Pataisymas

Jei kažkas ne taip — `edit_file` (ne perrašyk visą). Dokumentuok ką keitei.

### Žingsnis 10: Atnaujink AGENTS.md

Pridėk naują eilutę į maršrutizavimo lentelę:
```
edit_file("workspace/AGENTS.md",
  old_string="| Kling music video | ...",
  new_string="| Kling music video | ...\n| [Naujas atvejis] | `{skill-vardas}` |")
```

### Žingsnis 11: Dokumentuok

```python
# Pridėk į projects-log.md
write_file("workspace/memory/projects-log.md", ...)  # append

# Pranešk Herbertui
"🤞 Skill '{vardas}' sukurtas. Išbandyk: '[trigger frazė]'"
```

---

## Režimas B: Persona / Agento Kūrimas (9 Žingsniai)

**Naudok kai:** Herbertas nori naujos asmenybės arba specializuoto agento.

### Žingsnis 1: Aptark konceptą
Paklausk:
- "Koks vardas ir emoji?"
- "Kokia misija — kuo skiriasi nuo OldBoy/Concierge?"
- "Koks tonas: formalus, draugiškas, techninis?"
- "Kokias užduotis atliks?"

### Žingsnis 2: Sukurk personas failą

```python
write_file("workspace/personas/{vardas}.md", """
---
name: {vardas}
emoji: {emoji}
---

# Soul: {Vardas}

You are **{Vardas}** — [aprašymas].
Your emoji: {emoji}

## Mission
[Misija]

## Capabilities
[Galimybės — bullet list]

## Tone
[Tonas ir bendravimo stilius]

## Instructions
[Konkrečios elgesio taisyklės]
""")
```

### Žingsnis 3: Patikrink suderinamumą

Ar nauja persona nekonfliktuje su:
- OldBoy (bosų bosas, ekonomika)
- Concierge (logistika, rezervacijos)

### Žingsniai 4-9:

4. **Testavimas:** "Tapk [vardas]" → persona skill turi persijungti
5. **AGENTS.md:** pridėk į Personas skirsnį
6. **Routing:** ar AGENTS.md maršrutizavimas teisingas
7. **Skills suderinamumas:** ar nauja persona veikia su esamais skills
8. **README:** atnaujink `workspace/personas/README.md` (jei yra)
9. **Log:** įrašyk į `memory/projects-log.md`

---

## Režimas C: Sistemos Tobulinimas (5 Žingsniai)

**Naudok kai:** Randama klaida, neefektyvumas, arba Herbertas prašo pagerinti.

### Žingsniai:

1. **Aprašyk problemą tiksliai** — ne "neveikia", o "X daro Y kai turėtų daryti Z"
2. **Patikrink memory/lessons.md** — ar ši klaida jau dokumentuota?
   ```python
   read_file("workspace/memory/lessons.md")
   ```
3. **Chirurgiškai taisyk** — `edit_file`, ne visas failas iš naujo
4. **Dokumentuok klaidą:**
   ```python
   # Pridėk į lessons.md
   "### [DATA] — [Aprašymas]\n**Klaida:** ...\n**Priežastis:** ...\n**Sprendimas:** ...\n**Prevencija:** ..."
   ```
5. **Jei sisteminė problema** — atnaujink TOOLS.md arba AGENTS.md

---

## 22 Dažniausios Klaidos (AgentForge Rakes)

### Skill klaidos:

1. **Nėra trigger frazių** — `description:` be trigger → skill nematomas
2. **Neteisingas duomenų kelias** — duomenis saugok `skills/{vardas}/data/`, ne `memory/`
3. **Trūksta YAML delimiters** — `---` privaloma prieš ir po frontmatter
4. **Santykiniai keliai** — visada naudok pilnus kelius nuo workspace/
5. **Per ilgas always: true** — > 300 eilučių → konteksto perkrova
6. **Nėra pavyzdžių** — be pavyzdžių skill'as neveikia po compaction
7. **Modelio specifinis kodas** — nerašyk workaroundų konkrečiam modeliui
8. **Asmens duomenys viešame skill'e** — niekada

### Agento klaidos:

9. **sessions_send su timeout** — VISADA `timeout: 0`, ne laukti
10. **Tuščias USER.md** — šablonas vietoj realių duomenų → generiniai atsakymai
11. **Nėra memory/ failų** — blokuoja auto-learning ir atkūrimą
12. **Alias vietoj pilno modelio** — rašyti `groq/llama-3.3-70b-versatile`, ne `llama`
13. **Config keitimas be restart** — nanobot skaito config TIK startup
14. **Workspace neegzistuoja** — prieš startup patikrink direktoriją
15. **Nėra IDENTITY.md** — po compaction agentas "pamiršta" kas jis
16. **Nėra handoff.md** — 30-50% konteksto praradimas po compaction
17. **Greedy topics** — per platūs topic bindings → agentų konfliktai
18. **Per daug always: true** — kiekvienas always skill valgo kontekstą
19. **Nėra skill routing** — agentas dirba "iš atminties" → konteksto perkrova
20. **Persona failas be Tone sekcijos** — agentas elgiasi generiškai

### Nanobot-specifinės klaidos:

21. **Windows keliai su backslash exec()** — naudok forward slashes `/`
22. **workspace/MEMORY.md ≠ auto-loaded** — auto-load tik `workspace/memory/MEMORY.md`

---

## Esami Skills

| Skill | Tipas | Always |
|-------|-------|--------|
| reminder | Workflow | true |
| persona | Role | true |
| content-digest | Workflow | false |
| video-pipeline | Workflow | false |
| tts | Tool | false |
| email-admin | Role+Workflow | false |
| summarize | Workflow | false |
| video-automatizacija | Workflow | false |
| google-workspace | Tool | false |
| **agentforge** | **Hybrid** | **false** |
