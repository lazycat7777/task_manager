from fastapi import FastAPI
from .routers import users, tasks
from .database import engine, Base

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)