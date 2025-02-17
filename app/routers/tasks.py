from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task, status_code=201)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Создание новой задачи для пользователя.
    """
    created_task = await crud.create_task(db=db, task=task)
    return created_task

@router.get("/user/{user_id}", response_model=list[schemas.Task])
async def read_tasks(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Получение всех задач пользователя по его ID.
    """
    tasks = await crud.get_tasks(db, user_id=user_id)
    return tasks

@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    """
    Обновление задачи по её ID.
    Если задача не найдена, генерируется ошибка.
    """
    db_task = await crud.update_task(db=db, task_id=task_id, task=task)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}", response_model=schemas.Task)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удаление задачи по её ID.
    Если задача не найдена, генерируется ошибка.
    """
    db_task = await crud.delete_task(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
