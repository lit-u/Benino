---
name: video-pipeline
description: Analyze video URLs, extract content, generate informative clips with Lithuanian voiceover.
---

# Video Pipeline Skill

Analizuok video iš URL (Facebook, YouTube, bet koks) ir sukurk informacinį klipą su lietuvišku įgarsinimu.

## Naudojimas

Kai vartotojas siunčia video URL ir prašo analizuoti, sukurti klipą arba įgarsinti:

### Pilnas pipeline
```
exec(command="python scripts/benino/video_pipeline.py \"URL\"", timeout=600)
```

### Tik analizė (be video montažo)
```
exec(command="python scripts/benino/video_pipeline.py \"URL\" --skip-video", timeout=300)
```

### Tik įgarsinimas (TTS)
```
exec(command="python scripts/benino/video_pipeline.py --tts \"Tekstas lietuviškai\"", timeout=60)
```

### Įgarsinimas iš failo
```
exec(command="python scripts/benino/video_pipeline.py --tts-file workspace/video/output/.../script.txt", timeout=60)
```

## Pipeline žingsniai

1. **Parsisiuntimas** - `yt-dlp` (Facebook, YouTube, TikTok, Twitter...)
2. **Audio ištraukimas** - `ffmpeg`
3. **Transkripcija** - `faster-whisper` (arba subtitrai jei yra)
4. **AI analizė** - Groq LLM identifikuoja temas, faktus, paieškos užklausas
5. **Šaltinių paieška** - YouTube + Brave Search randa originalius video/straipsnius
6. **Scenarijaus generavimas** - LLM sukuria informacinį tekstą lietuviškai
7. **Voice-over** - `edge-tts` su lietuvišku balsu (lt-LT-LeonasNeural)
8. **Video montažas** - keyframes + voiceover → finalinis klipas

## Rezultatai

Output direktorija: `workspace/video/output/{data}_{slug}/`
- `source.mp4` - originalus video
- `transcript.txt` - transkripcija
- `analysis.json` - AI analizė (temos, faktai)
- `script.txt` - scenarijus lietuviškai
- `voiceover.mp3` - lietuviškas įgarsinimas
- `final.mp4` - galutinis informacinis klipas
- `frames/` - keyframes
- `README.md` - pilna ataskaita

## Svarbios pastabos

- Pipeline gali trukti 2-5 min. Ilgiems video naudok `spawn` vietoj `exec`.
- Facebook URL kartais reikalauja papildomo bandymo (yt-dlp fallback).
- Jei vartotojas nori tik garso - naudok `--tts` režimą (greitesnis).
- API raktai imami iš `nanobot/config.json` (Groq + Brave Search).

## Trigger žodžiai

Aktyvuok šį skill kai vartotojas sako:
- "Analizuok šį video"
- "Sukurk klipą iš šito"
- "Įgarsink"
- "Padaryk video apžvalgą"
- Siunčia Facebook/YouTube/TikTok nuorodą su prašymu analizuoti
