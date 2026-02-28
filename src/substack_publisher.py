"""Publishes generated posts to Substack via the unofficial API."""

import os
from datetime import date
from substack import Api
from substack.post import Post

PUBLICATION_URL = "https://hfdailysummaries.substack.com"


def publish_to_substack(content: str, post_date: date) -> str:
    """Publish a Markdown post to Substack. Returns the published post URL."""
    cookies = os.environ["SUBSTACK_COOKIES"]

    api = Api(cookies_string=cookies, publication_url=PUBLICATION_URL)
    user_id = api.get_user_id()

    title = f"HF Papers — {post_date.strftime('%B')} {post_date.day}, {post_date.year}"
    post = Post(title=title, subtitle="", user_id=user_id, audience="everyone")
    post.from_markdown(content, api=api)

    draft = api.post_draft(post.get_draft())
    api.prepublish_draft(draft["id"])
    api.publish_draft(draft["id"])

    slug = draft.get("slug", str(draft["id"]))
    return f"{PUBLICATION_URL}/p/{slug}"
