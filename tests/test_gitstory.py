"""Tests for git-story."""

import pytest
from gitstory.git import _parse_log
from gitstory.render import _strip_markdown, _wrap_html


class TestParseLog:
    def test_single_commit(self):
        raw = """abc1234|||Alice|||2026-06-30 10:00:00 +1000|||feat: add login
README.md
main.py"""
        commits = _parse_log(raw)
        assert len(commits) == 1
        assert commits[0]["hash"] == "abc1234"
        assert commits[0]["author"] == "Alice"
        assert commits[0]["message"] == "feat: add login"
        assert commits[0]["files"] == ["README.md", "main.py"]

    def test_multiple_commits(self):
        raw = """aaa|||Alice|||2026-06-30|||first
a.txt
bbb|||Bob|||2026-06-29|||second
b.txt"""
        commits = _parse_log(raw)
        assert len(commits) == 2
        assert commits[0]["hash"] == "aaa"
        assert commits[1]["hash"] == "bbb"

    def test_no_files(self):
        raw = """abc|||Alice|||2026-06-30|||no files"""
        commits = _parse_log(raw)
        assert len(commits) == 1
        assert commits[0]["files"] == []

    def test_empty_input(self):
        assert _parse_log("") == []


class TestRender:
    def test_strip_markdown(self):
        md = "# Title\n## Section\n- item\n**bold**"
        result = _strip_markdown(md)
        assert "Title" in result
        assert "Section" in result
        assert "•" in result
        assert "**" not in result

    def test_wrap_html(self):
        md = "# Hello\n## Sub\n- item\n⚠️ breaking"
        result = _wrap_html(md)
        assert "<h1>Hello</h1>" in result
        assert "<h2>Sub</h2>" in result
        assert "<li>item</li>" in result
        assert 'class="breaking"' in result
