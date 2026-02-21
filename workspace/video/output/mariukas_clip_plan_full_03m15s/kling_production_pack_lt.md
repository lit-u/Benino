# Mariukas - Kling-only gamybos paketas (03:15)

## 1. Principas
- Jokio live filmavimo.
- Visas klipas gaminamas su Kling (video generation) + rankinis montažas Premiere.
- Tikslas: nuoseklus vizualus pasaulis per visą 03:15.

## 2. Pipeline (Kling)
1. Previz: suskaidyti klipą į 4-8 s segmentus.
2. Character Bible: 7 personažų aprašai (vienoda apranga, veido bruožai, amžius, energija).
3. Location Bible: 12-15 raktinių lokacijų su vienodu meniniu tonu.
4. Prompt pass v1: sugeneruoti visus shotus pagal laiką.
5. Continuity pass v2: pataisyti nesutapimus (drabužiai, rekvizitai, spalvos, paros laikas).
6. Final render: eksportai 4K/1080p.
7. Premiere assembly: ritmas, lyric sync, spalva, titrai.

## 3. Segmentavimo taisyklės
- Tikslinis shot ilgis: 4-8 s.
- 03:15 = ~195 s => apie 32-42 shotai.
- Solo daliai (02:32-02:57): trumpesni 2-4 s shotai didesniam tempui.

## 4. Prompt struktūra (Kling)
Kiekvienam shotui visada naudoti:
- Subject (kas kadre)
- Location (kur)
- Action (ką daro)
- Camera (shot type + motion)
- Lighting + color mood
- Continuity tags (personažas, drabužis, rekvizitas)
- Negative constraints (no text, no watermark, no logo, no extra fingers)

## 5. Continuity taisyklės
- Matas: tas pats paltas + plaukų forma visame klipe.
- Ema: tas pats siluetas ir spalvinis kodas.
- Rekvizitai: aitvaras, bilietas, laikrodis turi išlikti tokie patys tarp scenų.
- Lokacijos spalvinė kryptis:
  - Posmeliai: vėsi pilkai žalsvi tonai
  - Priedainiai: kontrastingesni mėlyni/raudoni akcentai
  - Pabaiga: pereiti į ramesnį šiltesnį toną

## 6. Render planas pagal dainą
- 00:00-00:13 Intro: 2 shotai
- 00:13-00:46 I posmelis: 6-8 shotai
- 00:46-01:25 Priedainis A: 8-10 shotų
- 01:25-01:54 II posmelis: 6-7 shotai
- 01:54-02:32 Priedainis B: 8-10 shotų
- 02:32-02:57 Solo: 8-12 shotų
- 02:57-03:15 Pabaiga: 3-4 shotai

## 7. Premiere surinkimas
1. Import Kling clipus pagal laiko bloką.
2. Sudėlioti rough cut pagal lyrics timestampus.
3. Keisti netinkančius shotus pakartotiniu Kling renderiu.
4. Stabilizuoti spalvą (global LUT + lokalūs pataisymai).
5. Final export: 16:9 master, 9:16 social.

## 8. Ką daryti dabar
- Patvirtinti, kad dirbam tik su Kling.
- Tada sugeneruoti konkretų `shot-by-shot Kling prompt sheet` (40+ promptų) pagal tavo tekstą.
