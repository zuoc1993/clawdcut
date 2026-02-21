"""Tests for Asset Manager SubAgent."""

from pathlib import Path

import pytest

from clawdcut.agents.asset_manager import create_asset_manager_subagent


@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    """Create a temporary working directory."""
    return tmp_path


@pytest.fixture
def subagent(workdir: Path) -> dict:
    """Create an Asset Manager SubAgent spec."""
    return create_asset_manager_subagent(workdir)


class TestCreateAssetManagerSubagent:
    def test_returns_dict(self, subagent: dict) -> None:
        assert isinstance(subagent, dict)

    def test_has_required_fields(self, subagent: dict) -> None:
        assert "name" in subagent
        assert "description" in subagent
        assert "system_prompt" in subagent

    def test_name_is_asset_manager(self, subagent: dict) -> None:
        assert subagent["name"] == "asset-manager"

    def test_description_mentions_assets(self, subagent: dict) -> None:
        desc = subagent["description"]
        assert len(desc) > 0
        assert "asset" in desc.lower() or "素材" in desc

    def test_system_prompt_is_nonempty(self, subagent: dict) -> None:
        assert len(subagent["system_prompt"]) > 0

    def test_system_prompt_contains_workflow(self, subagent: dict) -> None:
        prompt = subagent["system_prompt"]
        assert "pexels" in prompt.lower() or "pixabay" in prompt.lower()

    def test_has_tools(self, subagent: dict) -> None:
        assert "tools" in subagent
        tools = subagent["tools"]
        assert len(tools) == 6

    def test_tool_names(self, subagent: dict) -> None:
        tool_names = [t.__name__ for t in subagent["tools"]]
        assert "pexels_search" in tool_names
        assert "pexels_download" in tool_names
        assert "pixabay_search" in tool_names
        assert "pixabay_download" in tool_names
        assert "freesound_search" in tool_names
        assert "freesound_download" in tool_names

    def test_tools_bound_to_workdir(self, subagent: dict, workdir: Path) -> None:
        """Verify download tools save files relative to workdir."""
        from unittest.mock import patch

        tools = {t.__name__: t for t in subagent["tools"]}
        with patch("clawdcut.tools.stock_tools.httpx.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.raise_for_status.return_value = None
            mock_get.return_value.content = b"test-data"

            tools["pexels_download"](
                "https://example.com/test.jpg",
                ".clawdcut/assets/images/test.jpg",
            )

        target = workdir / ".clawdcut/assets/images/test.jpg"
        assert target.exists()
        assert target.read_bytes() == b"test-data"
