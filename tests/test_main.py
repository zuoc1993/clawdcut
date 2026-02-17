"""Tests for CLI entry point."""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from click.testing import CliRunner

from clawdcut.main import main


@pytest.fixture
def runner() -> CliRunner:
    """Create a Click test runner."""
    return CliRunner()


class TestMain:
    @patch("clawdcut.main.run_textual_app", new_callable=AsyncMock, return_value=0)
    @patch("clawdcut.main.create_director_agent")
    def test_creates_clawdcut_directory(
        self,
        mock_create_agent: MagicMock,
        mock_run_app: AsyncMock,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        mock_create_agent.return_value = MagicMock()
        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            runner.invoke(main)
            clawdcut_dir = Path(td) / ".clawdcut"
            assert clawdcut_dir.exists()

    @patch("clawdcut.main.run_textual_app", new_callable=AsyncMock, return_value=0)
    @patch("clawdcut.main.create_director_agent")
    def test_creates_asset_subdirectories(
        self,
        mock_create_agent: MagicMock,
        mock_run_app: AsyncMock,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        mock_create_agent.return_value = MagicMock()
        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            runner.invoke(main)
            assets = Path(td) / ".clawdcut" / "assets"
            assert (assets / "images").exists()
            assert (assets / "videos").exists()
            assert (assets / "audio").exists()

    @patch("clawdcut.main.run_textual_app", new_callable=AsyncMock, return_value=0)
    @patch("clawdcut.main.create_director_agent")
    def test_calls_create_director_agent_with_cwd(
        self,
        mock_create_agent: MagicMock,
        mock_run_app: AsyncMock,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        mock_create_agent.return_value = MagicMock()
        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            runner.invoke(main)
            mock_create_agent.assert_called_once()
            call_args = mock_create_agent.call_args[0]
            assert call_args[0] == Path(td)

    @patch("clawdcut.main.run_textual_app", new_callable=AsyncMock, return_value=0)
    @patch("clawdcut.main.create_director_agent")
    def test_calls_run_textual_app_with_agent(
        self,
        mock_create_agent: MagicMock,
        mock_run_app: AsyncMock,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        sentinel_agent = MagicMock()
        mock_create_agent.return_value = sentinel_agent
        with runner.isolated_filesystem(temp_dir=tmp_path):
            runner.invoke(main)
            mock_run_app.assert_called_once()
            call_kwargs = mock_run_app.call_args[1]
            assert call_kwargs["agent"] is sentinel_agent

    @patch("clawdcut.main.run_textual_app", new_callable=AsyncMock, return_value=0)
    @patch("clawdcut.main.create_director_agent")
    def test_passes_cwd_to_run_textual_app(
        self,
        mock_create_agent: MagicMock,
        mock_run_app: AsyncMock,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        mock_create_agent.return_value = MagicMock()
        with runner.isolated_filesystem(temp_dir=tmp_path) as td:
            runner.invoke(main)
            call_kwargs = mock_run_app.call_args[1]
            assert call_kwargs["cwd"] == Path(td)

    @patch("clawdcut.main.run_textual_app", new_callable=AsyncMock, return_value=0)
    @patch("clawdcut.main.create_director_agent")
    def test_exits_cleanly(
        self,
        mock_create_agent: MagicMock,
        mock_run_app: AsyncMock,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        mock_create_agent.return_value = MagicMock()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(main)
            assert result.exit_code == 0

    @patch("clawdcut.main.run_textual_app", new_callable=AsyncMock, return_value=0)
    @patch("clawdcut.main.create_director_agent")
    def test_idempotent_directory_creation(
        self,
        mock_create_agent: MagicMock,
        mock_run_app: AsyncMock,
        runner: CliRunner,
        tmp_path: Path,
    ) -> None:
        """Running main twice should not fail on existing directories."""
        mock_create_agent.return_value = MagicMock()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            runner.invoke(main)
            result = runner.invoke(main)
            assert result.exit_code == 0
