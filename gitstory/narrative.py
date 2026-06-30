"""Prompt construction and narrative generation."""

from gitstory.git import get_commits
from gitstory.llm import generate


def _build_prompt(commits: list[dict]) -> str:
    """Build a prompt for the LLM from commit data."""
    lines = []
    for c in commits:
        files_str = ", ".join(c.get("files", [])) if c.get("files") else "(no files)"
        lines.append(f"- [{c['hash'][:8]}] {c['message']} ({c['author']}, {c['date'][:10]})")
        lines.append(f"  Files: {files_str}")

    commits_text = "\n".join(lines)

    return f"""You are a technical writer generating a human-readable changelog from git commit data.

Given the following commits, write a concise narrative changelog that:
1. Groups related changes into logical sections (Features, Bug Fixes, Refactoring, Dependencies, etc.)
2. Highlights breaking changes with ⚠️
3. Reads like a human wrote it — not a bullet list of commit messages
4. Mentions key contributors
5. Keeps it under 500 words

Commits:
{commits_text}

Narrative changelog:"""


def generate_narrative(commits: list[dict], model: str = "qwen3-coder",
                       ollama_url: str = "http://localhost:11434") -> str:
    """Generate a narrative changelog from commit data."""
    prompt = _build_prompt(commits)
    return generate(prompt, model=model, url=ollama_url)
