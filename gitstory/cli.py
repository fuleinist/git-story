"""CLI entry point for git-story."""

import sys
import click


@click.command()
@click.option("--since", default="1 week", help="Time range (e.g. '1 week', '2026-06-01', '2 days ago')")
@click.option("--until", default=None, help="End time (default: now)")
@click.option("--format", "format_name", default="markdown", type=click.Choice(["markdown", "html", "plain"]),
              help="Output format")
@click.option("--model", default="qwen3-coder", help="Ollama model name")
@click.option("-o", "--output", default=None, help="Write to file instead of stdout")
@click.option("--ollama-url", default="http://localhost:11434", help="Ollama server URL")
@click.option("-v", "--verbose", is_flag=True, help="Show raw commit data sent to model")
@click.option("--dry-run", is_flag=True, help="Show commit data without calling Ollama")
def main(since, until, format_name, model, output, ollama_url, verbose, dry_run):
    """Generate a human-readable narrative changelog from git history."""
    from gitstory.git import get_commits
    from gitstory.llm import check_ollama
    from gitstory.narrative import generate_narrative
    from gitstory.render import render_output

    # 1. Fetch commits
    if verbose:
        click.echo(f"Fetching commits since: {since}", err=True)
        if until:
            click.echo(f"Fetching commits until: {until}", err=True)

    commits = get_commits(since=since, until=until)

    if not commits:
        click.echo("No commits found in the specified range.", err=True)
        sys.exit(0)

    if verbose:
        click.echo(f"Found {len(commits)} commits", err=True)

    # 2. Dry-run: just show commit data
    if dry_run:
        from gitstory.render import render_commits_raw
        click.echo(render_commits_raw(commits))
        return

    # 3. Check Ollama
    if not check_ollama(ollama_url):
        click.echo(
            "Error: Ollama is not running. Start it with 'ollama serve' or set --ollama-url.",
            err=True,
        )
        sys.exit(1)

    # 4. Generate narrative
    if verbose:
        click.echo(f"Generating narrative using model: {model}", err=True)

    click.echo("📖 Writing story...", err=True)
    narrative = generate_narrative(commits, model=model, ollama_url=ollama_url)

    # 5. Render output
    output_text = render_output(narrative, format_name=format_name)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(output_text)
        click.echo(f"Written to {output}", err=True)
    else:
        click.echo(output_text)


if __name__ == "__main__":
    main()
