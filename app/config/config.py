from pydantic import BaseSettings

class Setting(BaseSettings):
    APP_NAME = "My App"
    DB_URL = "sqlite:///db.sqlite"
    SECRET_KEY = "secret"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRE_TIME_HOUR = 6
    # ...
    
    class Config:
        env_file = ".env"


def get_config():
    return Setting()
