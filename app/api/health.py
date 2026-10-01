from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings

router = APIRouter()

@router.get("/", tags=["Welcome"])
async def welcome(settings: Annotated[Settings, Depends(get_settings)]):
    """Welcome endpoint."""
    return {"message": f"Welcome to {settings.app_name}", "status": "ok"}

@router.get("/health", tags=["Health"])
async def health_check(settings: Annotated[Settings, Depends(get_settings)]):
    """Health check endpoint."""
    return {"message": "Health check passed", "status": "ok"}