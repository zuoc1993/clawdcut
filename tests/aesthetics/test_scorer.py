"""Tests for aesthetic scorer."""

from clawdcut.aesthetics.scorer import score_aesthetics
from clawdcut.aesthetics.types import StyleBrief


def test_scores_higher_for_cinematic_terms() -> None:
    brief = StyleBrief.cinematic_default()
    high = score_aesthetics(
        script_text="A warm cinematic emotional story with gentle pacing.",
        storyboard_text="Slow zoom, dissolve transitions, rule of thirds.",
        style_brief=brief,
    )
    low = score_aesthetics(
        script_text="Random chaotic flashy style",
        storyboard_text="Hard cuts everywhere and mixed tones",
        style_brief=brief,
    )

    assert high.overall > low.overall
    assert high.consistency >= low.consistency


def test_reports_issues_when_score_low() -> None:
    brief = StyleBrief.cinematic_default()
    result = score_aesthetics(
        script_text="",
        storyboard_text="",
        style_brief=brief,
    )
    assert result.overall < 60
    assert len(result.issues) > 0
    assert len(result.fix_suggestions) > 0
