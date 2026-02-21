#!/usr/bin/env python3
"""
Cinema planning helper for short-form videos.

Input: theme + optional goal/constraints
Output: scene, beats, shots, render_plan JSON
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Beat:
    id: str
    text: str


@dataclass
class Shot:
    beat_id: str
    beat_text: str
    shot_type: str
    lens: str
    camera: str
    emotion: str
    duration_s: float
    purpose: str


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def build_scene(theme: str, goal: str) -> str:
    t = theme.lower()
    if any(k in t for k in ["control", "kontrol", "chaos", "nestabil"]):
        return (
            "Character works in a controlled environment where everything seems perfect. "
            "A small failure appears and starts growing. "
            "Instead of forcing control, character accepts uncertainty and adapts."
        )
    if any(k in t for k in ["trust", "pasitikej", "team", "komanda"]):
        return (
            "Two people with different priorities must solve one urgent problem together. "
            "At first they do not trust each other. "
            "Through action, trust is built and result improves."
        )
    base = (
        "A character faces a clear obstacle, tries an obvious solution, fails, "
        "then changes approach and wins a smaller but meaningful result."
    )
    if goal:
        return f"{base} Goal focus: {normalize(goal)}"
    return base


def split_into_beats(scene_text: str) -> list[Beat]:
    raw = [
        "Establish world and current status quo.",
        "Introduce trigger that disrupts normal flow.",
        "Character reacts with first instinctive attempt.",
        "Complication raises emotional and practical stakes.",
        "Character reframes problem and chooses new approach.",
        "Short resolution with visible change and takeaway.",
    ]
    if "controlled environment" in scene_text.lower():
        raw = [
            "Perfect system is running smoothly and quietly.",
            "One monitor or signal fails unexpectedly.",
            "Character freezes and scans for cause.",
            "Failure spreads; pressure rises.",
            "Character stops over-controlling and prioritizes core fix.",
            "System stabilizes; character accepts uncertainty.",
        ]
    return [Beat(id=f"B{i+1}", text=t) for i, t in enumerate(raw)]


def beat_to_shot(beat: Beat) -> Shot:
    text = beat.text.lower()

    if any(k in text for k in ["establish", "status quo", "perfect system"]):
        return Shot(beat.id, beat.text, "EWS", "24mm", "Static", "Context", 4.5, "world")

    if any(k in text for k in ["fails", "trigger", "disrupt", "signal"]):
        return Shot(beat.id, beat.text, "CU", "85mm", "Locked", "Disruption", 5.0, "trigger")

    if any(k in text for k in ["freezes", "reacts", "instinctive"]):
        return Shot(beat.id, beat.text, "MCU", "50mm", "Slow push-in", "Stress", 6.0, "reaction")

    if any(k in text for k in ["pressure", "spreads", "stakes", "complication"]):
        return Shot(beat.id, beat.text, "OTS", "35mm", "Handheld subtle", "Tension", 6.5, "escalation")

    if any(k in text for k in ["reframes", "new approach", "prioritizes"]):
        return Shot(beat.id, beat.text, "MS", "35mm", "Tracking slow", "Agency", 6.0, "turn")

    return Shot(beat.id, beat.text, "WS", "35mm", "Static", "Release", 5.0, "resolution")


def adjust_durations(shots: list[Shot], target_seconds: float) -> None:
    if not shots:
        return
    current = sum(s.duration_s for s in shots)
    if current <= 0:
        return
    ratio = target_seconds / current
    for s in shots:
        s.duration_s = round(max(2.0, s.duration_s * ratio), 2)


def build_prompt(shot: Shot, style: str) -> str:
    return (
        f"{shot.shot_type} shot, {shot.beat_text} "
        f"Camera: {shot.camera}. Lens feel: {shot.lens}. "
        f"Emotion: {shot.emotion}. Style: {style}."
    )


def export_plan(theme: str, goal: str, style: str, beats: list[Beat], shots: list[Shot], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    scene = build_scene(theme, goal)

    with (out_dir / "scene.txt").open("w", encoding="utf-8") as f:
        f.write(scene + "\n")

    with (out_dir / "beats.json").open("w", encoding="utf-8") as f:
        json.dump([asdict(b) for b in beats], f, ensure_ascii=False, indent=2)

    shot_rows = []
    for s in shots:
        row = asdict(s)
        row["prompt"] = build_prompt(s, style)
        shot_rows.append(row)

    with (out_dir / "shots.json").open("w", encoding="utf-8") as f:
        json.dump(shot_rows, f, ensure_ascii=False, indent=2)

    render_plan = {
        "theme": theme,
        "goal": goal,
        "style": style,
        "target_seconds": round(sum(s.duration_s for s in shots), 2),
        "sequence": shot_rows,
    }

    with (out_dir / "render_plan.json").open("w", encoding="utf-8") as f:
        json.dump(render_plan, f, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a non-interactive cinema render plan.")
    parser.add_argument("--theme", required=True, help="Theme keyword, e.g. control, trust, conflict")
    parser.add_argument("--goal", default="", help="One-sentence video goal")
    parser.add_argument("--style", default="cinematic, natural skin, realistic lighting", help="Global style constraints")
    parser.add_argument("--target-seconds", type=float, default=60.0, help="Target runtime in seconds")
    parser.add_argument("--output", default="workspace/video/output/cinema_plan", help="Output folder")
    args = parser.parse_args()

    scene = build_scene(args.theme, args.goal)
    beats = split_into_beats(scene)
    shots = [beat_to_shot(b) for b in beats]
    adjust_durations(shots, args.target_seconds)

    export_plan(args.theme, args.goal, args.style, beats, shots, Path(args.output))
    print(f"Plan generated: {args.output}")


if __name__ == "__main__":
    main()
