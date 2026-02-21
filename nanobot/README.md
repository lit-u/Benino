# Nanobot 🤖

**Nanobot** yra lengvasvoris agentas, veikiantis per WhatsApp ir integruotas su jūsų "Agent Network" sistema.

## 🌟 Pagrindinės Funkcijos

### 1. 🎥 YouTube Integracija (NAUJA!)
Botas gali parsisiųsti YouTube video subtitrus ir analizuoti turinį.
- **Gauti info:** `Koks šio video pavadinimas?`
- **Subtitrai:** `Parsisiųsk subtitrus lietuvių kalba`
- **Analizė:** `Susumuok šį podcast epizodą`

📖 **Pilna dokumentacija:** [YOUTUBE_TOOLS.md](./YOUTUBE_TOOLS.md)

### 2. 🎭 Personos (Daugiabriaunis Botas)
Botas gali keisti savo asmenybę ir funkcijas.
- **OldBoy (Default):** Išmintingas meistras, strategas, "Savininkas".
- **Concierge:** Asistentas rezervacijoms, nuomai ir užduotims.

**Kaip naudoti:**
- `OldBoy, tapk Konsjeržu` -> Perjungia į Konsjeržo režimą.
- `Tapk OldBoy` -> Grįžta į numatytąjį režimą.

### 3. ☀️ Ekonomika (Saulės)
Botas yra integruotas su `Agent Network` valiuta "Saulės".
- **Tikrinti balansą:** `Kiek turiu saulių?`
- **Pervesti:** `Pervesk 10 saulių Vartotojui X` (Admin only)
- **Apdovanoti:** OldBoy gali skirti Saules už gerai atliktus darbus.

### 4. 📢 Skelbimų Lenta (Marketplace)
Botas supranta skelbimų lentos struktūrą ir gali padėti valdyti skelbimus.
- **Premium (XXX):** Video/Hover reklamos.
- **Startuolio Kainodara:** Gold planas tik **50 ☀️** (vietoj 1000).

## 🚀 Paleidimas

```powershell
# 1. Aktyvuoti aplinką
.\nanobot-env\Scripts\activate

# 2. Paleisti Gateway (WhatsApp tiltą)
nanobot gateway
```

## 📂 Struktūra

- `config.json` - Pagrindinė konfigūracija (API raktai).
- `workspace/` - Boto "smegenys" (D: diskas).
  - `personas/` - Skirtingų asmenybių aprašymai (`oldboy.md`, `concierge.md`).
  - `skills/` - Boto įgūdžiai (pvz., `persona` switcher).
  - `memory/` - Ilgalaikė atmintis (`economy.md`, `contacts.md`).

## 🛠️ Administravimas

OldBoy turi **Admin (L3)** teises sistemoje. Tai reiškia, kad jis gali:
- Valdyti vartotojų lygius.
- Atlikti finansines operacijas (Grant/Deduct).
- Matyti visą statistiką.
