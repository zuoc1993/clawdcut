"""CLI entry point for Clawdcut."""

import asyncio
from pathlib import Path

import click
from deepagents_cli.app import run_textual_app
from dotenv import load_dotenv

from clawdcut import __version__
from clawdcut.agents.director import create_director_agent

load_dotenv()


_DEFAULT_MEMORY = """\
# Clawdcut Project Memory

This file stores project-specific context for the Director agent.
The Director can update this file to remember user preferences,
project decisions, and creative direction across sessions.
"""


def _ensure_workdir(workdir: Path) -> None:
    """Create .clawdcut/ directory structure if it doesn't exist."""
    clawdcut_dir = workdir / ".clawdcut"
    clawdcut_dir.mkdir(exist_ok=True)
    (clawdcut_dir / "assets" / "images").mkdir(parents=True, exist_ok=True)
    (clawdcut_dir / "assets" / "videos").mkdir(parents=True, exist_ok=True)
    (clawdcut_dir / "assets" / "audio").mkdir(parents=True, exist_ok=True)

    memory_file = clawdcut_dir / "AGENTS.md"
    if not memory_file.exists():
        memory_file.write_text(_DEFAULT_MEMORY)


@click.command()
@click.version_option(version=__version__, prog_name="clawdcut")
def main() -> None:
    """Clawdcut - AI autonomous video editing tool."""
    workdir = Path.cwd()
    _ensure_workdir(workdir)

    agent = create_director_agent(workdir)
    asyncio.run(run_textual_app(agent=agent, cwd=workdir))


if __name__ == "__main__":
    main()
