import secrets
import string
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from typing import Protocol

CODE_ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 7


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


class InMemoryLinkStore:
    """LinkStore backed by a plain dict. Data is lost on restart."""

    def __init__(self) -> None:
        self._links: dict[str, LinkRecord] = {}
        # Sync endpoints run in a threadpool; guard the check-then-insert.
        self._lock = threading.Lock()

    def create(self, url: str) -> LinkRecord:
        with self._lock:
            code = self._new_code()
            record = LinkRecord(
                code=code,
                target_url=url,
                created_at=datetime.now(timezone.utc),
            )
            self._links[code] = record
            return record

    def get(self, code: str) -> LinkRecord | None:
        return self._links.get(code)

    def _new_code(self) -> str:
        while True:
            code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
            if code not in self._links:
                return code


@lru_cache
def get_link_store() -> LinkStore:
    """Return the process-wide link store."""
    return InMemoryLinkStore()
