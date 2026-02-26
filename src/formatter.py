"""Saves generated blog posts to disk as Markdown files."""

from __future__ import annotations

from datetime import date
from pathlib import Path


def save_post(content: str, output_dir: str, post_date: date | None = None) -> Path:
    """
    Save blog post content to a Markdown file.
    Returns the path of the saved file.
    """
    post_date = post_date or date.today()
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    filename = f"{post_date.isoformat()}.md"
    filepath = out_path / filename
    filepath.write_text(content, encoding="utf-8")
    return filepath
