# Clawdcut

AI autonomous video editing tool - a tribute to clawdbot.

Clawdcut is an intelligent video creation assistant that transforms your creative ideas into production-ready video projects through natural dialogue. It acts as your personal AI film director, handling everything from concept development to asset acquisition.

## Features

- **AI Director Agent**: An experienced film director that understands your creative vision through conversation
- **Creative Scripting**: Generates professional video scripts with scene descriptions, narration, and emotional arcs
- **Storyboard Design**: Creates detailed shot lists with camera movements, angles, and visual composition
- **Asset Management**: Automatically searches and downloads free stock media from Pexels and Pixabay
- **Project Memory**: Maintains context across sessions with persistent project memory
- **Remotion Integration**: Built-in best practices for Remotion video production in React

## Installation

```bash
uv tool install clawdcut
```

Or install from source:

```bash
git clone <repository-url>
cd clawdcut
uv sync --extra dev
```

## Quick Start

1. **Set up API keys** (for stock media search):
```bash
export PEXELS_API_KEY="your-pexels-api-key"
export PIXABAY_API_KEY="your-pixabay-api-key"
```

2. **Run Clawdcut**:
```bash
clawdcut
```

3. **Start creating**: Tell the Director what video you want to make, and it will guide you through the entire creative process.

## Workflow

Clawdcut follows a professional 7-phase video production workflow:

1. **Discovery** - Understand your creative intent through dialogue
2. **Concept** - Transform requirements into concrete creative proposals
3. **Scripting** - Generate detailed video scripts with timing and narration
4. **Asset Planning** - Determine all required media assets
5. **Asset Acquisition** - Search and download free stock media
6. **Storyboard** - Create detailed shot lists with camera specifications
7. **Iteration** - Refine based on feedback until satisfied

## Project Structure

When you run Clawdcut in a directory, it creates a `.clawdcut/` folder:

```
.clawdcut/
├── AGENTS.md          # Project memory and preferences
├── script.md          # Generated video script
├── storyboard.md      # Visual shot list
└── assets/
    ├── images/        # Downloaded images
    ├── videos/        # Downloaded videos
    └── audio/         # Downloaded audio
```

## Configuration

### Environment Variables

- `CLAWDCUT_MODEL` - Override the default LLM model (e.g., `openai:glm-5`)
- `OPENAI_MODEL` - Use OpenAI models (auto-prefixed with `openai:`)
- `ANTHROPIC_MODEL` - Use Anthropic models (auto-prefixed with `anthropic:`)
- `ANTHROPIC_BASE_URL` - Optional base URL for Anthropic-compatible third-party API
- `PEXELS_API_KEY` - Pexels API key for stock photos/videos
- `PIXABAY_API_KEY` - Pixabay API key for stock media

### Model Support

By default, Clawdcut uses Claude via the deepagents framework. You can configure other models:

```bash
# Use OpenAI models
export OPENAI_MODEL="gpt-4o"

# Use Anthropic models
export ANTHROPIC_MODEL="claude-3-5-sonnet-latest"

# Anthropic-compatible third-party endpoint
export ANTHROPIC_MODEL="claude-3-5-sonnet-latest"
export ANTHROPIC_BASE_URL="https://your-provider.example/v1"

# Or explicitly set any model
export CLAWDCUT_MODEL="openai:glm-5"
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd clawdcut

# Install with dev dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Run type checking
uv run mypy clawdcut
```

### Project Structure

```
clawdcut/
├── agents/           # AI agents
│   ├── director.py   # Main director agent
│   └── asset_manager.py  # Asset acquisition subagent
├── tools/            # External API tools
│   └── stock_tools.py    # Pexels/Pixabay integration
├── skills/           # Domain-specific skills
│   ├── creative-scripting/   # Script writing skill
│   ├── storyboard-design/    # Storyboard design skill
│   └── remotion-best-practices/  # Remotion video skill
└── main.py          # CLI entry point
```

## Skills

Clawdcut includes specialized skills for video production:

### Creative Scripting
Transforms creative intent into production-ready narration with emotional storytelling and precise timing alignment.

### Storyboard Design
Converts scripts into visual shot plans with camera movements, angles, and compositional references.

### Remotion Best Practices
Comprehensive guidelines for Remotion video creation including animations, audio, transitions, captions, and more.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Clawdcut is inspired by and a tribute to clawdbot, bringing AI-powered video creation to everyone.
