from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """
    Модель данных для пользователя в базе данных.
    Каждый пользователь имеет уникальные username и email.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user",
                         cascade="all, delete-orphan")


class Task(Base):
    """
    Модель данных для задачи в базе данных.
    Каждая задача имеет заголовок, описание и дату завершения.
    Задача связана с пользователем.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    due_date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="tasks")
