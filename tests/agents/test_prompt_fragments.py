"""Tests for shared prompt fragments across agents."""

from clawdcut.agents.director import DIRECTOR_SYSTEM_PROMPT
from clawdcut.agents.prompt_fragments import (
    BUILD_STYLE_BRIEF_CMD,
    SCORE_AESTHETICS_CMD,
    VALIDATE_STYLE_BRIEF_CMD,
    WRITE_FILE_STRING_RULE,
)
from clawdcut.agents.remotion_developer import REMOTION_DEVELOPER_SYSTEM_PROMPT


def test_director_uses_shared_aesthetic_commands() -> None:
    assert BUILD_STYLE_BRIEF_CMD in DIRECTOR_SYSTEM_PROMPT
    assert VALIDATE_STYLE_BRIEF_CMD in DIRECTOR_SYSTEM_PROMPT
    assert SCORE_AESTHETICS_CMD in DIRECTOR_SYSTEM_PROMPT


def test_remotion_uses_shared_aesthetic_commands() -> None:
    assert VALIDATE_STYLE_BRIEF_CMD in REMOTION_DEVELOPER_SYSTEM_PROMPT
    assert SCORE_AESTHETICS_CMD in REMOTION_DEVELOPER_SYSTEM_PROMPT


def test_director_embeds_write_file_string_rule() -> None:
    assert WRITE_FILE_STRING_RULE.strip() in DIRECTOR_SYSTEM_PROMPT
