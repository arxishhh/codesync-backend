from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlalchemy.orm import sessionmaker
from y_py import encode_state_as_update
from fastapi import FastAPI
import asyncio
from src.document.service import DocumentService
import logging

service = DocumentService()

engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))

Session = sessionmaker(
        bind = engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

async def get_session():
    async with Session() as session:
        yield session

async def create_session():
    async with Session() as session:
        return session

async def autosave_loop(app : FastAPI):

    docmanager = app.state.docmanager

    while True:
        await asyncio.sleep(30)
        logging.info("Auto-Saving Documents")
        async with Session() as session:
            for doc_id,content in list(docmanager.documents.items()):

                contentEncoded = encode_state_as_update(content)
                
                if not await service.update_document(
                    doc_id=doc_id,
                    content=contentEncoded,
                    session=session) :
                    logging.error(f"Failed to Update Document: {doc_id}")






            




