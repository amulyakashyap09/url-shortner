from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class LinkCreate(BaseModel):
    """Request body for creating a short link."""

    target_url: HttpUrl


class LinkOut(BaseModel):
    """Short link returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    code: str
    target_url: HttpUrl
    short_url: HttpUrl
    created_at: datetime
