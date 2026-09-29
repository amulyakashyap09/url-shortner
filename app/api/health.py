from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Welcome"])
async def welcome():
    """Welcome endpoint."""
    return {"message": "Welcome", "status": "ok"}

@router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"message": "Health check passed", "status": "ok"}