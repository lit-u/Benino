---
name: summarize
description: Summarize URLs/files/YouTube with built-in tools (no external summarize binary required).
---

# Summarize Skill (Workspace Override)

Use native tools to summarize content without the external `summarize` CLI.

## When to use

- "summarize this link"
- "kas ?iame video"
- "duok santrauk?"
- "transcribe and summarize"

## Workflow

1. If it is YouTube/video URL:
- use `python scripts/benino/video_pipeline.py "URL" --skip-video`
- read generated transcript/analysis files from `workspace/video/output/...`
- return concise Lithuanian summary

2. If it is a normal article URL:
- use web/read tools to fetch page content
- summarize key points, risks, and action items

3. If it is a local file:
- read file and summarize with sections:
  - Esm?
  - Pagrindin?s ??valgos
  - K? daryti toliau

## Output style

- Lithuanian
- Short first, then optional detailed bullets
- Mention confidence if source is incomplete
