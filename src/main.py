"""Entry point — fetch papers, generate blog post, save to disk."""

from __future__ import annotations

import os
import sys
import yaml
from datetime import date, timedelta
from pathlib import Path
from dotenv import load_dotenv

from .fetcher import fetch_papers, filter_papers, enrich_with_full_text
from .summarizer import generate_blog_post
from .formatter import save_post
from .llm import get_provider

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def run(target_date: date | None = None) -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    config = load_config()

    # Default to yesterday — today's papers haven't had time to accumulate upvotes
    if target_date is None:
        target_date = date.today() - timedelta(days=1)

    # --- Fetch and filter papers ---
    print(f"Fetching HuggingFace Daily Papers for {target_date}...")
    papers = fetch_papers(target_date)
    print(f"  Found {len(papers)} total papers.")

    threshold = config["papers"]["upvote_threshold"]
    max_papers = config["papers"]["max_papers"]
    papers = filter_papers(papers, upvote_threshold=threshold, max_papers=max_papers)
    print(f"  {len(papers)} papers meet the {threshold}+ upvote threshold.")

    if not papers:
        print("No papers met the threshold. Exiting.")
        return

    # --- Fetch full text from arxiv ---
    print("Fetching full paper texts from arxiv...")
    enrich_with_full_text(papers)
    fetched = sum(1 for p in papers if p.full_text)
    print(f"  Full text retrieved for {fetched}/{len(papers)} papers.")

    # --- Set up LLM ---
    llm_config = config["llm"]
    provider = get_provider(llm_config["provider"], model=llm_config.get("model"))
    print(f"Using LLM provider: {llm_config['provider']}")

    # --- Generate blog post ---
    print("Generating blog post...")
    post_content = generate_blog_post(papers, llm=provider)

    # --- Save output ---
    output_dir = config["output"]["dir"]
    saved_path = save_post(post_content, output_dir=output_dir, post_date=target_date)
    print(f"Blog post saved to: {saved_path}")

    # --- Publish to Substack (only when credentials are present) ---
    if os.environ.get("SUBSTACK_EMAIL") and os.environ.get("SUBSTACK_PASSWORD"):
        from .substack_publisher import publish_to_substack
        print("Publishing to Substack...")
        url = publish_to_substack(post_content, target_date)
        print(f"Published: {url}")


if __name__ == "__main__":
    # Optional: pass a date as a CLI arg, e.g. python -m src.main 2026-02-25
    target = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else None
    run(target_date=target)
