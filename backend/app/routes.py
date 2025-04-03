from fastapi import APIRouter
from app.auth.routes.register import router as register_router
from app.auth.routes.login import router as login_router
from app.auth.routes.logout import router as logout_router
from app.auth.routes.profile import router as profile_router

router = APIRouter()

router.include_router(register_router, tags=["auth"], prefix="/auth")
router.include_router(login_router, tags=["auth"], prefix="/auth")
router.include_router(logout_router, tags=["auth"], prefix="/auth")
router.include_router(profile_router, tags=["auth"], prefix="/auth")