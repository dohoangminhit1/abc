from fastapi import APIRouter
from app.auth.routes.register import router as register_router
from app.auth.routes.login import router as login_router

router = APIRouter()

router.include_router(register_router, tags=["auth"], prefix="/auth")
router.include_router(login_router, tags=["auth"], prefix="/auth")