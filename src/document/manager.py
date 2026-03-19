from typing import Dict
from y_py import YDoc,encode_state_as_update,apply_update
from src.document.service import DocumentService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.schemas import Document
from src.db.main import create_session

docService = DocumentService()

class DocumentManager:
    def __init__(self):
        self.documents : Dict[str,YDoc] = {}

    async def get_or_create(self,doc_id : str,session : AsyncSession,document:Document) -> YDoc | None:

        if doc_id in self.documents:
            return self.documents[doc_id]
        
        doc = self.documents.get(doc_id)
        if doc:
            return doc
        
        ydoc = YDoc()
        
        if document and document.content:
            with ydoc.begin_transaction():
                apply_update(ydoc,document.content)
            
        self.documents[doc_id] = ydoc
        return ydoc


    async def update(self,doc_id : str,updates : bytes,session : AsyncSession,document:Document):
        doc = await self.get_or_create(doc_id=doc_id,session=session,document=document)

        if not doc :
            return None
        
        with doc.begin_transaction():
            apply_update(doc,updates)

    async def get_state(self,doc_id : str,session : AsyncSession,document: Document):
        doc = await self.get_or_create(doc_id=doc_id,session=session,document=document)
        if doc :
            return encode_state_as_update(doc)
        return None
    
    async def delete(self,doc_id : str):
        if doc_id in self.documents:
            state = self.documents[doc_id]
            content = encode_state_as_update(state)
            session= await create_session()

            await docService.update_document(
                doc_id=doc_id,
                content=content,
                session=session
            )

            self.documents.pop(doc_id)




