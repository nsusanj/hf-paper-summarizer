"""Generates blog post content from papers using an LLM."""

from pathlib import Path
from .fetcher import Paper
from .llm.base import LLMProvider

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    return path.read_text(encoding="utf-8")


def build_papers_context(papers: list[Paper]) -> str:
    """Format papers into a structured string for the LLM prompt."""
    sections = []
    for i, p in enumerate(papers, 1):
        authors_str = ", ".join(p.authors[:3])
        if len(p.authors) > 3:
            authors_str += " et al."

        if p.full_text:
            content_block = f"**Full Paper Text:**\n{p.full_text}"
        else:
            content_block = f"**Abstract (full text unavailable):**\n{p.abstract}"

        sections.append(
            f"## Paper {i}: {p.title}\n"
            f"**Authors:** {authors_str}\n"
            f"**Upvotes:** {p.upvotes}\n"
            f"**URL:** {p.url}\n\n"
            f"{content_block}"
        )
    return "\n\n---\n\n".join(sections)


def generate_blog_post(papers: list[Paper], llm: LLMProvider) -> str:
    """Generate a full blog post for the given papers."""
    system_prompt = load_prompt("system.txt")
    papers_context = build_papers_context(papers)
    user_prompt = (
        f"Here are today's top HuggingFace papers. Write a blog post covering each one:\n\n"
        f"{papers_context}"
    )
    return llm.complete(system_prompt=system_prompt, user_prompt=user_prompt)
