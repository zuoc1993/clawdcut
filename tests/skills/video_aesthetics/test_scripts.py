"""Tests for video-aesthetics executable scripts and skill contract."""

import json
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _script_path(name: str) -> Path:
    return _repo_root() / "clawdcut" / "skills" / "video-aesthetics" / "scripts" / name


def test_scripts_exist() -> None:
    assert _script_path("build_style_brief.py").exists()
    assert _script_path("validate_style_brief.py").exists()
    assert _script_path("score_aesthetics.py").exists()


def test_build_style_brief_script_generates_file(tmp_path: Path) -> None:
    workdir = tmp_path
    subprocess.run(
        [
            sys.executable,
            str(_script_path("build_style_brief.py")),
            "--workdir",
            str(workdir),
        ],
        check=True,
    )

    output = workdir / ".clawdcut" / "style_brief.json"
    assert output.exists()
    data = json.loads(output.read_text())
    assert data["style_id"] == "cinematic_story"


def test_validate_style_brief_script_fails_for_invalid_json(tmp_path: Path) -> None:
    style_file = tmp_path / "style_brief.json"
    style_file.write_text("{}")

    result = subprocess.run(
        [
            sys.executable,
            str(_script_path("validate_style_brief.py")),
            "--style-brief",
            str(style_file),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "missing required fields" in result.stderr.lower()


def test_score_aesthetics_script_generates_report(tmp_path: Path) -> None:
    project = tmp_path / "project"
    clawd = project / ".clawdcut"
    clawd.mkdir(parents=True)

    (clawd / "script.md").write_text(
        "A warm cinematic emotional story with gentle pacing."
    )
    (clawd / "storyboard.md").write_text(
        "Slow zoom, dissolve transitions, rule of thirds."
    )
    (clawd / "style_brief.json").write_text(
        json.dumps(
            {
                "style_id": "cinematic_story",
                "narrative_mode": "cinematic_story",
                "palette": {"keywords": ["cinematic", "warm", "moody"]},
                "transition_language": {"forbidden": ["hard-cut", "glitch"]},
                "hard_constraints": ["maintain color harmony"],
            }
        )
    )

    subprocess.run(
        [
            sys.executable,
            str(_script_path("score_aesthetics.py")),
            "--project-dir",
            str(project),
            "--threshold",
            "75",
        ],
        check=True,
    )

    report = clawd / "aesthetic_report.md"
    score_json = clawd / "aesthetic_score.json"
    assert report.exists()
    assert score_json.exists()

    payload = json.loads(score_json.read_text())
    assert "overall" in payload
    assert payload["overall"] >= 75
