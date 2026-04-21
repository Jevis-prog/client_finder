from fastapi import APIRouter

from api.v1.routes import auth, leads


router = APIRouter()
router.include_router(auth.router, tags=['auth'])
router.include_router(leads.router, tags=['leads'])
