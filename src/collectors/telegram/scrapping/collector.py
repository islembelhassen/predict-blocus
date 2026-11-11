from sqlalchemy.orm import Session

from src.database.connection import (
    SessionLocal,
)

from src.collectors.telegram.scrapping.scraper import (
    fetch_channel,
)

from src.collectors.telegram.scrapping.parser import (
    extract_messages,
)

from src.database.repositories.source_repository import (
    SourceRepository,
)

from src.database.repositories.raw_event_repository import (
    RawEventRepository,
)

from src.storage.json_storage import (
    save_raw_events,
)

from src.utils.ids import (
    create_external_id,
)


def run():

    db: Session = SessionLocal()

    source_repo = SourceRepository(db)

    event_repo = RawEventRepository(db)

    telegram_sources = (
        source_repo.get_all_telegram_sources()
    )

    for source in telegram_sources:

        html = fetch_channel(
            source.url
        )

        messages = extract_messages(
            html
        )

        json_events = []

        for msg in messages:

            external_id = (
                create_external_id(
                    source.name,
                    msg["content"],
                    str(
                        msg["published_at"]
                    ),
                )
            )

            event = {
                "source_id": source.id,
                "external_id": external_id,
                "title": None,
                "content": msg["content"],
                "author": None,
                "url": msg["url"],
                "published_at":
                    msg["published_at"],
                "language": "fr",
                "metadata": {},
            }

            inserted = (
                event_repo.save(
                    event
                )
            )

            if inserted:
                json_events.append(
                    event
                )

        save_raw_events(
            json_events,
            source.name
        )

        print(
            f"{source.name}: "
            f"{len(json_events)} nouveaux événements"
        )

    db.close()


if __name__ == "__main__":
    run()