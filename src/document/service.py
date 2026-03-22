from sqlmodel import select
from src.db.schemas import Document
from sqlmodel.ext.asyncio.session import AsyncSession
from src.document.models import DocumentCreateModel
from itsdangerous.url_safe import URLSafeSerializer
from datetime import datetime
from typing import Dict
import logging
from src.config import Config


serializer = URLSafeSerializer(
    secret_key=Config.SERIALIZER_SECRET,
    salt="codesync"
)

class DocumentService:
    
    async def create_document(self,doc_details : DocumentCreateModel,session : AsyncSession) -> Dict:
        new_doc = doc_details.model_dump()
        document = Document(**new_doc)
        session.add(document)
        await session.commit()
        await session.refresh(document)

        return document.model_dump()
    
    async def get_document(self,doc_id : str,session : AsyncSession):
        
        statement = select(Document).where(Document.uid == doc_id)

        result = await session.exec(statement=statement)
        document = result.first()
        return document
    
    async def update_document(self,content : bytes,doc_id : str,session : AsyncSession) -> Dict | None:

        document = await self.get_document(doc_id=doc_id,session=session)

        if document :
            document.content = content
            document.updated_at = datetime.utcnow()
            
            await session.commit()
            await session.refresh(document)
            return document.model_dump()
        
        logging.warning(f"Document {doc_id} Not Present in Database")
        return None


class InviteService:

    async def serialize(self,doc_id : str,permission:str):
        try : 
            return serializer.dumps(
            {
                "doc_id":doc_id,
                "permission":permission
            })
        except Exception as e:
            logging.error(f"Could not serialize data :{str(e)}")
        
    async def deserialize(self,token : str):
        try : 
            return serializer.loads(token)
        except Exception as e:
            logging.error(f"Could not do this I dont know what: {str(e)}")







