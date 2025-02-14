from pydantic import BaseModel
from datetime import date

class TaskBase(BaseModel):
    title: str
    description: str
    due_date: date

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    tasks: list[Task] = []

    class Config:
        from_attributes = True
