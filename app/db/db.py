from sqlmodel import Session, create_engine, SQLModel
from app.config import get_config
from app.models import *
config = get_config()

engine = create_engine(config.DB_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)