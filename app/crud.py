from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from . import models, schemas

async def get_user(db: AsyncSession, user_id: int):
    """Получает пользователя по его ID."""
    return await db.get(models.User, user_id)

async def get_user_by_email(db: AsyncSession, email: str):
    """Поиск пользователя в базе по email."""
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str):
    """Поиск пользователя по username."""
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """Создание нового пользователя в базе данных."""
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_tasks(db: AsyncSession, user_id: int):
    """Получает все задачи пользователя по его ID."""
    result = await db.execute(select(models.Task).filter(models.Task.user_id == user_id))
    return result.scalars().all()

async def create_task(db: AsyncSession, task: schemas.TaskCreate):
    """Создание новой задачи."""
    db_task = models.Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task(db: AsyncSession, task_id: int, task: schemas.TaskCreate):
    """Обновление существующей задачи по её ID. Если задача не найдена, генерируется ошибка."""
    db_task = await db.get(models.Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def delete_task(db: AsyncSession, task_id: int):
    """Удаление задачи по её ID. Если задача не найдена, генерируется ошибка."""
    db_task = await db.get(models.Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(db_task)
    await db.commit()
    return db_task
