"""Fetches full paper text from arxiv HTML versions."""

from __future__ import annotations

import httpx
from bs4 import BeautifulSoup

ARXIV_HTML_URL = "https://arxiv.org/html/{paper_id}"


def fetch_full_text(paper_id: str) -> str | None:
    """
    Fetch the full text of a paper from its arxiv HTML version.
    Returns None if the paper has no HTML version or the fetch fails.
    """
    url = ARXIV_HTML_URL.format(paper_id=paper_id)
    try:
        response = httpx.get(url, timeout=30, follow_redirects=True)
        if response.status_code != 200:
            return None
    except httpx.RequestError:
        return None

    soup = BeautifulSoup(response.text, "lxml")
    article = soup.find("article")
    if not article:
        return None

    # Remove sections that add noise without useful content
    for tag in article.find_all("section", class_="ltx_bibliography"):
        tag.decompose()
    for tag in article.find_all("figure"):
        tag.decompose()
    for tag in article.find_all("section", class_="ltx_appendix"):
        tag.decompose()

    text = article.get_text(separator="\n", strip=True)

    # Collapse excessive blank lines produced by removed elements
    import re
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
