---
name: tts
description: Generate Lithuanian text-to-speech audio using edge-tts.
---

# TTS (Text-to-Speech) Skill

Generuok garso failus iš teksto naudojant `edge-tts`. Palaikoma lietuvių kalba.

## Naudojimas

### Iš teksto tiesiogiai
```
exec(command="python scripts/benino/video_pipeline.py --tts \"Sveiki! Tai yra testavimo pranešimas.\"", timeout=60)
```

### Iš failo
```
exec(command="python scripts/benino/video_pipeline.py --tts-file workspace/kelias/tekstas.txt --output workspace/video/output/mano_audio.mp3", timeout=60)
```

### Su kitu balsu
```
exec(command="python scripts/benino/video_pipeline.py --tts \"Tekstas\" --voice lt-LT-OnaNeural", timeout=60)
```

## Prieinami lietuviški balsai

| Balsas | Kodas | Aprašymas |
|--------|-------|-----------|
| Leonas | `lt-LT-LeonasNeural` | Vyriškas, neutralus (default) |
| Ona | `lt-LT-OnaNeural` | Moteriškas, neutralus |

## Anglų kalbos balsai (jei reikia)

| Balsas | Kodas |
|--------|-------|
| Guy | `en-US-GuyNeural` |
| Jenny | `en-US-JennyNeural` |
| Aria | `en-US-AriaNeural` |

## Trigger žodžiai

- "Įgarsink šį tekstą"
- "Padaryk audio iš..."
- "Perskaityk balsu"
- "Sukurk garso failą"
- "TTS" / "text to speech"

## Workflow

1. Vartotojas pateikia tekstą arba nurodo failą
2. Naudok `exec` su `video_pipeline.py --tts`
3. Rezultatas: MP3 failas `workspace/video/output/`
4. Pranešk vartotojui kur rastas failas

## Pastabos

- Generavimas trunka ~5-15 sek. (priklausomai nuo teksto ilgio)
- Max rekomenduojamas teksto ilgis: ~5000 simbolių (ilgesniam tekstui - suskaldyk į dalis)
- edge-tts yra nemokamas Microsoft serviso - nereikia API rakto
- Audio kokybė: gera (natūralus neuroninis balsas)
