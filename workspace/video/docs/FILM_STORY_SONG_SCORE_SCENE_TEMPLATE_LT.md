# Filmo sablonas: Story -> Song -> Score -> Scene

Data: 2026-02-13
Statusas: darbinis sablonas (ne klipinis)

## 0. Ka duodi kaip ivesti

- Apsakymo tekstas (pilnas arba sutrumpintas).
- Norimas filmo ilgis (pvz. 8 min, 22 min, 90 min).
- Tonas ir zanras (pvz. neo-noir, sci-fi drama, absurdas).
- Auditorija (festivalis, YouTube, social, kino sales cut).
- Gamybos ribos (Kling-only / mix / live).

## 1. STORY (dramaturgijos branduolys)

Tikslas: is apsakymo padaryti aisku kino karkasa.

### 1.1 Isgryninimas

- Tema (1 sakinys).
- Logline (1-2 sakiniai).
- Herojaus trukumas (vidinis konfliktas).
- Isorinis tikslas.
- Stakes (ka praranda, jei nepavyks).

### 1.2 Struktura

- 3 veiksmu planas:
  - Act I: setup + inciting incident.
  - Act II: eskalacija + midpoint + krizinis taskas.
  - Act III: kulminacija + pasekme.
- Beat sheet (8-15 pagrindiniu beatu su laiku).

### 1.3 Personaazai

- Min 5 veikejai:
  - vardas, funkcija istorijoje, noras, baime, vizualinis kodas.
- Santykiu schema (kas su kuo konfliktuoja, kas ka slepia).

## 2. SONG (dainos sluoksnis, jei filme yra daina)

Tikslas: dainos zodziai ir forma turi tarnauti istorijai, o ne atvirksciai.

### 2.1 Dainos paskirtis filme

- Kur daina atsiranda:
  - opening, midpoint, montage, finale, end credits.
- Ar daina yra:
  - diegetic (veikejai girdi),
  - non-diegetic (tik ziurovui).

### 2.2 Lyrikos struktura

- Forma:
  - Intro
  - Posmelis I
  - Priedainis
  - Posmelis II
  - Bridge / Solo
  - Final priedainis / Outro
- Kiekvienai daliai:
  - emocinis tikslas,
  - vaizdiniai simboliai,
- draudziamos klises.

### 2.3 Lyrikos kokybes patikra

- Ar zodziai turi konkretu veiksma/objekta, ne tik abstrakcija.
- Ar frazes dainuojamos (ritmiskai telpa).
- Ar daina nekeicia veikeju logikos.

## 3. SCORE (muzikos dramaturgija)

Tikslas: muzika valdo tempo pojuti ir scenu perejimus.

### 3.1 Muzikinis zemelapis

- BPM intervalai pagal scenas.
- Tonacija/motyvas kiekvienam pagrindiniam veikejui.
- Instrumentu sluoksniai:
  - pagrindinis motyvas,
  - tekstura/ambience,
  - ritmine atrama,
  - kulminacijos akcentai.

### 3.2 Cue sheet sablonas

Kiekvienam cue:

- `cue_id`
- `time_in` / `time_out`
- scena + beat
- emocija (itampa, kalte, atleidimas ir t. t.)
- garso dizaino pastabos (rain, rail, crowd, room tone)

## 4. SCENE (scenos ir kadruote)

Tikslas: is story ir score gauti filmavimo/generavimo uzduotis.

### 4.1 Scene bible

Kiekvienai scenai:

- `scene_id`
- vieta + paros laikas
- dalyvaujantys veikejai
- scenos tikslas
- konflikto forma
- rezultatas (kas pasikeite)

### 4.2 Shot design

- Kiekvienai scenai 6-20 shotu (pagal filmo formata).
- Shot kortele:
  - `shot_id`
  - trukme
  - kadro tipas (ECU, CU, MCU, MS, WS, EWS, OTS, POV, Dutch, Low)
  - kameros judesys
  - sviesa/spalva
  - veiksmas
  - continuity notes

### 4.3 Kling-ready prompt formatas

Naudoti ta pati karkasa kiekvienam shot:

- Subject
- Location
- Action
- Camera (shot type + movement)
- Lighting + color mood
- Continuity tags (character outfit/prop IDs)
- Negative constraints (no text, no watermark, no logo, no extra fingers)

## 5. Isvesties failai (minimum)

- `story_bible_lt.md`
- `song_lyrics_structured_lt.txt`
- `score_cue_sheet_lt.csv`
- `scene_bible_lt.md`
- `shot_list_kling.json`
- `render_batch_order.md`
- `edit_decision_list.md`

## 6. Vykdymo seka (praktine)

1. Apsakymas -> Story bible.
2. Story bible -> Dainos zodziu draftas.
3. Dainos forma -> Score cue sheet.
4. Story + Score -> Scene bible.
5. Scene bible -> Shot list + Kling promptai.
6. Render batchais (hero shotai pirmi).
7. Assembly/Premiere + garso suvedimas.
8. Final master + social cutai.

## 7. Greitas uzpildomas blankas (copy/paste)

```md
# Projekto pavadinimas

## STORY
- Tema:
- Logline:
- Herojus:
- Trukumas:
- Isorinis tikslas:
- Stakes:

## SONG
- Dainos paskirtis:
- Forma:
- Esminiai ivaizdziai:
- Draudziamos klises:

## SCORE
- BPM planas:
- Motyvai:
- CUE 01:
- CUE 02:

## SCENE
- SC01:
  - Tikslas:
  - Konfliktas:
  - Rezultatas:
- SC02:
  - Tikslas:
  - Konfliktas:
  - Rezultatas:

## SHOT
- SH001:
  - Type:
  - Duration:
  - Prompt:
- SH002:
  - Type:
  - Duration:
  - Prompt:
```
