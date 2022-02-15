from sqlmodel import SQLModel
from .auth import UserRead

class TodoBase(SQLModel):
    title: str
    content: str
    is_done: bool

class TodoRead(TodoBase):
    id: int
    user: UserRead


class TodoCreate(TodoBase):
    pass