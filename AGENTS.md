# AGENTS.md

## Project Overview

**Clawdcut** is an AI autonomous video editing tool built with Python. It uses a multi-agent architecture where a Director agent coordinates with an Asset Manager subagent to help users create video projects from concept to production.

## Architecture

### Core Components

1. **Director Agent** (`clawdcut/agents/director.py`)
   - Main orchestrator with 7-phase workflow (Discovery → Concept → Scripting → Asset Planning → Asset Acquisition → Storyboard → Iteration)
   - Uses LangGraph with MemorySaver for conversation continuity
   - Loads skills from `clawdcut/skills/` directory
   - Maintains project state in `.clawdcut/AGENTS.md`

2. **Asset Manager SubAgent** (`clawdcut/agents/asset_manager.py`)
   - Specialized subagent for stock media acquisition
   - Integrates with Pexels and Pixabay APIs
   - Organizes downloaded assets into `.clawdcut/assets/{images,videos,audio}/`

3. **Stock Tools** (`clawdcut/tools/stock_tools.py`)
   - HTTP clients for Pexels and Pixabay APIs
   - Search and download functionality for photos/videos

4. **Skills** (`clawdcut/skills/`)
   - `creative-scripting/` - Video script writing patterns
   - `storyboard-design/` - Shot list and camera movement planning
   - `remotion-best-practices/` - Video production best practices

## Development Guidelines

### Code Style

- **Line Length**: 88 characters (Black/Ruff default)
- **Python Version**: 3.12+
- **Type Hints**: Use full type annotations
- **Imports**: Sorted with Ruff (isort rules)

### Linting & Type Checking

```bash
# Run all checks
uv run ruff check .
uv run mypy clawdcut

# Format code
uv run black clawdcut
uv run ruff check --fix .
```

### Testing

```bash
# Run tests
uv run pytest

# With coverage
uv run pytest --cov=clawdcut --cov-report=html
```

### Project Conventions

1. **Agent System Prompts**: Stored as multiline strings with XML-style tags for structure
2. **Skills**: Use YAML frontmatter with `name`, `description`, and `metadata.tags`
3. **File Paths**: Use `pathlib.Path` for all filesystem operations
4. **Environment Config**: Use `python-dotenv` for loading `.env` files
5. **Async**: Use `asyncio` for async operations (required by deepagents)

## Key Files

| File | Purpose |
|------|---------|
| `clawdcut/main.py` | CLI entry point using Click |
| `clawdcut/agents/director.py` | Director agent configuration and workflow |
| `clawdcut/agents/asset_manager.py` | Asset manager subagent |
| `clawdcut/tools/stock_tools.py` | Pexels/Pixabay API tools |
| `pyproject.toml` | Package configuration, dependencies, tool settings |
| `.clawdcut/AGENTS.md` | Runtime project memory (per-project) |

## Dependencies

### Core
- `deepagents-cli` - AI agent framework
- `langchain` + `langgraph` - LLM orchestration
- `httpx` - HTTP client for APIs
- `pydantic` - Data validation
- `click` - CLI framework

### APIs
- Pexels API (requires `PEXELS_API_KEY`)
- Pixabay API (requires `PIXABAY_API_KEY`)

### Development
- `pytest` + `pytest-cov` - Testing
- `black` - Code formatting
- `ruff` - Linting
- `mypy` - Type checking

## Common Tasks

### Adding a New Tool

1. Add tool function in `clawdcut/tools/`
2. Update `create_stock_tools()` or create new tool factory
3. Register tool in the appropriate agent's system prompt
4. Add tests in `tests/tools/`

### Adding a New Skill

1. Create `clawdcut/skills/<skill-name>/SKILL.md`
2. Add YAML frontmatter with name and description
3. Write clear usage instructions with examples
4. Reference the skill in Director's system prompt if needed

### Modifying Agent Behavior

1. Edit system prompt in `clawdcut/agents/director.py` or `asset_manager.py`
2. Update `<capabilities>`, `<workflow>`, or `<tool_usage>` sections
3. Test with actual conversations to verify behavior

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `CLAWDCUT_MODEL` | Explicit model override | `openai:glm-5` |
| `OPENAI_MODEL` | OpenAI model selection | `gpt-4o` |
| `ANTHROPIC_MODEL` | Anthropic model selection | `claude-3-5-sonnet-latest` |
| `ANTHROPIC_BASE_URL` | Anthropic-compatible third-party endpoint | `https://provider.example/v1` |
| `PEXELS_API_KEY` | Pexels API access | `your-api-key` |
| `PIXABAY_API_KEY` | Pixabay API access | `your-api-key` |

## Notes for AI Assistants

- When modifying agent code, maintain the XML-style structure in system prompts
- Skills use markdown with YAML frontmatter - preserve this format
- The Director agent manages project memory in `.clawdcut/AGENTS.md` at runtime
- Always run tests and linting before committing changes
- Use type hints for all new functions
- Prefer `pathlib.Path` over string paths
