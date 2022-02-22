from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routes import auth, todo
import os

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/test")
def index():
    return {"test": "Hello World"}

@app.on_event('startup')
def on_startup():
    print("Starting up...")
    print(os.environ.get(key='DB_URL'))
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(todo.router)