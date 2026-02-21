# Video Automatizacija (Kling-only)

Data: 2026-02-12

## Tikslas

Uzsifiksuoti visa atlikta workflow, kad nereiketu visko kurti is naujo.

## Fiksuotos taisykles

- Dirbame tik `Kling-only`.
- `node sutvarkyk link` nenaudojamas video gamybai (tai teksto pipeline).
- Tikslinis formatas: `16:9`, `24 fps`.
- Trukme: `03:15` (`195s`), suskaidyta i ~48 shotus.

## Pagrindiniai failai

- Bendras master:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/video_clip_master_lt.md`
- Kling produkcijos planas:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_production_pack_lt.md`
- Shot sheet:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_shot_by_shot_prompt_sheet_v1.md`
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_shot_by_shot_prompt_sheet_v2_aggressive.md`
- Batch tvarka:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_batch_order_v1.md`
- Startinis Top 10 paketas:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_first_run_pack.md`
- Step-by-step + kaina:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_step_by_step_plan_lt.md`

## Trumpa vykdymo seka

1. Paleisti Top 10 shotu (po 4 variantus kiekvienam).
2. Is kiekvieno shot palikti top2.
3. Continuity fix ant top2.
4. Final top1.
5. Pereiti per `Batch_1..Batch_5`.
6. Surinkti Premiere.

## Kainos skaiciavimo sablonas

Is Kling paskyros paimti:

- `P` = plano kaina (USD)
- `K` = plano kreditai
- `C5` = kreditu kiekis uz 5s renderi
- `C10` = kreditu kiekis uz 10s renderi

Skaiciavimas:

- `TOTAL_CREDITS ~= 336 * C5`
- `USD_PER_CREDIT = P / K`
- `ESTIMATED_USD = TOTAL_CREDITS * USD_PER_CREDIT`

## Filmu sablonas (ne klipinis)

- Naudoti `Story -> Song -> Score -> Scene` sablona:
  - `workspace/video/docs/FILM_STORY_SONG_SCORE_SCENE_TEMPLATE_LT.md`

## Paruosti promptai (copy/paste)

- Filmo automatizacijai:
  - `workspace/video/docs/PROMPT_FILMO_AUTOMATIZACIJA_LT.md`
- Tik dainai is bet kokio teksto:
  - `workspace/video/docs/PROMPT_DAINA_IS_BET_KOKIO_TEKSTO_LT.md`

## Tools info ir prisijungimai

- Bendras gidas:
  - `workspace/video/docs/VIDEO_TOOLS_PRISIJUNGIMAI_LT.md`
- ACE paleidimo runbook (praktinis):
  - `workspace/video/output/proto_priestaravimai_A_ace_runbook_lt.md`
