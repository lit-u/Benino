
# STRUKTŪRINĖ ANALIZĖ: THE SHIFT TO SPECIFICATION-FIRST ENGINEERING
**Analitikas:** Mokslius
**Tema:** "Vibe Coding" fenomenas ir inžinerijos transformacija
**Šaltinis:** Nate Jones (OpenAI/Anthropic Case Studies)
**Data:** 2026-02-08

---

## 1. STRUKTŪRINIS LŪŽIS: NUO IMPLEMENTACIJOS PRIE SPECIFIKACIJOS

Mes stebime fundamentalų programinės įrangos inžinerijos paradigmos pokytį, kurį Nate Jones ir kiti analitikai vadina "Vibe Coding", tačiau akademiškai tai tiksliau vadinti **"Specification-First Engineering"**.

### 1.1. Tradicinis modelis (iki 2024 m.)
*   **Vertės kūrimas:** Rašyti sintaksiškai teisingą kodą (Implementation).
*   **Ribojantis veiksnys (Bottleneck):** Žmogaus gebėjimas rašyti ir debugginti sintaksę.
*   **Kaštai:** Aukšti (kiekviena funkcija reikalauja žmogaus valandų).

### 1.2. Naujasis modelis (2025-2026 m.)
*   **Vertės kūrimas:** Formuluoti tikslius reikalavimus ir sistemos architektūrą (Specification).
*   **Naujas Ribojantis veiksnys:** Žmogaus gebėjimas *paaiškinti* sistemą ir *validuoti* rezultatą.
*   **Kaštai:** Artėja prie nulio (Zero Marginal Cost of Creation).

**Įrodymas (Case Study):**
Boris Cherny (Anthropic, Claude Code Lead) viešai pripažino:
> *"I haven't written a line of production code in two months. I orchestrate AI agents to do it."*
Tai rodo, kad net įrankių kūrėjai perėjo į "orkestratoriaus" rolę.

---

## 2. EKONOMINĖS PASEKMĖS: "THE GREAT DECOUPLING"

Sam Altman (OpenAI) komentaras, kad "vienas žmogus dabar gali padaryti dešimties darbą", rodo ne tik efektyvumą, bet ir **atsiejimą (decoupling)**.

### 2.1. Darbo rinkos bifurkacija
Rinka skyla į dvi dalis:
1.  **Orkestratoriai (Architektai):** Tie, kurie supranta sistemas ir gali jas aprašyti. Jų vertė kyla eksponentiškai.
2.  **Sintaksės rašytojai (Code Monkeys):** Jų vertė krenta iki nulio, nes AI generuoja sintaksę greičiau ir pigiau.

### 2.2. Eksperimentavimo kaina
Kai eksperimentavimo kaina tampa nuline, mes pamatysime **"Kambro sprogimą"** (Cambrian Explosion) nišinėje programinėje įrangoje.
*   Anksčiau: Kurti programą "tik sau" neapsimokėjo.
*   Dabar: Kurti programą "tik šiam savaitgaliui" yra visiškai racionalu.

---

## 3. RIZIKOS ANALIZĖ: "THE AI SKILL TRAP"

Nors "Vibe Coding" skamba patraukliai, egzistuoja rimta kognityvinė rizika, kurią būtina paminėti.

### 3.1. Paviršutiniškumo spąstai
Jei inžinieriai nustoja rašyti kodą, ar jie praranda gebėjimą suprasti, kaip sistema veikia "po kapotu"?
*   Tai vadinama **"Cognitive Offloading"**.
*   Ilgainiui galime turėti "architektų" kartą, kuri nesupranta pamatų (atminties valdymo, tinklo protokolų niuansų), nes viską delegavo AI.

### 3.2. Saugumo skylės
Generuotas kodas dažnai veikia, bet gali turėti subtilių saugumo spragų, kurių "Vibe Coderis" (neturintis gilių žinių) nepastebės.
**Validacija tampa svarbesnė už generavimą.**

---

## IŠVADA: KĄ TAI REIŠKIA MUMS?

Tai nėra "pabaiga" programuotojams. Tai yra **evoliucija**.
Jei norime išlikti relavantiški, turime nustoti save vadinti "programuotojais" (Code Writers) ir pradėti vadinti "sistemos architektais" (System Designers).

**Moksliaus Verdiktas:**
"Vibe Coding" yra klaidinantis terminas. Tai nėra "vibe'as", tai yra **griežta inžinerinė disciplina**, kurioje natūrali kalba tampa nauja asemblerio kalba. Kas valdys kalbą, tas valdys sistemą.
