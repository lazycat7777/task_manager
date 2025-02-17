import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Берем URL базы данных из окружения, для тестов он будет задан в docker-compose
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/test_task_manager")

# Создаем движок для асинхронного соединения с базой данных
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# Настройка сессии для асинхронного взаимодействия
AsyncSessionLocal = sessionmaker(
    engine, autocommit=False, autoflush=False, class_=AsyncSession
)

Base = declarative_base()

# Функция для получения сессии для работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
