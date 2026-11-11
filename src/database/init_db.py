from connection import engine
from models import Base, Source

Base.metadata.create_all(bind=engine)

print("Tables created successfully")

# Sources par défaut

from sqlalchemy.orm import Session

default_sources = [
    {
        "name": "telegram_infoblocage",
        "type": "telegram",
        "url": "https://t.me/s/infoblocagefrance1",
    },
    {
        "name": "telegram_giletsjaunes",
        "type": "telegram",
        "url": "https://t.me/s/GiletsJaunesGenZ",
    },
    {
        "name": "google_news",
        "type": "news",
        "url": "https://news.google.com",
    },
    {
        "name": "unef",
        "type": "syndicat",
        "url": "https://www.unef.fr",
    },
    {
        "name": "union_etudiante",
        "type": "syndicat",
        "url": "https://unionetudiante.fr",
    },
    {
        "name": "france24",
        "type": "media",
        "url": "https://www.france24.com/fr",
    },
]

with Session(engine) as session:

    for source in default_sources:

        existing = (
            session.query(Source)
            .filter(Source.name == source["name"])
            .first()
        )

        if not existing:
            session.add(Source(**source))

    session.commit()

print("Default sources inserted")
