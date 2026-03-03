"""Tests for aesthetics typed models."""

from clawdcut.aesthetics.types import AestheticScore, StyleBrief


class TestStyleBrief:
    def test_builds_cinematic_default(self) -> None:
        brief = StyleBrief.cinematic_default()
        assert brief.style_id == "cinematic_story"
        assert brief.narrative_mode == "cinematic_story"
        assert "hard-cut" in brief.transition_language["forbidden"]


class TestAestheticScore:
    def test_supports_issue_and_suggestions(self) -> None:
        score = AestheticScore(
            overall=82.5,
            consistency=84.0,
            cinematicity=80.0,
            composition=83.0,
            color_harmony=81.0,
            motion_rhythm=86.0,
            issues=["Transitions too dense"],
            fix_suggestions=["Reduce transition frequency to <= 25% shots"],
        )
        assert score.overall > 80
        assert len(score.issues) == 1
