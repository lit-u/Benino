# Proto Prieštaravimai - Variantas A Generation Pack

Data: 2026-02-13
Bazė: "Darvino Triukšmas"
Tikslas: greitas paleidimas į muzikos generatorių + pasiruošimas filminei scenų eigai.

## 1. Target versijos

- `A_radio`: 03:15
- `A_full`: 04:10

## 2. Struktūra su laiku (A_radio 03:15)

- 00:00-00:16 Intro (spoken, tamsi atmosfera)
- 00:16-00:46 Posmelis I
- 00:46-01:13 Priedainis
- 01:13-01:43 Posmelis II
- 01:43-02:06 Bridge
- 02:06-02:44 Final priedainis
- 02:44-03:15 Outro (instrumentinis, ilgas fade)

## 3. Struktūra su laiku (A_full 04:10)

- 00:00-00:24 Intro
- 00:24-01:02 Posmelis I
- 01:02-01:14 Instrumentinis intarpas
- 01:14-01:50 Priedainis
- 01:50-02:28 Posmelis II
- 02:28-02:58 Bridge
- 02:58-03:42 Final priedainis
- 03:42-04:10 Ilgas outro

## 4. Muzikos promptai (3 versijos)

### Prompt 1 - Main (rekomenduojamas startas)

```text
Genre: cinematic trip-hop, industrial art-pop
Tempo: 90 BPM
Key: D minor
Mood: sad, existential, restrained, tense but intimate
Arrangement: sparse kick, deep sub bass, analog synth drones, soft piano fragments, cinematic strings in chorus, long reverb tails
Vocal: male low register, close-mic, spoken-sung hybrid, fragile emotional tone, intentional pauses between lines
Structure: intro spoken, verse, chorus, verse, bridge, final chorus, long instrumental outro
Dynamics: keep verses minimal, widen in choruses, strongest peak at final chorus, then decaying outro
Avoid: rap cadence, trap hi-hat rolls, EDM drops, bright major chords, over-compression
Language: Lithuanian
```

### Prompt 2 - Darker

```text
Genre: dark cinematic trip-hop, industrial ambient pop
Tempo: 88-90 BPM
Key: F minor
Mood: bleak, cold, urban night, psychological pressure
Arrangement: distorted low textures, metallic percussion accents, pulsing bass, dissonant string layers, tape noise
Vocal: intimate, almost whispered in verses, fuller but still sad in chorus
Structure: same as provided timeline, include 6-12s instrumental gaps for breath
Avoid: upbeat groove, funky basslines, cheerful hooks
Language: Lithuanian
```

### Prompt 3 - Cleaner mix

```text
Genre: cinematic art-pop with trip-hop pulse
Tempo: 90 BPM
Key: D minor
Mood: melancholic, reflective, human vs instinct conflict
Arrangement: cleaner drums, defined bass, piano motif, controlled synth pads, moderate strings
Vocal: clear articulation, emotional but not theatrical, preserve spoken phrases in intro and bridge
Mix: vocal upfront, bass controlled, no harsh highs
Avoid: aggressive rap flow, over-saturated distortion, pop-happy chorus harmonies
Language: Lithuanian
```

## 5. Vokalo atlikimo gairės

- Posmeliai: trumpesnės frazės, palikti oro tarp eilučių.
- Priedainis: melodija platesnė, bet be šauksmo.
- Bridge: pusiau kalbama, maksimaliai arti mikrofono.
- Pabaiga: paskutinė eilutė su nusileidimu, ne su kulminaciniu "užrėkimu".

## 6. Instrumentinių intarpų taisyklė

- Po kiekvieno didesnio teksto bloko įterpti 4-10s muzikinį kvėpavimą.
- Naudoti: piano decay, drone, string swell, metaliniai perkusiniai akcentai.
- Intarpai turi "nešti įtampą", ne "užpildyti tylą".

## 7. Eksporto tikslai

- `mix_main.wav` (24bit, 48kHz)
- `mix_instrumental.wav`
- `mix_vocal_stem.wav`
- `lyrics_final_lt.txt`

## 8. Greitas paleidimas (30 min)

1. Paleisti Prompt 1 ir sugeneruoti 2-3 versijas.
2. Išsirinkti geriausią vokalo emociją.
3. Jei per švaru, paleisti Prompt 2.
4. Jei per purvu, paleisti Prompt 3.
5. Patvirtinti `A_radio` arba `A_full` kaip gamybinį master.
