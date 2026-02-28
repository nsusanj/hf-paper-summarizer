"""Publishes generated posts to Substack via the unofficial API."""

import os
from datetime import date
from substack import Api
from substack.post import Post

PUBLICATION_URL = "https://hfdailysummaries.substack.com"


def publish_to_substack(content: str, post_date: date) -> str:
    """Publish a Markdown post to Substack. Returns the published post URL."""
    email = os.environ.get("SUBSTACK_EMAIL")
    password = os.environ.get("SUBSTACK_PASSWORD")
    cookies = os.environ.get("SUBSTACK_COOKIES")

    if cookies:
        api = Api(cookies_string=cookies, publication_url=PUBLICATION_URL)
    elif email and password:
        api = Api(email=email, password=password, publication_url=PUBLICATION_URL)
    else:
        raise EnvironmentError("Set SUBSTACK_COOKIES in .env (see .env.example for instructions).")
    user_id = api.get_user_id()

    title = f"HF Papers — {post_date.strftime('%B')} {post_date.day}, {post_date.year}"
    post = Post(title=title, subtitle="", user_id=user_id, audience="everyone")
    post.from_markdown(content, api=api)

    draft = api.post_draft(post.get_draft())
    api.prepublish_draft(draft["id"])
    api.publish_draft(draft["id"])

    slug = draft.get("slug") or draft.get("id") or ""
    return f"{PUBLICATION_URL}/p/{slug}"
