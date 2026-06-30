# git-story 📖

CLI that generates human-readable narrative changelogs from git history using local LLMs via Ollama — no API keys needed.

## Quick Start

```bash
# Install
pip install -e .

# Last week's story
git story --since '1 week'

# Custom time range
git story --since '2026-06-01' --until '2026-06-30'

# Write to file
git story --since '1 week' -o CHANGELOG.md

# HTML output
git story --since '1 week' --format html -o changelog.html
```

## How It Works

1. `git story` fetches commits in the given time range (hash, author, date, message, files)
2. Sends the structured commit data to a local Ollama model (default: `qwen3-coder`)
3. The LLM generates a narrative changelog grouped by logical sections
4. Outputs as markdown, HTML, or plain text

## Requirements

- Python 3.11+
- [Ollama](https://ollama.ai) running locally
- A code-capable model pulled (e.g., `ollama pull qwen3-coder`)

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--since` | `1 week` | Time range |
| `--until` | now | End time |
| `--format` | `markdown` | `markdown`, `html`, or `plain` |
| `--model` | `qwen3-coder` | Ollama model |
| `-o` / `--output` | stdout | Output file |
| `--ollama-url` | `http://localhost:11434` | Ollama server |
| `-v` / `--verbose` | off | Show raw commit data |
| `--dry-run` | off | Show commits without LLM |

## License

MIT
