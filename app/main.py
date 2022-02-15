from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routes import auth, todo

app = FastAPI()

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(todo.router)