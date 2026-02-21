---
name: video-automatizacija
description: Kling-only video automation workflow for 03:15 music video production (planning, prompts, batching, cost model).
homepage: https://app.klingai.com/global/
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["python", "ffmpeg", "ffprobe"] },
      },
  }
---

# Video Automatizacija (Kling-only)

Use this skill when the user wants end-to-end music video generation with Kling (no live filming), from lyrics/timing to render batches.

## Scope

- Mode: `kling_only`
- Target format: 16:9, 24 fps
- Typical duration: 03:15 (195s)
- Typical output: 48 shots + batch render order

## Canonical files (this workspace)

- Master doc:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/video_clip_master_lt.md`
- Kling production guide:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_production_pack_lt.md`
- Shot-by-shot prompts:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_shot_by_shot_prompt_sheet_v1.md`
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_shot_by_shot_prompt_sheet_v2_aggressive.md`
- Batch execution order:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_batch_order_v1.md`
- First-run pack (Top 10 shots):
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_first_run_pack.md`
- Step-by-step with links/cost formula:
  - `workspace/video/output/mariukas_clip_plan_full_03m15s/kling_step_by_step_plan_lt.md`
- Film automation prompt (Story -> Song -> Score -> Scene):
  - `workspace/video/docs/PROMPT_FILMO_AUTOMATIZACIJA_LT.md`
- Song-from-text prompt:
  - `workspace/video/docs/PROMPT_DAINA_IS_BET_KOKIO_TEKSTO_LT.md`
- Tools + login guide:
  - `workspace/video/docs/VIDEO_TOOLS_PRISIJUNGIMAI_LT.md`

## Standard workflow

1. Confirm `kling_only` and song structure with timestamps.
2. Build/refresh shot sheet (`v2_aggressive` preferred for stronger visuals).
3. Run first pass on Top 10 shots (4 variants each).
4. Keep top 2 per shot for continuity fix.
5. Final render top 1 per shot.
6. Continue by batch order (`Batch_1..Batch_5`).
7. Assemble in Premiere, then export master + social crops.

## Cost model (template)

Collect from Kling account:

- `P` = monthly plan price (USD)
- `K` = monthly credits
- `C5` = credits per 5s render
- `C10` = credits per 10s render

Then estimate:

- `TOTAL_CREDITS ~= 336 * C5` (for 48-shot full 3-pass flow with mostly short clips)
- `USD_PER_CREDIT = P / K`
- `ESTIMATED_USD = TOTAL_CREDITS * USD_PER_CREDIT`

## Quality gates

- Character continuity: MATAS/EMA face + clothing consistency across adjacent shots.
- Prop continuity: kite/ticket/watch unchanged in design and color.
- Section rhythm: choruses must feel more energetic than verses.
- Visual quality: avoid flat lighting, generic centered framing, weak motion.

## When to regenerate

Regenerate `v2` prompts if:

- face drift > acceptable
- props mutate
- mood mismatch between section and visuals
- too many safe/static-looking shots
