from fastapi import APIRouter, Depends

from api.v1.routes.auth import get_current_user
from api.v1.schemas import LeadOut
from bot.uow.sql import SQLUoW


router = APIRouter()


@router.get('/leads', response_model=list[LeadOut])
async def list_leads(user=Depends(get_current_user)) -> list[LeadOut]:
    async with SQLUoW() as uow:
        leads = await uow.leads_repo.list_leads()

    return [
        LeadOut(
            id=lead.id,
            external_id=lead.external_id,
            sender_id=lead.sender_id,
            chat_id=lead.chat_id,
            message_text=lead.message_text,
            is_lead=lead.is_lead,
            reason=lead.reason,
            processing_status=lead.processing_status.value,
            username=lead.user.username if lead.user else None,
            chat_title=lead.chat.chat_title if lead.chat else None,
        )
        for lead in leads
    ]
