from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    """
    Базовая схема для пользователя, включающая имя пользователя и email.
    """
    username: str
    email: str

class UserCreate(UserBase):
    """
    Схема для создания нового пользователя.
    Наследует UserBase и добавляет дополнительные проверки для создания.
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
        orm_mode = True

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
    Наследует TaskBase и добавляет дополнительные проверки для создания задачи.
    """
    pass

class Task(TaskBase):
    """
    Схема задачи с ID, предназначена для возврата данных из API.
    """
    id: int

    class Config:
        """
        Настройки для Pydantic, чтобы использовать ORM модели (SQLAlchemy).
        """
        orm_mode = True
