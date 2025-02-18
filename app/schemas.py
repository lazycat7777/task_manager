from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class UserBase(BaseModel):
    """
    Базовая схема для пользователя, включающая имя пользователя и email.
    """
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Схема для создания нового пользователя.
    """
    pass


class User(UserBase):
    """
    Схема пользователя с ID, предназначена для возврата данных из API.
    """
    id: int

    class Config:
        """
        Настройки для Pydantic, чтобы использовать ORM модели (SQLAlchemy).
        """
        from_attributes = True


class TaskBase(BaseModel):
    """
    Базовая схема для задачи, включающая заголовок, описание и дату завершения.
    """
    title: str
    description: str
    due_date: date
    user_id: int


class TaskCreate(TaskBase):
    """
    Схема для создания новой задачи.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Схема для обновления задачи.
    Позволяет обновлять только переданные поля.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None


class Task(TaskBase):
    """
    Схема задачи с ID, предназначена для возврата данных из API.
    """
    id: int

    class Config:
        """
        Настройки для Pydantic, чтобы использовать ORM модели (SQLAlchemy).
        """
        from_attributes = True
