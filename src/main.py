"""Entry point — fetch papers, generate blog post, save to disk."""

import sys
import yaml
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

from .fetcher import fetch_papers, filter_papers
from .summarizer import generate_blog_post
from .formatter import save_post
from .llm import get_provider

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def run(target_date: date | None = None) -> None:
    load_dotenv()
    config = load_config()

    # --- Fetch and filter papers ---
    print(f"Fetching HuggingFace Daily Papers for {target_date or 'today'}...")
    papers = fetch_papers(target_date)
    print(f"  Found {len(papers)} total papers.")

    threshold = config["papers"]["upvote_threshold"]
    max_papers = config["papers"]["max_papers"]
    papers = filter_papers(papers, upvote_threshold=threshold, max_papers=max_papers)
    print(f"  {len(papers)} papers meet the {threshold}+ upvote threshold.")

    if not papers:
        print("No papers met the threshold today. Exiting.")
        return

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


if __name__ == "__main__":
    # Optional: pass a date as a CLI arg, e.g. python -m src.main 2024-01-15
    target = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else None
    run(target_date=target)
