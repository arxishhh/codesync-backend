from fastapi import APIRouter
from src.document.models import DocumentCreateModel,InviteModel
from src.document.service import DocumentService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from src.document.service import InviteService
import logging

docService = DocumentService()
inviteService = InviteService()

docroute = APIRouter()

@docroute.post('/create')
async def create_document(doc_details : DocumentCreateModel,session : AsyncSession = Depends(get_session)):

    new_doc = await docService.create_document(
        doc_details=doc_details,
        session=session
    )

    return {
        'message' : "Document Created Successfully",
        'document' : new_doc
    }

@docroute.get("/invite")
async def create_invite(invite_details : InviteModel):
    
    token = await inviteService.serialize(
        doc_id=invite_details.doc_id,
        permission=invite_details.permission
    )
    if token : 
        return token
    
    logging.error("Failed to Generate Invite Link")





