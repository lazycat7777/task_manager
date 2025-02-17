import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

environment = os.getenv("PRODUCTION", "False")
testing = os.getenv("TESTING", "False")

PRODUCTION_DATABASE_URL = os.getenv("PRODUCTION_DATABASE_URL")
TESTING_DATABASE_URL = os.getenv("TESTING_DATABASE_URL")

if environment == "True":
    DATABASE_URL = PRODUCTION_DATABASE_URL
elif testing == "True":
    DATABASE_URL = TESTING_DATABASE_URL
else:
    DATABASE_URL = PRODUCTION_DATABASE_URL    

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    engine, autocommit=False, autoflush=False, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
