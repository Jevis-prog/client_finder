from fastapi import APIRouter

from api.v1.routes import auth, leads, stats


router = APIRouter()
router.include_router(auth.router, tags=['auth'])
router.include_router(leads.router, tags=['leads'])
router.include_router(stats.router, tags=['stats'])
