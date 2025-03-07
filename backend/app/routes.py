from fastapi import APIRouter
from app.controllers.item_controller import router as items_router
from app.controllers.auth_controller import router as auth_router

router = APIRouter()

router.include_router(items_router, prefix="/items", tags=["items"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
