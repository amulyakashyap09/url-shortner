from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.links import router as links_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    """Create FastAPI application."""
    # Depends() only resolves inside request handlers, so the factory calls
    # the cached getter directly; routes use Depends(get_settings) instead.
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )
    app.include_router(health_router)
    app.include_router(links_router, prefix="/links")
    return app


app = create_app()
