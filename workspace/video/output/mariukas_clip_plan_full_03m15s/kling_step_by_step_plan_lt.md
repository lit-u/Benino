# Kling Step-by-Step planas (03:15 klipui)

Data: 2026-02-12

## 0) Oficialios nuorodos
- Kling Global app: https://app.klingai.com/global/
- Kling kursai / tutorial: https://courses.klingai.com/
- (In-app) `Release Notes` ir `Quick Start` skiltys yra pa?iame Kling UI.

Pastaba apie kainas:
- ?iandien tiksli? oficiali? plan? kain? automati?kai nuskaityti nepavyko (Kling puslapiai JS/robots apriboti), tod?l kain? reikia paimti tiesiai i? tavo paskyros `Plans` lange.

## 1) Paruo?imas prie? renderius
1. Prisijunk ? https://app.klingai.com/global/.
2. Pasitikrink `Plans / Credits` puslap? ir u?sira?yk:
- m?nesio plano kain? (USD)
- kiek kredit? duoda planas
- kiek kredit? kainuoja 5s ir 10s generacija (jei rodo)
3. Pasirink master format?:
- Aspect `16:9`
- FPS `24`
- Target: `03:15`

## 2) Naudojami m?s? failai
- Pagrindinis prompt? failas v2 (agresyvus):
`workspace/video/output/mariukas_clip_plan_full_03m15s/kling_shot_by_shot_prompt_sheet_v2_aggressive.md`
- JSON versija automatizacijai:
`workspace/video/output/mariukas_clip_plan_full_03m15s/kling_shot_by_shot_prompt_sheet_v2_aggressive.json`
- Renderinimo eili?kumas:
`workspace/video/output/mariukas_clip_plan_full_03m15s/kling_batch_order_v1.md`
- Greitas startas (Top 10):
`workspace/video/output/mariukas_clip_plan_full_03m15s/kling_first_run_pack.md`

## 3) Praktinis paleidimas (pirmas vakaras)
1. Atidaryk `kling_first_run_pack.md`.
2. Renderink Top 10 shot? po 4 variantus:
- naming: `S18_v1..v4`, `S10_v1..v4`, ir t. t.
3. Atranka:
- pasilieki `top2` kiekvienam shot.
4. Continuity fix:
- tie patys drabu?iai, veidai, rekvizitai.
5. Final:
- i? `top2` pasirenki `top1` final renderiui.

## 4) Pilnas workflow (visi 48 shotai)
- Seed scan: 4 variantai x 48 shotai = 192 renderiai
- Continuity pass: 2 variantai x 48 shotai = 96 renderiai
- Final pass: 1 variantas x 48 shotai = 48 renderiai
- I? viso: 336 renderiai

## 5) Ka?t? skai?iavimas (tikslus, i? tavo plan? kain?)
?ra?yk ?ias reik?mes i? Kling paskyros:
- `C5` = kreditai u? vien? 5s render?
- `C10` = kreditai u? vien? 10s render?
- `P` = plano kaina USD
- `K` = plano kreditai

M?s? atveju (dauguma shot? 4-5s), greita aproksimacija:
- `TOTAL_CREDITS ? 336 * C5`
- `USD_PER_CREDIT = P / K`
- `ESTIMATED_USD = TOTAL_CREDITS * USD_PER_CREDIT`

Jei dal? shot? renderinsi 10s:
- `TOTAL_CREDITS = (N5 * C5) + (N10 * C10)`

## 6) Rekomenduojama ekonomin? taktika
1. Pirm? kart? daryk tik Top 10 (ne visus 48).
2. Jei rezultatas ?laiko?, tik tada leisk vis? Batch_1..Batch_5.
3. Solo dal? (02:32-02:57) renderink paskutin?, nes ji turi daugiausiai variacij?.
4. Nekelk rezoliucijos ? max, kol neturi u?fiksuoto final kadravimo.

## 7) Kokyb?s check-list
- Ar Matas/Ema i?lieka nuosekl?s tarp gretim? shot??
- Ar rekvizitai (aitvaras, bilietas, laikrodis) nesikei?ia forma/spalva?
- Ar yra per ?safe? kadr? (per centrinis, per plok??ias ap?vietimas)?
- Ar priedainiuose tempas jau?iasi didesnis nei posmeliuose?

## 8) Kai tur?si pirm? rezultat?
Atsi?sk shot ID ir trump? vertinim?:
- `Sxx: OK / per blanku / veidas ne tas / judesys blogas`

Pagal tai padarysiu `prompt surgery v3` konkretiems kadrams.
