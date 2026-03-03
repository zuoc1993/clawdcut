"""Score aesthetic alignment from script/storyboard/style brief files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_CINEMATIC_HINTS = {
    "cinematic",
    "warm",
    "emotional",
    "story",
    "dissolve",
    "rule of thirds",
    "slow zoom",
    "tracking",
    "moody",
}

_ANTI_HINTS = {
    "chaotic",
    "random",
    "hard cut",
    "glitch",
    "flashy",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True, type=Path)
    parser.add_argument("--threshold", default=75.0, type=float)
    return parser.parse_args()


def _count_matches(text: str, keywords: set[str]) -> int:
    lowered = text.lower()
    return sum(1 for kw in keywords if kw in lowered)


def main() -> int:
    args = parse_args()
    clawd = args.project_dir / ".clawdcut"
    script_file = clawd / "script.md"
    storyboard_file = clawd / "storyboard.md"
    style_file = clawd / "style_brief.json"

    if (
        not script_file.exists()
        or not storyboard_file.exists()
        or not style_file.exists()
    ):
        print("required files missing under .clawdcut", file=sys.stderr)
        return 2

    script = script_file.read_text()
    storyboard = storyboard_file.read_text()
    style_data = json.loads(style_file.read_text())

    style_keywords: set[str] = set()
    palette = style_data.get("palette", {})
    raw_keywords = palette.get("keywords", []) if isinstance(palette, dict) else []
    if isinstance(raw_keywords, list):
        style_keywords = {str(k).lower() for k in raw_keywords}

    combined = f"{script}\n{storyboard}".lower()
    cinematic_hits = _count_matches(combined, _CINEMATIC_HINTS | style_keywords)
    anti_hits = _count_matches(combined, _ANTI_HINTS)

    base = 60 + cinematic_hits * 4 - anti_hits * 6
    overall = max(0.0, min(100.0, round(base, 2)))

    issues: list[str] = []
    suggestions: list[str] = []
    if anti_hits > 0:
        issues.append("Detected anti-cinematic cues.")
        suggestions.append("Reduce aggressive transitions and random pacing.")
    if cinematic_hits < 3:
        issues.append("Cinematic signals are sparse.")
        suggestions.append("Add explicit color/composition/motion intent.")
    if not issues:
        issues.append("No major aesthetic violations detected.")
        suggestions.append("Preserve current style consistency.")

    score_payload = {
        "overall": overall,
        "consistency": overall,
        "cinematicity": min(100.0, overall + 2),
        "composition": max(0.0, min(100.0, overall - 1)),
        "color_harmony": max(0.0, min(100.0, overall - 1)),
        "motion_rhythm": max(0.0, min(100.0, overall - 2)),
        "issues": issues,
        "fix_suggestions": suggestions,
    }

    (clawd / "aesthetic_score.json").write_text(
        json.dumps(score_payload, indent=2, ensure_ascii=False)
    )
    report = (
        "# Aesthetic Report\n\n"
        f"- Overall Score: {overall}\n"
        f"- Threshold: {args.threshold}\n"
        f"- Pass: {'yes' if overall >= args.threshold else 'no'}\n\n"
        "## Issues\n"
        + "\n".join(f"- {item}" for item in issues)
        + "\n\n## Suggestions\n"
        + "\n".join(f"- {item}" for item in suggestions)
        + "\n"
    )
    (clawd / "aesthetic_report.md").write_text(report)

    if overall < args.threshold:
        print(f"overall score < {args.threshold}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
