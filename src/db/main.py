from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlalchemy.orm import sessionmaker

engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))

async def get_session():
    
    Session = sessionmaker(
        bind = engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    
    async with Session() as session:
        yield session

