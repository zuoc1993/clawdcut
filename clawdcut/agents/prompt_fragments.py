"""Shared prompt fragments for Clawdcut agents.

Keep repeated operational rules in one place to avoid drift across prompts.
"""

BUILD_STYLE_BRIEF_CMD = (
    "python clawdcut/skills/video-aesthetics/scripts/build_style_brief.py --workdir ."
)
VALIDATE_STYLE_BRIEF_CMD = (
    "python clawdcut/skills/video-aesthetics/scripts/"
    "validate_style_brief.py --style-brief .clawdcut/style_brief.json"
)
SCORE_AESTHETICS_CMD = (
    "python clawdcut/skills/video-aesthetics/scripts/"
    "score_aesthetics.py --project-dir . --threshold 75"
)

WRITE_FILE_STRING_RULE = """\
- **CRITICAL for tool calls**: `write_file`'s `content` must be a plain string.
  - Never pass a Python/JSON object directly to `content`.
  - For JSON files, serialize first, then write the serialized text.
  - Good pattern:
    1. Build style brief object in reasoning
    2. Convert to JSON text with indentation
    3. Call `write_file(file_path='.clawdcut/style_brief.json', content='<json text>')`
  - Bad pattern: `content={...}` (this will fail with "Input should be a valid string")
"""
