from fastapi import APIRouter
from src.document.models import DocumentCreateModel
from src.document.service import DocumentService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

docService = DocumentService()

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



