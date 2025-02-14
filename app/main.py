# app/main.py
from fastapi import FastAPI

from app.routers import task, user
from . import models, database


# Создание таблиц
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Подключение роутеров
app.include_router(user.router)  # Правильный путь
app.include_router(task.router)  # Правильный путь
