from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models import Todo, User
from app.db import get_session
from app.utils import get_active_user
from app.schemas import TodoRead, TodoCreate
from typing import List


router = APIRouter(
    prefix="/todos",
    tags=["Todo"],
    dependencies=[Depends(get_active_user)]
)


@router.get("/", response_model=List[TodoRead])
async def read_root(db: Session = Depends(get_session), user: User = Depends(get_active_user)):
    return db.exec(select(Todo).where(Todo.user_id == user.id)).fetchall()


@router.post(path="/", response_model=TodoRead)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_session), user: User = Depends(get_active_user)):
    todo_db = Todo.from_orm(todo)
    todo_db.user_id = user.id
    db.add(todo_db)
    db.commit()
    return todo_db