import requests

from sqlalchemy.orm import Session

from src.database.connection import (
    SessionLocal,
)

from src.utils.ids import (
    create_external_id,
)

from src.storage.json_storage import (
    save_raw_events,
)

from src.collectors.union_etudiante.parser import (
    extract_articles,
)

from src.database.repositories.source_repository import (
    SourceRepository,
)

from src.database.repositories.raw_event_repository import (
    RawEventRepository,
)

URL = "https://union-etudiante.fr/dossier-de-presse/"


def run():

    db: Session = SessionLocal()

    source_repo = SourceRepository(db)

    event_repo = RawEventRepository(db)

    source = source_repo.get_by_name(
        "union_etudiante"
    )

    response = requests.get(
        URL,
        timeout=30
    )

    articles = extract_articles(
        response.text
    )

    inserted_events = []

    for article in articles:

        external_id = (
            create_external_id(
                "union_etudiante",
                article["url"] or "",
                "",
            )
        )

        event = {
            "source_id": source.id,
            "external_id": external_id,
            "title": article["title"],
            "content": article["content"],
            "author": "Union Étudiante",
            "url": article["url"],
            "published_at": article["published_at"],
            "language": "fr",
            "metadata": {}
        }


        inserted = event_repo.save(
            event
        )

        if inserted:
            inserted_events.append(
                event
            )

    save_raw_events(
        inserted_events,
        "union_etudiante"
    )

    print(
        "Union Étudiante : "
        f"{len(inserted_events)} nouveaux événements"
    )

    db.close()


if __name__ == "__main__":
    run()