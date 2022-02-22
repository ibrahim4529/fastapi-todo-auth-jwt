from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .user import User


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    is_done: bool
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User]= Relationship(back_populates="todos")