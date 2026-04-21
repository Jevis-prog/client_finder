from fastapi import APIRouter, Depends

from api.v1.routes.auth import get_current_user
from api.v1.schemas import StatsOut
from bot.uow.sql import SQLUoW


router = APIRouter()


@router.get('/stats', response_model=StatsOut)
async def get_stats(user=Depends(get_current_user)) -> StatsOut:
    async with SQLUoW() as uow:
        stats = await uow.leads_repo.get_stats()

    return StatsOut(**stats)
