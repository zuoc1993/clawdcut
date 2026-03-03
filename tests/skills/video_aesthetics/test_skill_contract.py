"""Contract tests for video-aesthetics skill content."""

from pathlib import Path


def test_skill_mentions_scripts_and_threshold() -> None:
    skill = Path("clawdcut/skills/video-aesthetics/SKILL.md").read_text().lower()
    assert "scripts/build_style_brief.py" in skill
    assert "scripts/validate_style_brief.py" in skill
    assert "scripts/score_aesthetics.py" in skill
    assert "overall >= 75" in skill or "threshold: 75" in skill
