"""Fetches and filters HuggingFace Daily Papers."""

import httpx
from dataclasses import dataclass
from datetime import date


HF_API_URL = "https://huggingface.co/api/daily_papers"


@dataclass
class Paper:
    title: str
    abstract: str
    upvotes: int
    authors: list[str]
    paper_id: str  # arxiv ID, used to build URL

    @property
    def url(self) -> str:
        return f"https://huggingface.co/papers/{self.paper_id}"


def fetch_papers(target_date: date | None = None) -> list[Paper]:
    """
    Fetch daily papers from HuggingFace.
    If target_date is None, fetches today's papers.
    """
    params = {}
    if target_date:
        params["date"] = target_date.isoformat()

    response = httpx.get(HF_API_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    papers = []
    for item in data:
        paper_info = item.get("paper", {})
        paper_id = paper_info.get("id", "")
        authors = [a.get("name", "") for a in paper_info.get("authors", [])]
        papers.append(Paper(
            title=paper_info.get("title", ""),
            abstract=paper_info.get("abstract", ""),
            upvotes=item.get("numComments", 0),  # HF API uses numComments for upvotes
            authors=authors,
            paper_id=paper_id,
        ))

    return papers


def filter_papers(papers: list[Paper], upvote_threshold: int, max_papers: int) -> list[Paper]:
    """Filter papers by upvote threshold and cap at max_papers, sorted by upvotes descending."""
    filtered = [p for p in papers if p.upvotes >= upvote_threshold]
    filtered.sort(key=lambda p: p.upvotes, reverse=True)
    return filtered[:max_papers]
