"""Typed models for project-level aesthetic decisions and scoring."""

from pydantic import BaseModel, Field


class StyleBrief(BaseModel):
    """Project-level aesthetic contract shared across all agents."""

    style_id: str
    narrative_mode: str
    palette: dict[str, object]
    grading_preset: str
    camera_language: dict[str, object]
    transition_language: dict[str, object]
    composition_rules: dict[str, object]
    atmosphere_rules: dict[str, object]
    typography_rules: dict[str, object]
    music_profile: dict[str, object]
    hard_constraints: list[str]

    @classmethod
    def cinematic_default(cls) -> "StyleBrief":
        """Create the default cinematic style profile."""
        return cls(
            style_id="cinematic_story",
            narrative_mode="cinematic_story",
            palette={
                "primary": ["#1F2A44", "#D9A066", "#F2E9DC"],
                "keywords": ["cinematic", "warm", "natural", "moody"],
                "forbidden": ["neon-purple-heavy", "oversaturated-green"],
            },
            grading_preset="cinematic_warm",
            camera_language={
                "preferred": ["slow-zoom-in", "pan", "tracking"],
                "forbidden": ["shake-heavy", "random-orbit"],
            },
            transition_language={
                "preferred": ["dissolve", "fade-to-black", "wipe-left"],
                "forbidden": ["hard-cut", "glitch"],
                "max_density": 0.25,
            },
            composition_rules={
                "preferred": ["rule-of-thirds", "center-weighted"],
                "safe_margin": 0.08,
            },
            atmosphere_rules={
                "vignette": 0.25,
                "grain": 0.08,
                "light_leak": 0.1,
            },
            typography_rules={
                "title_style": "elegant-serif",
                "body_style": "clean-sans",
                "animation": "fade-slide-up",
            },
            music_profile={
                "curve": "gentle-rise",
                "dynamic_range": "medium",
            },
            hard_constraints=[
                "avoid visual clutter",
                "maintain color harmony",
                "preserve narrative pacing",
            ],
        )


class AestheticScore(BaseModel):
    """Scored breakdown for aesthetic quality and consistency."""

    overall: float = Field(ge=0.0, le=100.0)
    consistency: float = Field(ge=0.0, le=100.0)
    cinematicity: float = Field(ge=0.0, le=100.0)
    composition: float = Field(ge=0.0, le=100.0)
    color_harmony: float = Field(ge=0.0, le=100.0)
    motion_rhythm: float = Field(ge=0.0, le=100.0)
    issues: list[str]
    fix_suggestions: list[str]

