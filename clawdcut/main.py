"""CLI entry point for Clawdcut."""

import asyncio
import json
from pathlib import Path

import click
from deepagents_cli.app import run_textual_app
from dotenv import load_dotenv

from clawdcut import __version__
from clawdcut.agents.director import create_director_agent

load_dotenv(override=True)


_DEFAULT_MEMORY = """\
# Clawdcut Project Memory

This file stores project-specific context for the Director agent.
The Director can update this file to remember user preferences,
project decisions, and creative direction across sessions.
"""

_DEFAULT_AESTHETIC_REPORT = """\
# Aesthetic Report

- Status: initialized
- Overall Score: pending
- Notes: Generated after storyboard and style brief are ready.
"""

_DEFAULT_STYLE_BRIEF = {
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


def _ensure_workdir(workdir: Path) -> None:
    """Create .clawdcut/ directory structure if it doesn't exist."""
    clawdcut_dir = workdir / ".clawdcut"
    clawdcut_dir.mkdir(exist_ok=True)
    (clawdcut_dir / "assets" / "images").mkdir(parents=True, exist_ok=True)
    (clawdcut_dir / "assets" / "videos").mkdir(parents=True, exist_ok=True)
    (clawdcut_dir / "assets" / "audio").mkdir(parents=True, exist_ok=True)

    memory_file = clawdcut_dir / "AGENTS.md"
    if not memory_file.exists():
        memory_file.write_text(_DEFAULT_MEMORY)

    style_brief_file = clawdcut_dir / "style_brief.json"
    if not style_brief_file.exists():
        style_brief_file.write_text(
            json.dumps(_DEFAULT_STYLE_BRIEF, indent=2, ensure_ascii=False)
        )

    aesthetic_report_file = clawdcut_dir / "aesthetic_report.md"
    if not aesthetic_report_file.exists():
        aesthetic_report_file.write_text(_DEFAULT_AESTHETIC_REPORT)


@click.command()
@click.version_option(version=__version__, prog_name="clawdcut")
def main() -> None:
    """Clawdcut - AI autonomous video editing tool."""
    workdir = Path.cwd()
    _ensure_workdir(workdir)

    agent = create_director_agent(workdir)
    asyncio.run(run_textual_app(agent=agent, cwd=workdir))


if __name__ == "__main__":
    main()
