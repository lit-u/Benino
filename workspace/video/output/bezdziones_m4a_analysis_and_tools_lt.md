# bezdziones.m4a - technine analize ir GitHub irankiai

Data: 2026-02-13
Failas: `D:\_PAL\benino\workspace\documents\bezdziones.m4a`

## 1. Greita technine analize (padaryta lokaliai)

- Trukme: `60.0 s`
- Audio codec: `Opus`
- Sample rate: `48 kHz`
- Kanalai: `stereo (2ch)`
- Bitrate (stream): `~137 kbps`
- Bitrate (container): `~139 kbps`
- Integruotas garsumas: `-16.2 LUFS`
- Loudness range (LRA): `10.2 LU`
- Mean volume: `-17.5 dB`
- Max volume: `-1.0 dB`
- Meta komentaras rodo Suno kilme:
  - `made with suno ...`

Trumpa isvada:
- Daina turi pakankamai dinamika (LRA 10.2), nera "plyta".
- Peak iki `-1.0 dB` yra saugus web platformoms.
- Kaip demo/tarpinis renderis - tvarkoje.

## 2. Ar galiu "ismokti analizuoti"?

Taip. Jau galime:
- automatiskai vertinti technine kokybe (loudness, peak, dinamika),
- lyginti kelis renderius tarpusavyje,
- prideti muzikinius pozymeius (tempo, key, timbre, segmentai) su papildomais irankiais.

## 3. GitHub irankiai (praktinis pasirinkimas)

### A) Bazinis ir greitas startas

1. `librosa` - Python audio/muzikos analize:
- https://github.com/librosa/librosa
- Naudojimas: tempo, chroma, segmentai, spectral feature.

2. `Essentia` - placiausias MIR toolbox:
- https://github.com/MTG/essentia
- Naudojimas: low-level + high-level descriptoriai, muzikiniai pozymeiai.

### B) Tikslesni taskai

3. `madmom` - ritmas, beat/downbeat:
- https://github.com/CPJKU/madmom

4. `libkeyfinder` - tonacijos nustatymas:
- https://github.com/mixxxdj/libkeyfinder

5. `basic-pitch` - audio->MIDI (melodijos/aukscio analizei):
- https://github.com/spotify/basic-pitch

### C) Stem ir palyginimo analize

6. `spleeter` - vocal/accompaniment atskyrimas:
- https://github.com/deezer/spleeter

7. `mir_eval` - metrikos ir benchmark vertinimas:
- https://github.com/mir-evaluation/mir_eval

8. `openSMILE` - labai platus feature extraction:
- https://github.com/audeering/opensmile

## 4. Rekomenduojamas pipeline tau (be GPU streso)

1. `ffprobe + ffmpeg` (technine kokybe).
2. `librosa` (tempo + segmentacija + energijos kreive).
3. `Essentia` (aukstesnio lygio descriptoriai).
4. Jei reikia: `spleeter` vocals/stems.
5. Lyginimo lentele tarp keliu Suno versiju.

## 5. Kitas praktinis zingsnis

Jei duosi 2-3 papildomus renderius, padarysiu:
- vienoda automatine ataskaita visiems,
- "best candidate" atranka pagal technine + muzikine stabiluma.
