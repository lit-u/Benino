# Video Technine Dokumentacija (v1)

Data: 2026-02-12

## 1. Ar PDF yra promptu pavyzdziu?

Taip. `workspace/documents/Project Carnival Intimacy Ad.pdf` yra konkretus promptu naudojimo aprasas:
- Koncepcijos/scripto promptas (screenplay tipo instrukcija su satyriniu scenarijumi).
- "Prompt System" skaidre: shot list + detailed prompts + scene breakdown.
- Kling 3.0 video promptu pavyzdys su element taginimu (`@element_...`) konsistencijai tarp kadru.

Trumpi pavyzdziai is PDF:
- "Start with concept, not tools"
- "Prompt System (ChatGPT to Nano Banana Pro)"
- "You can tag elements within video prompts to ensure visual and narrative consistency"

## 2. Startinis saltinis musu pipeline

Pradinis URL: https://www.facebook.com/share/v/1Fv7Z81kjt/

Tikslas: sukurti kartojama workflow, kur kadravimo kalba + promptu sintakse duoda prognozuojama rezultata (Nano Banana PRO / ChatGPT / video generatoriai).

## 3. Kadravimo tipai (LT -> EN)

### Baziniai
- Extreme Close-Up (ECU) / Itin stambus planas
Matoma labai maza detale: akis, lupos, oda, mikroemocija.

- Close-Up (CU) / Stambus planas
Matomas veidas arba vienas konkretus objektas.

- Medium Close-Up (MCU) / Vidutiniskai stambus planas
Nuo krutines arba peciu iki galvos.

- Medium Shot (MS) / Vidutinis planas
Nuo liemens arba krutines iki galvos.

- Medium Wide Shot (MWS) / Vidutiniskai platus planas
Personazas matomas mazdaug nuo keliu aukstyn.

- Wide Shot (WS) / Platus planas (pilnas ugis)
Visa figura matoma nuo galvos iki koju.

- Extreme Wide Shot (EWS) / Itin platus planas
Personazas labai mazas, dominuoja aplinka, mastelis ir kontekstas.

### Papildomi
- Over-the-Shoulder Shot (OTS) / Planas per peti
Vaizdas rodomas per kito personazo peti; itampa, kryptis, dialogo perspektyva.

- POV Shot / Subjektyvus planas
Kamera atstoja personazo akis; ziurovas "jo vietoje".

- Dutch Angle / Pakrypes planas
Kamera pakreipta; nerimas, chaosas, nestabilumas.

- Low Angle Shot / Zemas rakursas
Kamera is apacios; personazas atrodo galingesnis ar gresmingas.

## 4. Promptu sablonai (praktikai)

### 4.1 Vieno kadro sablonas (Nano Banana / image model)
```
[SHOT_TYPE], [subject], [emotion/action], [location],
lighting: [soft/commercial/cinematic],
lens feel: [35mm/50mm/85mm],
color grade: [warm/neutral/cool],
background: [depth of field details],
style constraints: natural skin texture, no plastic look, no artifacts.
```

Pavyzdys:
```
Medium Close-Up (MCU), jaunas vyras kalba su terapeutu, nerimastinga israiska,
vintage medinis kabinetas,
soft commercial lighting,
50mm lens feel,
warm cream color grade,
background diplomas slightly out of focus,
natural skin texture, realistic fabric, no text, no watermark.
```

### 4.2 Video promptas (Kling tipo)
```
@element_character [brief action cue].
[SHOT_TYPE] of @element_character.
Lighting: [..]. Background: [..].
Dialogue tone: [..].
Camera motion: [locked / slow push-in / handheld subtle].
Duration: [x]s.
```

### 4.3 Dialogo scenos mini-paketas
- Shot A: EWS (establishing)
- Shot B: OTS (speaker 1)
- Shot C: OTS reverse (speaker 2)
- Shot D: MCU reaction
- Shot E: CU punchline

## 5. Rekomenduojamas mini-pipeline (MVP)

1. Concept + script (<=60s).
2. Shot list (8-14 kadru).
3. Kiekvienam kadrui: strukturuotas promptas.
4. Generacija (iteracijos, ne vienas pass).
5. Assembly (timeline + typo + music pacing + basic grade).
6. QA: ritmas, konsistencija, ar kadravimo kalba atitinka intencija.

