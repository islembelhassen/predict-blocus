


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    type = Column(String(50))
    url = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    city = Column(String(255))

    aliases = Column(
        ARRAY(String),
        default=[],
    )


class RawEvent(Base):
    __tablename__ = "raw_events"

    id = Column(Integer, primary_key=True)

    source_id = Column(
        Integer,
        ForeignKey("sources.id"),
        nullable=False,
    )

    external_id = Column(String(255))

    title = Column(Text)

    content = Column(
        Text,
        nullable=False,
    )

    author = Column(String(255))

    url = Column(Text)

    published_at = Column(DateTime(timezone=True))

    collected_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    language = Column(String(10))

    metadata_json = Column(
        JSONB,
        default=dict,
    )


class DailyRiskFeature(Base):
    __tablename__ = "daily_risk_features"

    id = Column(Integer, primary_key=True)

    date = Column(
        Date,
        nullable=False,
    )

    university_id = Column(
        Integer,
        ForeignKey("universities.id"),
        nullable=False,
    )

    telegram_mentions = Column(Integer, default=0)

    news_mentions = Column(Integer, default=0)

    union_mentions = Column(Integer, default=0)

    unef_mentions = Column(Integer, default=0)

    media_mentions = Column(Integer, default=0)

    sentiment_score = Column(Float)

    risk_score = Column(Float)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "date",
            "university_id",
            name="uq_daily_risk_features",
        ),
    )