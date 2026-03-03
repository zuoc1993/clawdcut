---
name: video-aesthetics
description: Use when defining, validating, or enforcing project visual style in Clawdcut, especially before asset acquisition, storyboard finalization, and Remotion code generation.
metadata:
  tags: aesthetics, color-grading, transitions, composition, cinematography, visual-design
---

# Video Aesthetics Skill

## Overview
This skill enforces cinematic style with executable scripts, not just prose guidance.

## Required Scripts
- `scripts/build_style_brief.py`
- `scripts/validate_style_brief.py`
- `scripts/score_aesthetics.py`

## Required Execution Gates
1. Concept finalized:
```bash
python clawdcut/skills/video-aesthetics/scripts/build_style_brief.py --workdir .
python clawdcut/skills/video-aesthetics/scripts/validate_style_brief.py --style-brief .clawdcut/style_brief.json
```

2. Storyboard completed:
```bash
python clawdcut/skills/video-aesthetics/scripts/score_aesthetics.py --project-dir . --threshold 75
```

3. Before Remotion generation:
```bash
python clawdcut/skills/video-aesthetics/scripts/validate_style_brief.py --style-brief .clawdcut/style_brief.json
python clawdcut/skills/video-aesthetics/scripts/score_aesthetics.py --project-dir . --threshold 75
```

## Pass Criteria
- `overall >= 75`
- If `overall < 75`, do not proceed. Fix storyboard/style decisions and score again.

## Output Artifacts
- `.clawdcut/style_brief.json`
- `.clawdcut/aesthetic_score.json`
- `.clawdcut/aesthetic_report.md`

## Style Defaults
- `style_id`: `cinematic_story`
- Avoid high-noise style drift and excessive hard cuts.
- Prioritize coherent color harmony, composition clarity, and gentle narrative rhythm.

## Related Rules
- [rules/color-grading.md](./rules/color-grading.md)
- [rules/transitions.md](./rules/transitions.md)
- [rules/camera-motion.md](./rules/camera-motion.md)
- [rules/composition.md](./rules/composition.md)
