"""Output rendering for git-story."""

from jinja2 import Environment, PackageLoader, select_autoescape


def render_output(narrative: str, format_name: str = "markdown") -> str:
    """Render the narrative in the requested format."""
    if format_name == "markdown":
        return narrative  # LLM already outputs markdown
    elif format_name == "html":
        return _wrap_html(narrative)
    else:
        return _strip_markdown(narrative)


def render_commits_raw(commits: list[dict]) -> str:
    """Render raw commit data for dry-run mode."""
    lines = []
    for c in commits:
        lines.append(f"commit {c['hash']}")
        lines.append(f"Author: {c['author']}")
        lines.append(f"Date:   {c['date']}")
        lines.append(f"")
        lines.append(f"    {c['message']}")
        lines.append(f"")
        for f in c.get("files", []):
            lines.append(f"    {f}")
        lines.append(f"")
    return "\n".join(lines)


def _wrap_html(markdown_text: str) -> str:
    """Wrap narrative in minimal HTML."""
    import html
    escaped = html.escape(markdown_text)
    # Simple markdown-like conversion
    lines = []
    for line in escaped.split("\n"):
        if line.startswith("### "):
            lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("- "):
            lines.append(f"<li>{line[2:]}</li>")
        elif line.startswith("⚠️ "):
            lines.append(f'<p class="breaking">{line}</p>')
        elif line.strip() == "":
            lines.append("<br>")
        else:
            lines.append(f"<p>{line}</p>")

    body = "\n".join(lines)
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Changelog</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 720px; margin: 2em auto; line-height: 1.6; color: #333; }}
h1 {{ border-bottom: 2px solid #eee; padding-bottom: 0.3em; }}
.breaking {{ background: #fff3cd; padding: 0.5em; border-radius: 4px; }}
li {{ margin: 0.3em 0; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def _strip_markdown(markdown_text: str) -> str:
    """Strip markdown formatting for plain text output."""
    import re
    text = re.sub(r"^###\s+", "", markdown_text, flags=re.MULTILINE)
    text = re.sub(r"^##\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^#\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\*\*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^- ", "  • ", text, flags=re.MULTILINE)
    return text.strip()
