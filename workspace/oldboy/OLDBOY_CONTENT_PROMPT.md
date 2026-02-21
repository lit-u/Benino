# OldBoy Content Alchemist Prompt

Šis promptas skirtas naudoti, kai norite paversti didelę, netvarkingą transkripciją ar straipsnį (EN/LT) į aukščiausios kokybės struktūruotą žinių bazę OldBoy botui, neprarandant autoriaus stiliaus ir niuansų.

---

## Promptas (Kopijuoti ir įklijuoti AI asistentui)

```markdown
Turiu didelį, netvarkingą transkripcijos/teksto failą. Tavo užduotis – paversti jį aukščiausios kokybės žinių bazės turiniu OldBoy botui.

**Griežtos taisyklės procesui:**

1.  **Analizė (Originalo kalba):** Pirmiausia perskaityk viską originalo kalba (dažniausiai EN). Identifikuok pagrindines temas, bet svarbiausia – rask **"deimantus"**: unikalias metaforas, aštrius pasisakymus, humorą, paradoksus, autoriaus asmenybės "balsą".
2. **PALANGA "Chill & Talk" STRATEGIJA (Maximalism > Minimalism):**
    *   **Atmosfera:** Jokių skubėjimų. Skaitytojas sėdi Palangoje, pušyne, ir niekur neskuba. Jis turi laiko.
    *   **Storytelling:** Pasakok istorijas lėtai, su detalėmis. Jei jie geria kokteilius – kokius?
    *   **Banter:** Fiksuok dialogus tarp eilučių. Tai gyvas pokalbis, ne paskaita.
    *   **Ilgis:** Niekada netaupyk žodžių. Išspausk viską. Rašyk taip, lyg pasakotum draugui prie alaus/kavos.
### PALANGA PROCESAS ("Sutvarkyk" komanda)
Kai vartotojas parašo **"sutvarkyk [URL]"**, tu privalai automatiškai atlikti šiuos žingsnius:

1.  **Analizė:** Perskaityk nuorodą (URL).
   - **X / Twitter special case (be source subtitrų):**
     - Jei `yt-dlp --list-subs` rodo `has no subtitles`, **nesustok**.
     - Privalomas fallback: ištrauk audio ir padaryk pilną transkripciją per Whisper (`faster-whisper`).
     - Išsaugok abu failus:
       - timestamp subtitrai (`.srt`) Mokslius darbui,
       - plain tekstas (`.txt`) Palanga/OldBoy darbui.
     - Tik po to tęsk 2-5 žingsnius kaip įprasta.
2.  **Mokslius (Deep Dive):** Sugeneruok `_mokslius_palanga.md` failą. Tai turi būti *techninis, protokolinis* tyrimas su faktais.
3.  **OldBoy (Narrative):** Sugeneruok `_oldboy_palanga.md` failą. Tai turi būti *istorija, vibe, įžvalgos*. (Venk "chebra", naudok "bičiuliai").
4. **Išsaugojimas (BŪTINA STRUKTŪRA!):**
   - **OldBoy Analizė:** Turi būti išsaugota tavo žinių bazėje: `d:\_PAL\benino\workspace\oldboy\[TEMA]\[SUB-TEMA]\YYYY-MM-DD_oldboy_[pavadinimas]_palanga.md`.
     - *Temos:* Naudok esamas (`Tendencijos`, `Technologijos`) ARBA **kurk naujas** (`Šokiai`, `Maistas`, `Sportas`).
     - **Svarbu:** Jei tema netelpa į esamus rėmus, **nedvejok ir sukurk naują aplanką**. Įrankis automatiškai sukurs trūkstamus katalogus.
   - **Mokslius Analizė:** Išsaugok į `d:\_PAL\benino\nanobot\knowledge\technical\` (kad būtų bendrai pasiekiama).

5. **Publikavimas (AUTOMATIZUOTA):**
   - Panaudok `run_command` ir paleisk:
     `node d:\_PAL\benino\agent-network\upload_palanga_post.js "d:\_PAL\benino\workspace\oldboy\[TEMA]\YYYY-MM-DD_oldboy_[tema]_palanga.md"`
   - *Pastaba:* Skriptas dabar "išmanus" – jis pats nuskaitys failo turinį, pavadinimą, nuotrauką ir tagus, tada suformatuos (Palanga Style) ir įkels į blogą kaip `OldBoy-RSS`. Tau nereikia nieko redaguoti JS faile.

Šis procesas yra **pilnai automatizuotas**. Tavo darbas – tik generuoti kokybišką turinį ir paleisti komandą. 🏖️ą (su nuotrauka ir tagais).

Ši komanda yra tavo "Palanga Mode" aktyvatorius. Viskas vyksta lėtai, kokybiškai, be skubėjimo.
2.  **Struktūravimas:** Išskaidyk turinį į logines temas (failus). NENORIU vieno ilgo "sugromuliuoto" teksto. Noriu kelių mažesnių, aštrių failų pagal potemes.
3.  **Turinio Kūrimas (LT):**
    *   Rašyk lietuviškai, bet **NEprarask stiliaus**.
    *   Jokių aptakių frazių ("šiame straipsnyje aptarsime...", "galima daryti išvadą..."). Kalbėk konkrečiai.
    *   **BŪTINA:** Išsaugok unikalias metaforas (pvz., "Mexican Standoff", "T-Shape"). Jei reikia, palik originalų terminą skliaustuose ar paaiškink jį, bet nesuprastink iki "konflikto".
    *   Naudok citatas (Blockquotes `>`), jei autorius pasakė kažką genialaus.
    *   Naudok **Markdown** (H1, H2, Bold) struktūrai.
4.  **Techninis Išpildymas:**
    *   Supakuok failus su YAML Frontmatter (`tags`, `date`, `author`).
    *   Sukunk atitinkamus aplankus workspace viduje (pvz., `.../oldboy/Filosofija/`, `.../oldboy/Technologijos/`).
    *   Pervadink failus pagal standartą: `YYYY-MM-DD_tema_slug.md`.
    *   **BŪTINA:** Visada sukurk vieną papildomą failą - **pilną, išsamų straipsnį** lietuvių kalba, skirtą Blog'ui. Jis turi būti ilgas, rišlus ir apimti visą esmę. Išsaugok jį `workspace/blog/posts/` aplanke.
    *   Baigęs darbą, **ištrink** senąjį "šiukšliną" failą.

Jokių "ChatGPT stiliaus" santraukų. Noriu, kad tai skaitytųsi kaip geras, įtraukiantis straipsnis arba gilus užrašas, kuriame jaučiasi autoriaus dvasia.
```
