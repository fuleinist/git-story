"""Git log parsing utilities."""

import subprocess
import re
from datetime import datetime
from typing import Optional


def get_commits(since: str = "1 week", until: Optional[str] = None) -> list[dict]:
    """Fetch commits from git log within the given time range.

    Returns a list of dicts with: hash, author, date, message, files.
    """
    args = [
        "git", "log",
        f"--since={since}",
        "--format=%H|||%an|||%ai|||%s",
        "--name-only",
    ]
    if until:
        args.append(f"--until={until}")

    result = subprocess.run(args, capture_output=True, text=True, cwd=".")
    if result.returncode != 0:
        raise RuntimeError(f"git log failed: {result.stderr.strip()}")

    return _parse_log(result.stdout)


def _parse_log(raw: str) -> list[dict]:
    """Parse git log --format output into structured commit data."""
    commits = []
    current = None
    files = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        # Commit header: hash|||author|||date|||subject
        if "|||" in line:
            if current is not None:
                current["files"] = files
                commits.append(current)
                files = []

            parts = line.split("|||", 3)
            current = {
                "hash": parts[0],
                "author": parts[1],
                "date": parts[2],
                "message": parts[3] if len(parts) > 3 else "",
            }
        elif current is not None:
            # File path
            files.append(line)

    if current is not None:
        current["files"] = files
        commits.append(current)

    return commits
