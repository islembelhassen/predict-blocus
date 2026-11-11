from email.utils import parsedate_to_datetime


def parse_entry(entry):

    published_at = None

    if hasattr(entry, "published"):
        try:
            published_at = (
                parsedate_to_datetime(
                    entry.published
                )
            )
        except Exception:
            pass

    return {
        "title": getattr(
            entry,
            "title",
            None,
        ),

        "content": getattr(
            entry,
            "summary",
            "",
        ),

        "url": getattr(
            entry,
            "link",
            None,
        ),

        "published_at": published_at,
    }