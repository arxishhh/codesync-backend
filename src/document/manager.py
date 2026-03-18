from typing import Dict
from y_py import YDoc,encode_state_as_update,apply_update
from src.document.service import DocumentService
from sqlmodel.ext.asyncio.session import AsyncSession

docService = DocumentService()

class DocumentManager:
    def __init__(self):
        self.documents : Dict[str,YDoc] = {}

    async def get_or_create(self,doc_id : str,session : AsyncSession) -> YDoc | None:

        if doc_id in self.documents:
            return self.documents[doc_id]
        
        doc = self.documents.get(doc_id)
        if doc:
            return doc
        
        ydoc = YDoc()
        document = await docService.get_document(
            doc_id=doc_id,
            session = session)
        
        if not document:
            return None
        
        if document and document.content:
            with ydoc.begin_transaction():
                apply_update(ydoc,document.content)
            
        self.documents[doc_id] = ydoc
        return ydoc


    async def update(self,doc_id : str,updates : bytes,session : AsyncSession):
        doc = await self.get_or_create(doc_id=doc_id,session=session)

        if not doc :
            return None
        
        with doc.begin_transaction():
            apply_update(doc,updates)

    async def get_state(self,doc_id : str,session : AsyncSession):
        doc = await self.get_or_create(doc_id=doc_id,session=session)
        if doc :
            return encode_state_as_update(doc)
        return None




