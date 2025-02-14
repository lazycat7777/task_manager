from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter()

@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, user_id: int, db: Session = Depends(database.SessionLocal)):
    return crud.create_task(db=db, task=task, user_id=user_id)

@router.get("/tasks/", response_model=list[schemas.Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(database.SessionLocal)):
    return crud.get_tasks(db=db, skip=skip, limit=limit)

@router.get("/users/{user_id}/tasks/", response_model=list[schemas.Task])
def get_user_tasks(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(database.SessionLocal)):
    return crud.get_user_tasks(db=db, user_id=user_id, skip=skip, limit=limit)

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(database.SessionLocal)):
    return crud.update_task(db=db, task_id=task_id, task=task)

@router.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(database.SessionLocal)):
    return crud.delete_task(db=db, task_id=task_id)
