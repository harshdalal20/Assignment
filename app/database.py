import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:Dalal1024@localhost:5432/taskdb")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False)
Base = declarative_base()

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
