from sqlalchemy.orm import Session

from src.database.models import Source


class SourceRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_all_telegram_sources(self):

        return (
            self.db.query(Source)
            .filter(
                Source.type == "telegram"
            )
            .all()
        )

    def get_by_name(
    self,
    name: str,
   ):

        return (
            self.db.query(Source)
            .filter(
                Source.name == name
            )
            .first()
        )

    def get_all_by_type(
    self,
    source_type: str,
    ):
        return (
            self.db.query(Source)
            .filter(
                Source.type
                == source_type
            )
            .all()
        )
  