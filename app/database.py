from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@db/task_manager"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    """
    Функция, которая предоставляет сессию для взаимодействия с базой данных.
    Сессия автоматически закрывается после выполнения.
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()