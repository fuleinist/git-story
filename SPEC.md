# git-story — SPEC v1

## Mission
A CLI tool that generates human-readable narrative changelogs from git history using local LLMs via Ollama — no API keys needed.

## Why
Commit messages are terse and technical. PR reviews and changelogs require manual effort. Developers want to understand "what happened this week" without reading raw `git log`.

## Usage
```bash
# Basic — last week's story
git story --since '1 week'

# Custom time range
git story --since '2026-06-01' --until '2026-06-30'

# Output formats
git story --since '1 week' --format markdown  # default
git story --since '1 week' --format html
git story --since '1 week' --format plain

# With custom model
git story --since '1 week' --model qwen3-coder

# Write to file
git story --since '1 week' -o CHANGELOG.md

# Pipe to stdout
git story --since '1 week' --format plain | head -20
```

## Acceptance Criteria

### CLI (MVP)
- [x] `git story` command (installed as `git-story` binary, also callable as `git story`)
- [x] `--since` flag: time range (e.g. `1 week`, `2026-06-01`, `2 days ago`)
- [x] `--until` flag: end time (default: now)
- [x] `--format` flag: `markdown` (default), `html`, `plain`
- [x] `--model` flag: Ollama model name (default: `qwen3-coder`)
- [x] `-o` / `--output`: write to file instead of stdout
- [x] `--ollama-url`: custom Ollama server URL (default: `http://localhost:11434`)
- [x] Fetches git log with author, date, message, and files changed
- [x] Sends commit data to local Ollama for narrative generation
- [x] Groups related changes into logical sections
- [x] Identifies breaking changes and highlights them
- [x] Detects patterns (refactoring, bug fixes, features, deps)

### Output Quality
- [x] Narrative reads like a human wrote it, not a bullet list
- [x] Breaking changes called out with ⚠️ or similar marker
- [x] Empty/no commits in range returns a friendly message
- [x] Respects `.git` directory boundaries (works in subdirs)

### Developer Experience
- [x] Clear error if Ollama not running
- [x] Clear error if no commits in range
- [x] Progress indicator during LLM processing
- [x] Verbose mode (`-v`) shows raw commit data sent to model
- [x] Dry-run mode (`--dry-run`) shows commit data without calling Ollama

## Tech Stack
- **Language:** Python 3.11+ (fastest path for Ollama API + git parsing)
- **CLI:** `click` or `argparse`
- **Ollama:** `requests` to `http://localhost:11434/api/generate`
- **Git:** `gitpython` or subprocess `git log`
- **Output:** Jinja2 templates for markdown/html/plain

## Architecture
```
git-story/
├── gitstory/
│   ├── __init__.py
│   ├── cli.py           # CLI entry point
│   ├── git.py           # Git log parsing
│   ├── llm.py           # Ollama API client
│   ├── narrative.py     # Prompt construction + response parsing
│   └── render.py        # Output rendering (markdown/html/plain)
├── templates/           # Jinja2 templates
├── SPEC.md
├── README.md
├── pyproject.toml
└── Makefile
```

## Out of Scope (v1)
- Interactive mode / TUI
- GitHub/GitLab integration
- Multi-repo summaries
- Caching LLM responses
- Custom prompt templates
