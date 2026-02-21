#!/usr/bin/env python3
"""
Standalone video automation entrypoint.

This is intentionally separate from `node sutvarkyk link` text pipeline.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import json

from cinema_pipeline import (
    adjust_durations,
    beat_to_shot,
    build_scene,
    export_plan,
    split_into_beats,
)


def slug(text: str) -> str:
    safe = "".join(ch.lower() if ch.isalnum() else "_" for ch in text.strip())
    safe = "_".join(part for part in safe.split("_") if part)
    return safe[:40] or "video"


def run_plan_mode(args: argparse.Namespace, out_dir: Path) -> None:
    if not args.theme.strip():
        raise ValueError("--theme is required in plan mode")

    scene = build_scene(args.theme, args.goal)
    beats = split_into_beats(scene)
    shots = [beat_to_shot(b) for b in beats]
    adjust_durations(shots, args.target_seconds)
    export_plan(args.theme, args.goal, args.style, beats, shots, out_dir)

    if args.source_url:
        (out_dir / "source_url.txt").write_text(args.source_url.strip() + "\n", encoding="utf-8")


def run_examples_mode(args: argparse.Namespace, out_dir: Path) -> None:
    if not args.source_file:
        raise ValueError("--source-file is required in examples mode")

    source_file = Path(args.source_file)
    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    frames_dir = out_dir / "frames_examples"
    frames_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = str(frames_dir / "frame_%04d.jpg")
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(source_file),
        "-vf",
        f"fps={args.examples_fps},scale=1280:-1",
        output_pattern,
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    frames = sorted(p.name for p in frames_dir.glob("frame_*.jpg"))
    manifest = {
        "mode": "examples",
        "source_file": str(source_file),
        "frames_dir": str(frames_dir),
        "frame_count": len(frames),
        "examples_fps": args.examples_fps,
        "notes": "Sample frames for manual shot reference and labeling.",
    }
    (out_dir / "examples_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run standalone video automation.")
    parser.add_argument("--mode", choices=["plan", "examples"], default="plan", help="Automation mode")
    parser.add_argument("--theme", default="", help="Video theme (required in plan mode)")
    parser.add_argument("--goal", default="", help="One-sentence goal")
    parser.add_argument("--style", default="cinematic, natural skin, realistic lighting", help="Global style")
    parser.add_argument("--target-seconds", type=float, default=60.0, help="Runtime target")
    parser.add_argument("--source-url", default="", help="Optional source URL reference")
    parser.add_argument("--source-file", default="", help="Local source video path (required in examples mode)")
    parser.add_argument("--examples-fps", type=float, default=0.5, help="Frame extraction rate for examples mode")
    parser.add_argument("--output", default="", help="Optional output dir override")
    args = parser.parse_args()

    if args.output:
        out_dir = Path(args.output)
    else:
        stamp = datetime.now().strftime("%Y-%m-%d")
        base_name = args.theme if args.theme.strip() else "video"
        out_dir = Path(f"workspace/video/output/video_automate/{stamp}_{slug(base_name)}")

    out_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "plan":
        run_plan_mode(args, out_dir)
    else:
        run_examples_mode(args, out_dir)

    print(f"Video automate completed: {out_dir}")


if __name__ == "__main__":
    main()
