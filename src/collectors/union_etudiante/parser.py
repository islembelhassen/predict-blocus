from datetime import datetime, timezone

from bs4 import BeautifulSoup


FRENCH_MONTHS = {
    "janvier": 1,
    "février": 2,
    "fevrier": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "août": 8,
    "aout": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "décembre": 12,
    "decembre": 12,
}


def parse_published_at(value):
    if not value:
        return None

    normalized = " ".join(value.strip().lower().split())

    try:
        return datetime.fromisoformat(
            normalized.replace("z", "+00:00")
        )
    except ValueError:
        pass

    parts = normalized.split(" ")
    if len(parts) != 3 or parts[1] not in FRENCH_MONTHS:
        raise ValueError(
            f"Date de publication non reconnue: {value!r}"
        )

    try:
        return datetime(
            int(parts[2]),
            FRENCH_MONTHS[parts[1]],
            int(parts[0]),
            tzinfo=timezone.utc,
        )
    except ValueError as error:
        raise ValueError(
            f"Date de publication invalide: {value!r}"
        ) from error


def extract_articles(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    articles = []

    items = soup.select(
        ".e-loop-item"
    )

    for item in items:

        link_node = item.find(
            "a",
            href=True
        )

        title_node = item.select_one(
            ".elementor-heading-title"
        )

        date_node = item.find("time")

        if not title_node:
            continue

        articles.append(
            {
                "title": title_node.get_text(
                    strip=True
                ),

                "content": title_node.get_text(
                    strip=True
                ),

                "url":
                    link_node["href"]
                    if link_node
                    else None,

                "published_at": parse_published_at(
                    date_node.get("datetime")
                    or date_node.get_text(
                        strip=True
                    )
                    if date_node
                    else None
                ),
            }
        )

    return articles