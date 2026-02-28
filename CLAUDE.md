# HuggingFace Daily Paper Summarizer

## Project Overview

A Python application that fetches the HuggingFace Daily Papers feed, filters to the most popular papers, fetches full paper text from arxiv, and uses an LLM to generate a newsletter post summarizing them — in the style of Nathan Lambert / Sebastian Raschka (insightful ML depth).

Posts are published automatically to [hfdailysummaries.substack.com](https://hfdailysummaries.substack.com).

## Status: All Phases Complete

### Phase 1 — Local MVP ✅
- Fetch HuggingFace Daily Papers via API
- Filter by upvote threshold (configurable, default: 20+)
- Fetch full paper text from arxiv HTML (fallback to abstract)
- Generate blog post via LLM (Gemini free tier)
- Save output as Markdown file in `outputs/` (gitignored)

### Phase 2 — Automation ✅
- Daily cron via Mac launchd (fires at 9:00 AM local time)
- Mac wakes at 8:59 AM via `pmset repeat wake`
- GitHub Actions workflow kept for manual runs only (`workflow_dispatch`)

### Phase 3 — Substack Publishing ✅
- Auto-publishes to Substack via `python-substack` (cookie-based auth)
- Note: Substack's API is blocked by Cloudflare from datacenter IPs (GitHub Actions),
  so publishing runs locally via launchd. Cookie auth bypasses the login endpoint.

## Tech Stack

- **Language:** Python 3.9+ (system Python on Mac)
- **LLM:** Google Gemini free tier (`gemini-2.5-flash`) for prototyping; Claude API (`claude-sonnet-4-6`) for production
- **LLM abstraction:** Pluggable backend — swap provider via config without touching core code
- **Package manager:** `uv` (preferred) or `pip`
- **Config:** `.env` for secrets, `config.yaml` for tunable parameters
- **Scheduling:** Mac launchd at `/Users/nathansusanj/Library/LaunchAgents/com.hfpapers.daily.plist`

## Project Structure

```
hf-paper-summarizer/
├── CLAUDE.md                  # This file
├── .env.example               # Template for required env vars
├── config.yaml                # Tunable config (upvote threshold, paper count, LLM provider, etc.)
├── requirements.txt
├── src/
│   ├── main.py                # Entry point — orchestrates fetch → summarize → save → publish
│   ├── fetcher.py             # Fetches and filters HuggingFace Daily Papers
│   ├── arxiv_fetcher.py       # Fetches full paper text from arxiv HTML
│   ├── summarizer.py          # LLM calls, prompt management
│   ├── substack_publisher.py  # Publishes to Substack via python-substack
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py            # Abstract LLM interface
│   │   ├── gemini.py          # Google Gemini implementation (default/free)
│   │   └── claude.py          # Anthropic Claude implementation (production)
│   └── formatter.py           # Saves Markdown output to outputs/
├── outputs/                   # Generated blog posts — GITIGNORED (published to Substack)
├── prompts/                   # System prompts — GITIGNORED (kept private)
│   └── system.txt             # Main blog post generation prompt
└── .github/
    └── workflows/
        └── daily.yml          # GitHub Actions (manual trigger only — use for ad-hoc runs)
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

# For Substack publishing (cookie-based — see .env.example for setup instructions)
SUBSTACK_COOKIES=
```

## Writing Style Guide

The writing style and tone are defined in `prompts/system.txt` and documented in `STYLE_NOTES.md`. Both files are gitignored and kept private — they contain the editorial voice that differentiates this newsletter.

General direction: technically substantive, direct, occasionally dry. Aimed at ML practitioners who want insight, not just summaries.

## Development Notes

- HuggingFace Daily Papers API: `https://huggingface.co/api/daily_papers`
  - Returns: `paper.title`, `paper.summary` (abstract), `paper.upvotes`, `paper.authors[].name`, `paper.id` (arxiv ID)
- Full paper text fetched from `https://arxiv.org/html/{paper_id}` — strips bibliography, figures, appendices
- Script defaults to yesterday's papers (today's haven't accumulated upvotes yet)
- When switching from Gemini to Claude: change `llm.provider` in `config.yaml` and set `ANTHROPIC_API_KEY`
- Substack session cookies expire after several months — re-extract from browser devtools and update `.env`

## Ops Reference

```bash
# Check launchd job is registered
launchctl list | grep hfpapers

# Trigger manually right now
launchctl start com.hfpapers.daily

# Watch logs
tail -f ~/Library/Logs/hf-paper-summarizer.log

# Check scheduled wake time
pmset -g sched

# Run for a specific date
.venv/bin/python -m src.main 2026-02-25
```
