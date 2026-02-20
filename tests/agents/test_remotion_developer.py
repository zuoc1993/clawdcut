"""Tests for Remotion Developer SubAgent."""

from pathlib import Path

import pytest

from clawdcut.agents.remotion_developer import create_remotion_developer_subagent


@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    """Create a temporary working directory."""
    return tmp_path


@pytest.fixture
def subagent(workdir: Path) -> dict:
    """Create a Remotion Developer SubAgent spec."""
    return create_remotion_developer_subagent(workdir)


class TestCreateRemotionDeveloperSubagent:
    def test_returns_dict(self, subagent: dict) -> None:
        assert isinstance(subagent, dict)

    def test_has_required_fields(self, subagent: dict) -> None:
        assert "name" in subagent
        assert "description" in subagent
        assert "system_prompt" in subagent
        assert "tools" in subagent

    def test_name_is_remotion_developer(self, subagent: dict) -> None:
        assert subagent["name"] == "remotion-developer"

    def test_description_mentions_remotion(self, subagent: dict) -> None:
        desc = subagent["description"]
        assert len(desc) > 0
        assert "remotion" in desc.lower()

    def test_description_mentions_storyboard(self, subagent: dict) -> None:
        desc = subagent["description"]
        assert "storyboard" in desc.lower() or "storyboard" in desc

    def test_description_mentions_typescript(self, subagent: dict) -> None:
        desc = subagent["description"]
        assert "typescript" in desc.lower() or "react" in desc.lower()

    def test_system_prompt_is_nonempty(self, subagent: dict) -> None:
        assert len(subagent["system_prompt"]) > 0

    def test_system_prompt_contains_identity(self, subagent: dict) -> None:
        prompt = subagent["system_prompt"]
        assert "<identity>" in prompt

    def test_system_prompt_contains_workflow(self, subagent: dict) -> None:
        prompt = subagent["system_prompt"]
        assert "<workflow>" in prompt

    def test_system_prompt_contains_coding_standards(self, subagent: dict) -> None:
        prompt = subagent["system_prompt"]
        assert "<coding_standards>" in prompt

    def test_system_prompt_contains_tool_usage(self, subagent: dict) -> None:
        prompt = subagent["system_prompt"]
        assert "<tool_usage>" in prompt

    def test_system_prompt_mentions_react(self, subagent: dict) -> None:
        prompt = subagent["system_prompt"]
        assert "react" in prompt.lower()

    def test_system_prompt_mentions_typescript(self, subagent: dict) -> None:
        prompt = subagent["system_prompt"]
        assert "typescript" in prompt.lower()

    def test_system_prompt_mentions_studio(self, subagent: dict) -> None:
        prompt = subagent["system_prompt"]
        assert "studio" in prompt.lower()

    def test_tools_is_list(self, subagent: dict) -> None:
        """Remotion developer uses Bash and Read tools from deepagents."""
        tools = subagent["tools"]
        assert isinstance(tools, list)

    def test_has_skills(self, subagent: dict) -> None:
        """Remotion developer should have skills configured."""
        assert "skills" in subagent
        skills = subagent["skills"]
        assert isinstance(skills, list)
        assert len(skills) > 0
