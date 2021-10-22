from fastapi import APIRouter

from auth import router as auth
from live import router as live
from users import router as users

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(live.router, prefix="/live", tags=["live"])
router.include_router(users.router, tags=["users"])
