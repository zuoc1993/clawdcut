"""Tests for Director Agent."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from clawdcut.agents.director import (
    DIRECTOR_SYSTEM_PROMPT,
    SKILLS_DIR,
    _resolve_model,
    create_director_agent,
)


@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    """Create a temporary working directory."""
    return tmp_path


class TestDirectorSystemPrompt:
    def test_prompt_is_nonempty(self) -> None:
        assert len(DIRECTOR_SYSTEM_PROMPT) > 0

    def test_prompt_mentions_director_role(self) -> None:
        assert "Director" in DIRECTOR_SYSTEM_PROMPT or "导演" in DIRECTOR_SYSTEM_PROMPT

    def test_prompt_mentions_script(self) -> None:
        prompt = DIRECTOR_SYSTEM_PROMPT
        assert "script" in prompt.lower() or "脚本" in prompt

    def test_prompt_mentions_storyboard(self) -> None:
        assert (
            "storyboard" in DIRECTOR_SYSTEM_PROMPT.lower()
            or "分镜" in DIRECTOR_SYSTEM_PROMPT
        )

    def test_prompt_mentions_clawdcut_dir(self) -> None:
        assert ".clawdcut" in DIRECTOR_SYSTEM_PROMPT

    def test_prompt_mentions_asset_manager(self) -> None:
        assert (
            "asset-manager" in DIRECTOR_SYSTEM_PROMPT.lower()
            or "asset manager" in DIRECTOR_SYSTEM_PROMPT.lower()
            or "素材" in DIRECTOR_SYSTEM_PROMPT
        )

    def test_prompt_mentions_audio_types(self) -> None:
        prompt = DIRECTOR_SYSTEM_PROMPT.lower()
        assert "audio_type" in prompt
        assert "music" in prompt
        assert "sfx" in prompt


class TestSkillsDir:
    def test_skills_dir_exists(self) -> None:
        assert SKILLS_DIR.exists(), f"Skills directory does not exist: {SKILLS_DIR}"

    def test_skills_dir_has_creative_scripting(self) -> None:
        assert (SKILLS_DIR / "creative-scripting" / "SKILL.md").exists()

    def test_skills_dir_has_storyboard_design(self) -> None:
        assert (SKILLS_DIR / "storyboard-design" / "SKILL.md").exists()


class TestResolveModel:
    def test_returns_none_without_env_vars(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("CLAWDCUT_MODEL", raising=False)
        monkeypatch.delenv("OPENAI_MODEL", raising=False)
        monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)
        monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
        assert _resolve_model() is None

    def test_uses_clawdcut_model_first(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CLAWDCUT_MODEL", "anthropic:claude-haiku")
        monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")
        monkeypatch.setenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
        monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
        assert _resolve_model() == "anthropic:claude-haiku"

    @patch("clawdcut.agents.director.init_chat_model")
    def test_uses_openai_model_before_anthropic_model(
        self,
        mock_init_chat_model: MagicMock,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        sentinel_model = MagicMock()
        mock_init_chat_model.return_value = sentinel_model
        monkeypatch.delenv("CLAWDCUT_MODEL", raising=False)
        monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
        monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")
        monkeypatch.setenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")

        result = _resolve_model()

        assert result is sentinel_model
        mock_init_chat_model.assert_called_once_with(
            "openai:gpt-4o",
            max_tokens=8192,
        )

    def test_uses_anthropic_model_when_set(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("CLAWDCUT_MODEL", raising=False)
        monkeypatch.delenv("OPENAI_MODEL", raising=False)
        monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
        monkeypatch.setenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")

        assert _resolve_model() == "anthropic:claude-3-5-sonnet-latest"

    @patch("clawdcut.agents.director.init_chat_model")
    def test_uses_anthropic_base_url_with_init_chat_model(
        self, mock_init_chat_model: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        sentinel_model = MagicMock()
        mock_init_chat_model.return_value = sentinel_model
        monkeypatch.delenv("CLAWDCUT_MODEL", raising=False)
        monkeypatch.delenv("OPENAI_MODEL", raising=False)
        monkeypatch.setenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
        monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://example.com/v1")

        result = _resolve_model()

        assert result is sentinel_model
        mock_init_chat_model.assert_called_once_with(
            "anthropic:claude-3-5-sonnet-latest",
            base_url="https://example.com/v1",
            max_tokens=8192,
        )


class TestCreateDirectorAgent:
    @patch("clawdcut.agents.director.create_deep_agent")
    def test_calls_create_deep_agent(
        self, mock_create: MagicMock, workdir: Path
    ) -> None:
        mock_create.return_value = MagicMock()
        create_director_agent(workdir)
        mock_create.assert_called_once()

    @patch("clawdcut.agents.director.create_deep_agent")
    def test_passes_system_prompt(self, mock_create: MagicMock, workdir: Path) -> None:
        mock_create.return_value = MagicMock()
        create_director_agent(workdir)
        kwargs = mock_create.call_args[1]
        assert "system_prompt" in kwargs
        assert len(kwargs["system_prompt"]) > 0

    @patch("clawdcut.agents.director.create_deep_agent")
    def test_passes_subagents_with_asset_manager(
        self, mock_create: MagicMock, workdir: Path
    ) -> None:
        mock_create.return_value = MagicMock()
        create_director_agent(workdir)
        kwargs = mock_create.call_args[1]
        assert "subagents" in kwargs
        subagents = kwargs["subagents"]
        assert len(subagents) >= 1
        asset_mgr = subagents[0]
        assert asset_mgr["name"] == "asset-manager"

    @patch("clawdcut.agents.director.create_deep_agent")
    def test_passes_skills_directory(
        self, mock_create: MagicMock, workdir: Path
    ) -> None:
        mock_create.return_value = MagicMock()
        create_director_agent(workdir)
        kwargs = mock_create.call_args[1]
        assert "skills" in kwargs
        skills = kwargs["skills"]
        assert len(skills) > 0
        assert str(SKILLS_DIR) in skills[0]

    @patch("clawdcut.agents.director.create_deep_agent")
    def test_passes_backend(self, mock_create: MagicMock, workdir: Path) -> None:
        mock_create.return_value = MagicMock()
        create_director_agent(workdir)
        kwargs = mock_create.call_args[1]
        assert "backend" in kwargs
        assert kwargs["backend"] is not None

    @patch("clawdcut.agents.director.create_deep_agent")
    def test_passes_checkpointer(self, mock_create: MagicMock, workdir: Path) -> None:
        mock_create.return_value = MagicMock()
        create_director_agent(workdir)
        kwargs = mock_create.call_args[1]
        assert "checkpointer" in kwargs
        assert kwargs["checkpointer"] is not None

    @patch("clawdcut.agents.director.create_deep_agent")
    def test_passes_memory_in_clawdcut_dir(
        self, mock_create: MagicMock, workdir: Path
    ) -> None:
        mock_create.return_value = MagicMock()
        create_director_agent(workdir)
        kwargs = mock_create.call_args[1]
        assert "memory" in kwargs
        assert len(kwargs["memory"]) > 0
        memory_path = kwargs["memory"][0]
        assert ".clawdcut" in memory_path
        assert memory_path.endswith("AGENTS.md")

    @patch("clawdcut.agents.director.create_deep_agent")
    def test_returns_agent(self, mock_create: MagicMock, workdir: Path) -> None:
        sentinel = MagicMock()
        mock_create.return_value = sentinel
        result = create_director_agent(workdir)
        assert result is sentinel