## 6. Kokybes taisykles

- Konsistencija svarbiau uz "viena tobula kadra".
- Vienam kadrui viena intencija.
- Jei emocija neiskaitoma per 1-2 s, prompta trumpinti ir konkretinti.
- Vengti multi-angle viename generavimo pass, jei prioritetas yra greitis.

## 7. Kitas zingsnis

Kai turesim pilna transkripta/iskarpas is FB video, papildom:
- "Shot taxonomy examples" su realiais kadrais is to video.
- "Prompt library v2" (geri/nesekmingi promptai + pataisos).
- "Assembly presets" (15s, 30s, 60s versijos).

## 8. FB video pavyzdziu kadrai (praktinis rinkinys)

Saltinis:
- `workspace/video/docs/examples/source.mp4`

Sugeneruoti "golden" JPG failai (po 1 kadravimo tipui):
- `workspace/video/docs/examples/frames_golden/ECU_2.5s_Extreme_Close_Up.jpg`
- `workspace/video/docs/examples/frames_golden/CU_6.0s_Close_Up.jpg`
- `workspace/video/docs/examples/frames_golden/MCU_13.0s_Medium_Close_Up.jpg`
- `workspace/video/docs/examples/frames_golden/MS_19.0s_Medium_Shot.jpg`
- `workspace/video/docs/examples/frames_golden/MWS_26.0s_Medium_Wide_Shot.jpg`
- `workspace/video/docs/examples/frames_golden/WS_32.0s_Wide_Shot.jpg`
- `workspace/video/docs/examples/frames_golden/EWS_40.0s_Extreme_Wide_Shot.jpg`
- `workspace/video/docs/examples/frames_golden/LOW_43.5s_Low_Angle_Shot.jpg`
- `workspace/video/docs/examples/frames_golden/OTS_55.0s_Over_the_Shoulder.jpg`

Pastaba del sio konkretaus source:
- OCR aptiko: `ECU, CU, MCU, MS, MWS, WS, EWS, LOW, OTS`.
- OCR neaptiko: `POV, DUTCH`.
- Santrauka yra faile: `workspace/video/docs/examples/frames_golden/README_missing_shots.txt`.

## 9. Cinema planavimo automatizacija (is `brain_os/cinema` ideju)

Perkelta i praktini, neinteraktyvu stage `workspace` aplinkoje:
- `theme -> scene -> beats -> shots -> render_plan`
- be `input()` stabdymu
- su UTF-8 failais

Skriptas:
- `workspace/video/tools/cinema_pipeline.py`

Paleidimo pavyzdys (60s):
```bash
python workspace/video/tools/cinema_pipeline.py \
  --theme "kontrole ir chaosas" \
  --goal "Parodyti kaip pereinama nuo kontroles prie adaptacijos" \
  --target-seconds 60 \
  --output workspace/video/output/cinema_plan_control_60s
```

Sugeneruojami failai:
- `scene.txt`
- `beats.json`
- `shots.json`
- `render_plan.json`

Praktinis rezultatas:
- `workspace/video/output/cinema_plan_control_60s/render_plan.json`

## 10. Atskira video automatizacija

Svarbu:
- `node sutvarkyk link` yra teksto/knowledge pipeline.
- Video gamybai naudojam atskira automate entrypoint.

Entry point:
- `workspace/video/tools/video_automate.py`

Paleidimas:
```bash
python workspace/video/tools/video_automate.py \
  --mode plan \
  --theme "1min intro filmas" \
  --goal "Per 60s parodyti problema ir sprendima" \
  --source-url "https://www.facebook.com/share/v/1Fv7Z81kjt/"
```

Output pavyzdys:
- `workspace/video/output/video_automate/2026-02-12_1min_intro_filmas/render_plan.json`

Papildomas rezimas (`examples`):
```bash
python workspace/video/tools/video_automate.py \
  --mode examples \
  --source-file workspace/video/docs/examples/source.mp4 \
  --examples-fps 0.25 \
  --output workspace/video/output/video_automate/test_examples_mode
```
