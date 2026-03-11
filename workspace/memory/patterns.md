# Darbo Modeliai (Patterns)

> Optimalūs workflow'ai, rasti per praktiką.
> Formatas: `### [Pattern pavadinimas]` → Kada naudoti → Veiksmai → Kodėl taip

---

### URL → Blog Post Pipeline

**Kada naudoti:** Herbertas siunčia URL su prašymu analizuoti / publikuoti
**Veiksmai:**
```bash
exec(command="node d:/_PAL/benino/agent-network/sutvarkyk.js [URL]", timeout=120)
```
1. Palaukti ~27s
2. Patikrinti rezultatą: `http://localhost:3000/user/@OldBoy-RSS`
3. Pranešti Herbertui apie sukurtus postus (Mokslius + OldBoy + temos)
**Kodėl taip:** `sutvarkyk.js` vienu paleidymu daro: analizę + 2 straipsnius + 2-5 temas → 4 blog postai
**Pastaba:** Jei serveris neveikia → `cd agent-network && npm start` pirmiau

---

### Modelio Keitimas

**Kada naudoti:** LLM klaidos, lėtumas, arba Herbertas prašo pakeisti
**Veiksmai:**
1. `read_file("C:/Users/Herba/.nanobot/config.json")`
2. Pakeisti `agents.defaults.model` → pilnas pavadinimas (pvz. `groq/llama-3.3-70b-versatile`)
3. Stop gateway
4. Jei session poisoning → ištrinti `C:\Users\Herba\.nanobot\sessions\`
5. Restart: bridge → gateway
**Kodėl taip:** Config tik startup metu nuskaitomas, alias (be prefix) neveikia

---

### Agent-Network Git Workflow

**Kada naudoti:** Po bet kokių pakeitimų agent-network/
**Veiksmai:**
```bash
cd d:/_PAL/benino/agent-network
git add [failai]
git commit -m "type: aprašymas"
git push origin main
```
**Kodėl taip:** agent-network = atskiras submodule, push reikalingas Vercel deploy
**Prevencija:** NIEKADA necommitinti iš benino/ root — tik iš agent-network/

---

### Konteksto Atkūrimas Po Compaction

**Kada naudoti:** Agentas "pamiršo" kontekstą arba po cold start
**Veiksmai:**
1. `read_file("workspace/memory/handoff.md")` — paskutinis save-game
2. `read_file("workspace/memory/YYYY-MM-DD.md")` — šiandienos darbas
3. `read_file("workspace/memory/MEMORY.md")` — kritiniai faktai
4. Jei projektas vyksta → `read_file("workspace/memory/projects-log.md")`
5. Pranešti Herbertui: "🤞 Kontekstas atkurtas. [Santrauka]."
**Kodėl taip:** Handoff.md = 95% konteksto atkūrimas (be jo → 30-50% praradimas)

---

### Naujų Skills Kūrimas

**Kada naudoti:** Herbertas prašo automatizuoti pasikartojantį darbą
**Veiksmai:**
1. Paklausk 2-3 konkrečius vartojimo pavyzdžius
2. Nuspręsk tipą: Workflow / Role-Based / Data-Driven / Hybrid
3. Sukurk `workspace/skills/{vardas}/SKILL.md` su YAML frontmatter
4. Testuok su realiu pavyzdžiu
5. Atnaujink AGENTS.md maršrutizavimo lentelę
6. Įrašyk į `memory/projects-log.md`
**Kodėl taip:** Skill be pavyzdžių → neveikia po compaction
