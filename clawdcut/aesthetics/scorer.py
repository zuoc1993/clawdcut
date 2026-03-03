"""Heuristic aesthetic scoring based on script and storyboard text."""

from clawdcut.aesthetics.types import AestheticScore, StyleBrief

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


def _count_matches(text: str, keywords: set[str]) -> int:
    source = text.lower()
    return sum(1 for kw in keywords if kw in source)


def score_aesthetics(
    script_text: str,
    storyboard_text: str,
    style_brief: StyleBrief,
) -> AestheticScore:
    """Generate a lightweight score report for aesthetic alignment."""
    combined = f"{script_text}\n{storyboard_text}".strip().lower()
    if not combined:
        return AestheticScore(
            overall=25.0,
            consistency=25.0,
            cinematicity=20.0,
            composition=30.0,
            color_harmony=25.0,
            motion_rhythm=25.0,
            issues=[
                "Insufficient script/storyboard aesthetic detail.",
                "Unable to verify cinematic consistency.",
            ],
            fix_suggestions=[
                "Add explicit color grading and transition intent per scene.",
                "Specify camera language and composition targets per shot.",
            ],
        )

    style_keywords: set[str] = set()
    raw_keywords = style_brief.palette.get("keywords", [])
    if isinstance(raw_keywords, list):
        style_keywords = {str(k).lower() for k in raw_keywords}
    cinematic_hits = _count_matches(combined, _CINEMATIC_HINTS | style_keywords)
    anti_hits = _count_matches(combined, _ANTI_HINTS)

    base = 60 + cinematic_hits * 4 - anti_hits * 6
    consistency = max(0.0, min(100.0, base))
    cinematicity = max(0.0, min(100.0, base + 2))
    composition = max(0.0, min(100.0, 55 + cinematic_hits * 3 - anti_hits * 4))
    color_harmony = max(0.0, min(100.0, 58 + cinematic_hits * 3 - anti_hits * 5))
    motion_rhythm = max(0.0, min(100.0, 56 + cinematic_hits * 3 - anti_hits * 4))
    overall = round(
        (
            consistency
            + cinematicity
            + composition
            + color_harmony
            + motion_rhythm
        )
        / 5,
        2,
    )

    issues: list[str] = []
    suggestions: list[str] = []
    if anti_hits > 0:
        issues.append("Detected anti-cinematic cues (flashy/glitch/hard-cut).")
        suggestions.append("Reduce aggressive transitions and random pacing.")
    if cinematic_hits < 3:
        issues.append("Cinematic signals are sparse.")
        suggestions.append(
            "Add color, composition, and motion intent in script/storyboard."
        )
    if not issues:
        issues.append("No major aesthetic violations detected.")
        suggestions.append("Preserve current style consistency during iteration.")

    return AestheticScore(
        overall=overall,
        consistency=round(consistency, 2),
        cinematicity=round(cinematicity, 2),
        composition=round(composition, 2),
        color_harmony=round(color_harmony, 2),
        motion_rhythm=round(motion_rhythm, 2),
        issues=issues,
        fix_suggestions=suggestions,
    )
