"""Build a default cinematic style brief for a Clawdcut project."""

import argparse
import json
from pathlib import Path

DEFAULT_STYLE_BRIEF = {
    "style_id": "cinematic_story",
    "narrative_mode": "cinematic_story",
    "palette": {
        "primary": ["#1F2A44", "#D9A066", "#F2E9DC"],
        "keywords": ["cinematic", "warm", "natural", "moody"],
        "forbidden": ["neon-purple-heavy", "oversaturated-green"],
    },
    "grading_preset": "cinematic_warm",
    "camera_language": {
        "preferred": ["slow-zoom-in", "pan", "tracking"],
        "forbidden": ["shake-heavy", "random-orbit"],
    },
    "transition_language": {
        "preferred": ["dissolve", "fade-to-black", "wipe-left"],
        "forbidden": ["hard-cut", "glitch"],
        "max_density": 0.25,
    },
    "composition_rules": {
        "preferred": ["rule-of-thirds", "center-weighted"],
        "safe_margin": 0.08,
    },
    "atmosphere_rules": {
        "vignette": 0.25,
        "grain": 0.08,
        "light_leak": 0.1,
    },
    "typography_rules": {
        "title_style": "elegant-serif",
        "body_style": "clean-sans",
        "animation": "fade-slide-up",
    },
    "music_profile": {
        "curve": "gentle-rise",
        "dynamic_range": "medium",
    },
    "hard_constraints": [
        "avoid visual clutter",
        "maintain color harmony",
        "preserve narrative pacing",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--style-id", default="cinematic_story")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    clawdcut_dir = args.workdir / ".clawdcut"
    clawdcut_dir.mkdir(parents=True, exist_ok=True)

    style_brief = dict(DEFAULT_STYLE_BRIEF)
    style_brief["style_id"] = args.style_id
    style_brief["narrative_mode"] = args.style_id

    output = clawdcut_dir / "style_brief.json"
    output.write_text(json.dumps(style_brief, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
