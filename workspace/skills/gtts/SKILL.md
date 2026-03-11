---
name: gtts
description: Greitas tekstų įgarsinimas lietuvių kalba naudojant Google TTS. Triggeriai: "įgarsink", "padaryk audio", "sukurk mp3", "skaityk garsiai", "audioknygą"
always: false
---

# gTTS — Greito Įgarsinimo Skill

Konvertuoja lietuvišką tekstą į MP3 audio failą per Google Translate TTS.

## Galimybės
- Tekstas → MP3 (lietuvių kalba)
- Failas → MP3 (nuskaito .txt failą)
- Greita, nemokama, nereikia API rakto

## Apribojimai
- Tik vienas balsas (Google LT)
- Kirčiavimas ne visada tikslus
- Reikia interneto ryšio
- ~5000 simbolių limitas vienam requestui (ilgesnius tekstus skaido automatiškai)

## Naudojimas

### Tekstas → MP3
```python
exec("python workspace/skills/gtts/scripts/narrate.py --text 'Tavo tekstas čia' --out output.mp3")
```

### Failas → MP3
```python
exec("python workspace/skills/gtts/scripts/narrate.py --file input.txt --out output.mp3")
```

## Workflow
1. Gauni tekstą arba failo kelią
2. Paleidi `narrate.py` skriptą
3. Praneši kur išsaugotas MP3 failas
