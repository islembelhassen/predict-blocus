import feedparser



import feedparser

from sqlalchemy.orm import Session

from src.database.connection import (
    SessionLocal,
)


from src.collectors.google_news.parser import (
    parse_entry,
)

from src.utils.ids import (
    create_external_id,
)

from src.storage.json_storage import (
    save_raw_events,
)

from src.database.repositories.source_repository import (
    SourceRepository,
)

from src.database.repositories.raw_event_repository import (
    RawEventRepository,
)


RSS_URLS = [
    "https://news.google.com/rss/search?q=blocus+universite&hl=fr&gl=FR&ceid=FR:fr",

    "https://news.google.com/rss/search?q=greve+etudiante&hl=fr&gl=FR&ceid=FR:fr",

    "https://news.google.com/rss/search?q=occupation+campus&hl=fr&gl=FR&ceid=FR:fr",

    "https://news.google.com/rss/search?q=manifestation+etudiante&hl=fr&gl=FR&ceid=FR:fr",
]


def run():

    db: Session = SessionLocal()

    source_repo = SourceRepository(db)

    event_repo = RawEventRepository(db)

    source = (
        source_repo
        .get_by_name(
            "google_news"
        )
    )

    if not source:
        raise Exception(
            "google_news source not found"
        )

    inserted_events = []

    for rss_url in RSS_URLS:

        feed = feedparser.parse(
            rss_url
        )

        for entry in feed.entries:

            parsed = parse_entry(
                entry
            )

            external_id = (
                create_external_id(
                    source.name,
                    parsed["url"],
                    str(
                        parsed[
                            "published_at"
                        ]
                    ),
                )
            )

            event = {
                "source_id":
                    source.id,

                "external_id":
                    external_id,

                "title":
                    parsed["title"],

                "content":
                    parsed["content"],

                "author":
                    "Google News",

                "url":
                    parsed["url"],

                "published_at":
                    parsed["published_at"],

                "language":
                    "fr",

                "metadata": {
                    "rss_url":
                        rss_url
                },
            }

            inserted = (
                event_repo.save(
                    event
                )
            )

            if inserted:
                inserted_events.append(
                    event
                )

    save_raw_events(
        inserted_events,
        "google_news"
    )

    print(
        f"Google News: "
        f"{len(inserted_events)} "
        f"new events"
    )

    db.close()


if __name__ == "__main__":
    run()