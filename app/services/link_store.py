import secrets
import string
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated, Protocol

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.link import Link

CODE_ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 7
MAX_CODE_ATTEMPTS = 5


class CodeGenerationError(Exception):
    """Could not find an unused short code."""


@dataclass(frozen=True)
class LinkRecord:
    """A stored short link."""

    code: str
    target_url: str
    created_at: datetime

class LinkStore(Protocol):
    """Storage interface for short links."""

    def create(self, url: str) -> LinkRecord: ...

    def get(self, code: str) -> LinkRecord | None: ...

def get_link_store(db: Annotated[Session, Depends(get_db)]) -> LinkStore:
    """Return a link store bound to this request's DB session."""
    return SqlLinkStore(db)

class SqlLinkStore:
    """LinkStore backed by a SQL database."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, url: str) -> LinkRecord:
        """Create a new short link."""
        for _ in range(MAX_CODE_ATTEMPTS):
            link = Link(code=_new_code(), target_url=url)
            self._db.add(link)
            try:
                self._db.commit()
            except IntegrityError:
                # Code collision; try again.
                self._db.rollback()
                continue
            return _to_record(link)
        raise CodeGenerationError(f"No unused code after {MAX_CODE_ATTEMPTS} attempts")

    def get(self, code: str) -> LinkRecord | None:
        """Get a short link by its code."""
        link = self._db.execute(select(Link).where(Link.code == code)).scalar_one_or_none()
        return _to_record(link) if link else None

def _new_code() -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))

def _to_record(link: Link) -> LinkRecord:
    created_at = link.created_at
    if created_at.tzinfo is None:  # SQLite drops tzinfo; we stored UTC
        created_at = created_at.replace(tzinfo=UTC)
    return LinkRecord(code=link.code, target_url=link.target_url, created_at=created_at)