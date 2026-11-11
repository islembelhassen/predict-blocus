import json

from pathlib import Path
from datetime import datetime


def save_raw_events(
    events: list,
    source: str,
):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    directory = Path(
        f"data/raw/{source}"
    )

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = directory / f"{today}.json"

    if file_path.exists():

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as f:

            existing = json.load(f)

    else:
        existing = []

    existing.extend(events)

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            existing,
            f,
            ensure_ascii=False,
            indent=2,
            default=str,
        )