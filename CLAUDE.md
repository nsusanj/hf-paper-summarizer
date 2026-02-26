# HuggingFace Daily Paper Summarizer

## Project Overview

A Python application that fetches the HuggingFace Daily Papers feed, filters to the most popular papers, and uses an LLM to generate an entertaining blog post summarizing them — in the style of Nathan Lambert / Sebastian Ratschka (insightful ML depth) with a dash of Bill Simmons (lively, witty, accessible).

The end goal is a daily Substack newsletter, but Phase 1 focuses on local iteration to get the format right.

## Phases

### Phase 1 — Local MVP (current focus)
- Fetch HuggingFace Daily Papers via API
- Filter by upvote threshold (configurable, default: 20+)
- Generate blog post via LLM (Gemini free tier for prototyping)
- Save output as Markdown file in `outputs/`

### Phase 2 — Automation
- GitHub Actions daily cron job (free)
- Outputs committed to repo or saved as artifacts

### Phase 3 — Substack Integration
- Publish generated post as a Substack draft
- AI editor review step before publishing
- Eventually: fully automated publish + send to subscribers

## Tech Stack

- **Language:** Python 3.11+
- **LLM:** Google Gemini free tier (`gemini-1.5-flash`) for prototyping; Claude API (`claude-sonnet-4-6`) for production
- **LLM abstraction:** Pluggable backend — swap provider via config without touching core code
- **Package manager:** `uv` (preferred) or `pip`
- **Config:** `.env` for secrets, `config.yaml` for tunable parameters
- **Scheduling:** GitHub Actions (Phase 2+)

## Project Structure

```
hf-paper-summarizer/
├── CLAUDE.md                  # This file
├── .env.example               # Template for required env vars
├── config.yaml                # Tunable config (upvote threshold, paper count, LLM provider, etc.)
├── requirements.txt
├── src/
│   ├── main.py                # Entry point — orchestrates fetch → summarize → save
│   ├── fetcher.py             # Fetches and filters HuggingFace Daily Papers
│   ├── summarizer.py          # LLM calls, prompt management
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py            # Abstract LLM interface
│   │   ├── gemini.py          # Google Gemini implementation (default/free)
│   │   └── claude.py          # Anthropic Claude implementation (production)
│   └── formatter.py           # Assembles final Markdown blog post
├── outputs/                   # Generated blog posts (gitignored or committed)
├── prompts/                   # System prompts — GITIGNORED (kept private)
│   └── system.txt             # Main blog post generation prompt
└── .github/
    └── workflows/
        └── daily.yml          # GitHub Actions cron (Phase 2)
```

## Key Configuration (config.yaml)

- `upvote_threshold`: Minimum upvotes to include a paper (default: 20)
- `max_papers`: Maximum papers per post even if threshold is exceeded (default: 10)
- `output_dir`: Where to write generated posts (default: `outputs/`)
- `llm.provider`: Which LLM backend to use — `gemini` or `claude` (default: `gemini`)
- `llm.model`: Model name override (defaults to best model for the chosen provider)

## Environment Variables

```
# For Gemini (prototyping — free tier)
GOOGLE_API_KEY=         # From Google AI Studio: aistudio.google.com

# For Claude (production — when ready to switch)
ANTHROPIC_API_KEY=      # From console.anthropic.com (separate from claude.ai Pro subscription)
```

## Writing Style Guide

The writing style and tone are defined in `prompts/system.txt` and documented in `STYLE_NOTES.md`. Both files are gitignored and kept private — they contain the editorial voice that differentiates this newsletter.

General direction: technically substantive, witty, accessible, and opinionated-but-fair. Aimed at curious technical readers who want insight, not just summaries.

## Development Notes

- HuggingFace Daily Papers API: `https://huggingface.co/api/daily_papers`
  - Returns: `paper.title`, `paper.summary` (abstract), `paper.upvotes`, `paper.authors[].name`, `paper.id` (arxiv ID)
- Outputs should be valid Markdown, easily pasteable into Substack
- Keep prompts in `prompts/` so tone/style can be iterated without touching code
- When switching from Gemini to Claude: change `llm.provider` in `config.yaml` and set `ANTHROPIC_API_KEY`

## Future TODOs (Phase 3)
- Substack draft creation via API/email
- AI editor review pass before publishing
- Fully automated publish + subscriber send
