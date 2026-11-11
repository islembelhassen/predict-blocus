from sqlalchemy.orm import Session

from src.database.models import RawEvent


class RawEventRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def exists(
        self,
        external_id: str,
    ):

        return (
            self.db.query(RawEvent)
            .filter(
                RawEvent.external_id
                == external_id
            )
            .first()
            is not None
        )

    def save(
        self,
        event: dict,
    ):

        if self.exists(
            event["external_id"]
        ):
            return False

        raw_event = RawEvent(**event)

        self.db.add(raw_event)

        self.db.commit()

        return True