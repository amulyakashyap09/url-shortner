from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from app.core.config import Settings, get_settings
from app.schemas.link import LinkCreate
from app.services.link_store import get_link_store, LinkStore

router = APIRouter()
link_store: LinkStore = get_link_store()

@router.get("/{code}", tags=["links"], response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def get_link(code: str, settings: Settings = Depends(get_settings)):
    """Get a short link by its code."""
    # This is a placeholder implementation. In a real application, you would
    # retrieve the link from the database or another storage mechanism.
    record = link_store.get(code=code)
    if not record:
        raise HTTPException(status_code=404, detail="Link not found")
    return {
        "code": record.code,
        "target_url": record.target_url,
        "short_url": f"{settings.base_url}/{record.code}",
        "created_at": record.created_at.isoformat(),
    }

@router.post("/", tags=["links"])
async def create_link(link_create: LinkCreate, settings: Settings = Depends(get_settings), status_code=status.HTTP_201_CREATED):
    """Create a new short link."""
    # This is a placeholder implementation. In a real application, you would
    # generate a unique code and store the link in the database or another
    # storage mechanism.
    record = link_store.create(url=link_create.target_url)
    return {
        "code": record.code,
        "target_url": record.target_url,
        "short_url": f"{settings.base_url}/{record.code}",
        "created_at": record.created_at.isoformat(),
    }